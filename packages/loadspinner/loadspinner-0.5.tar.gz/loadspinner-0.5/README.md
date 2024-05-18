# loadspinner
![Pepy Total Downlods](https://img.shields.io/pepy/dt/loadspinner)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/loadspinner)
![GitHub repo size](https://img.shields.io/github/repo-size/xyzpw/loadspinner)

A CLI based loading spinner which is used to tell the user work is being done in the background.

**Loadspinner** contains more than 20 spinners to choose from, and you can even create your own spinner.

## Prerequisites
- Terminal that accepts ANSI codes

## Usage
Creating a spinner:
```python
import loadspinner
spinner = loadspinner.Spinner(spinner_type="classic")
```

Starting the spinner:
```python
spinner.start() # starts the spinner
spinner.stop() # stops the spinner
```

> [!HINT]
> You can also assign a timer to spinners, e.g. `spinner.start(5)` will stop the spinner after 5 seconds.

Usage with context managers:
```python
import loadspinner
with loadspinner.Spinner("newton"):
    input("press enter to stop ")
```

Usage with decorators:
```python
from loadspinner import functionSpinner
@functionSpinner("building")
def doWork():
    # code...
doWork()
```

Spinners can be made or customized:
```python
import loadspinner
loadspinner.makeSpinner(
    name="myCustomSpinner",
    frames=["a", "b", "c", "1", "2", "3"],
    interval=200,
)
```
The above code will create its own spinner which can be accessed as its own name, e.g. `loadspinner.Spinner("myCustomSpinner")`
