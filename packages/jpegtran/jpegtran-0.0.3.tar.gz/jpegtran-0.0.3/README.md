# JPEG: A Python wrapper for jpegtran

JPEG is a Python wrapper for jpegtran, designed to make it easier to interact with and manipulate JPEG files directly from Python. It is much faster than Pillow and OpenCV, as it operates directly on the JPEG file headers. This also means, as you might expect, only the JPEG format is supported.

## Dependancies
You must have [jpegtran](https://jpegclub.org/jpegtran/) installed on your system to use this library.

## Installation
To install the JPEG Python wrapper, you can use pip:

```python
pip install jpegtran
```

## Usage

Here's how to use the JPEG wrapper to open a JPEG file, optimize it, rotate it by 90 degrees, and save the result:

```python
import jpeg

jpeg \
    .open('example.jpg') \
    .optimize() \
    .rotate(90) \
    .save('example-rotated.jpg')
```
