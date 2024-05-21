## Installation

```python
pip install jpegtran
```

## Usage

```python
import jpeg

jpeg \
    .open('example.jpg') \
    .optimize() \
    .rotate(90) \
    .save('example-rotated.jpg')
```