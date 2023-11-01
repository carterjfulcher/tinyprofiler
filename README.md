# tinyprofiler

Tiny Profiler is a sub 200 line profiling utility that records telemetry from your app,
provides metrics and a flame graph to help debug latency and throughput.

## Installation

```bash
pip install tinyprofiler
```

## Usage

```python3
from tinyprofiler import Observer

observer = Observer()

@observer.profile()
def your_function():
  # do something
```

![img](./img/p.png)

## API

### `Observer`

`Observer(num_samples: int = 10, enabled: bool = True)`

- `num_samples` (optional): The number of samples to collect. You can configure how many samples to collect during profiling. The default is 10.

- `enabled` (optional): You can enable or disable profiling using this parameter. By default, profiling is enabled (True).

### `Observer.profile` (decorator)

`profile(self, trace: str = '__main__', parent: bool = False) -> None:`

- `trace` (optional) - the trace to group functions together

- `parent` (optional): Set this to True if you want to treat the decorated function as a parent node in the flame graph hierarchy.
