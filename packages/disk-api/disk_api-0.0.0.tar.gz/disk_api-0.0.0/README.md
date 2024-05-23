# disk-api
An API... but in the filesystem

> [!IMPORTANT]
> This is only an idea at the current point in time

## Basic Idea

As this is only the basic idea there is nothing you can test yet.
But basically this library should offer a nice abstraction to [libfuse](https://github.com/libfuse/libfuse?tab=readme-ov-file#libfuse)

```python
from diskapi import DiskAPI

api = DiskAPI()

@api.get("/index")
def index():
    return f"Hello World"


if __name__ == '__main__':
    api.run(mount="~/api/")
```
```shell
$ cat ~/api/index
Hello World
```

## Installation

```shell
pip3 install disk-api
```
