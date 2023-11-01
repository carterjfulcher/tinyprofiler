import os 
import sys
from typing import Optional
import time

class Telemetry:
  # could use pydantic here, but then we have to have reqs.txt :/
  def __init__(self, start_time: float, end_time: float, object: str, trace: str, parent: Optional[bool]):
    self.start_time = start_time
    self.end_time = end_time
    self.object = object
    self.trace = trace
    self.parent = parent

  start_time: float
  end_time: float
  object: str
  trace: str
  parent: Optional[bool]

class Observer:
  def __init__(self, num_samples: int = 10, enabled: bool = True):
    self._telemetry = []
    self._init_time = time.time()
    self._num_samples = num_samples
    self._samples = 0
    self._saved = False
    self._enabled = enabled 
  
  def analyze(self):
    traces = {}
    for t in self._telemetry:
      if t.trace not in traces:
        traces[t.trace] = []
      traces[t.trace].append(t)

    print("\nTinyProfiler\n")
    print(f"{self._samples} samples recorded in {round(time.time() - self._init_time, 2)} seconds\n")

    for trace, data in traces.items():
      print(f"===================== {trace} ===================")
      
      # separate samples
      parents = [i for i in data if i.parent]
      children = [i for i in data if not i.parent]
      samples = []
      for parent in parents:
        sample = []
        for child in children:
          if child.start_time >= parent.start_time and child.end_time <= parent.end_time:
            sample.append(child)
        # sort by start_time and guarantee parent is first
        sample.sort(key=lambda x: x.start_time)
        sample.insert(0, parent)
        samples.append(sample)

      # print metrics 
      print(f"{'Operation':<40}{'Avg':<10}{'Min':<10}{'Max':<10}")
      print(f"{'---------':<40}{'---':<10}{'---':<10}{'---':<10}")
      avgs = {}
      for unique_object in set([i.object for i in data]):
        avgs[unique_object] = []
        for sample in samples:
          for i in sample:
            if i.object == unique_object:
              avgs[unique_object].append((i.end_time - i.start_time)/1000000)
              break
      avgs = {k: v for k, v in sorted(avgs.items(), key=lambda item: sum(item[1])/len(item[1]), reverse=True)}
      for unique_object, values in avgs.items():
        print(f"{unique_object:<40}{sum(values)/len(values):<10.2f}{min(values):<10.2f}{max(values):<10.2f}ms")

      # flame graph:
      for index, sample in enumerate(samples):
        parent = sample[0]
        children = sample[1:]
        size = os.get_terminal_size().columns
        print(f"\n{f'Flame Graph: Sample {index}':^{size}}\n")
        print(f"{parent.object:<30}{'='*(size-30)}")
        total_space = size - 30
        for child in children:
          # determine offset and length
          offset = max(1, int(((child.start_time - parent.start_time) / (parent.end_time - parent.start_time)) * total_space))
          duration = max(1, int(((child.end_time - child.start_time) / (parent.end_time - parent.start_time)) * total_space))
          print(f"{child.object:<30}{offset*' '}{duration*'='}")

        try:
          input("\n\nPress any key for another sample, or ctrl+c to exit\n")
        except: 
          sys.exit(0)

  def profile(self, trace: str = '__main__', parent: bool = False):
    def decorator(func):
      def wrapper(*args, **kwargs):
        if not self._enabled:
          return func(*args, **kwargs)
        start_time = time.time_ns()
        result = func(*args, **kwargs)
        if(self._saved):
          return result
        
        end_time = time.time_ns()
        if self._samples < self._num_samples:
          self._telemetry.append(Telemetry(
            start_time=start_time,
            end_time=end_time,
            object=func.__name__,
            trace=trace,
            parent=parent
          ))
          if parent:
            self._samples += 1
        else: 
          print("Telemetry Sample Complete. Pausing... (press ctrl+c to exit)")
          self.analyze()
          sys.exit(0)
        return result
      return wrapper
    return decorator