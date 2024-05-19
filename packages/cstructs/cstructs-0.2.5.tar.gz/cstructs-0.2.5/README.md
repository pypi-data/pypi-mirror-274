# cstructs
Think [`struct`](https://docs.python.org/3/library/struct.html), but on steroids. 

[![PyPI - Version](https://img.shields.io/pypi/v/cstructs.svg)](https://pypi.org/project/cstructs)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cstructs.svg)](https://pypi.org/project/cstructs)
[![PyPI - License](https://img.shields.io/pypi/l/cstructs.svg)](https://pypi.org/project/cstructs)
[![status](https://github.com/yntha/cstructs/actions/workflows/run-tests.yml/badge.svg?branch=feature%2Fread-binary-data)](https://github.com/yntha/cstructs/actions/workflows/run-tests.yml)

-----
***Note:*** *This version supercedes the original [cstruct](https://github.com/yntha/cstruct) package. This is my first attempt at a test driven development cycle, so I apologize in advance if the things that I do don't make sense.*

**Table of Contents**

- [Installation](#installation)
- [Features](#features)
- [Usage](tests/)
- [License](#license)

## Installation

```console
python -m pip install --user -U cstructs
```

## Features
- [x] Serializing
- [x] Deserializing
- [x] Inheritance between datastructs
- [x] Sequences
- [x] Allow other datastructs to be members
- [x] Callbacks for reading/writing
- [x] Individual class metadata
- [x] Variable length data by depending on the value of another member
- [x] String decoding using specified encoding format
- [x] Lazy sequence loading
- [x] Fallback(default) value for missing values
- [ ] Handling of various types of data alignment
- [ ] Is type checker friendly
## License

`cstructs` is distributed under the terms of the [GNU GPL v3](https://spdx.org/licenses/GPL-3.0-or-later.html) license.
