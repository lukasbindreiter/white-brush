# White Brush [![GitHub license](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/lukasbindreiter/white-brush/blob/master/LICENSE)

White Brush is a tool for enhancing hand-written notes.

### Build Status

| Branch        | Status        | Information |
| ------------- | --------------| ------- |
| **master**        | [![Build Status](https://img.shields.io/travis/lukasbindreiter/white-brush/master.svg?style=flat-square)](https://travis-ci.org/lukasbindreiter/white-brush) | [![Coverage Status](https://img.shields.io/coveralls/lukasbindreiter/white-brush/master.svg?style=flat-square)](https://coveralls.io/github/lukasbindreiter/white-brush?branch=master) |
| Christoph   | [![Build Status](https://img.shields.io/travis/lukasbindreiter/white-brush/developer/christoph.svg?style=flat-square)](https://travis-ci.org/lukasbindreiter/white-brush) |[Assigned Issues/Todos](https://github.com/lukasbindreiter/white-brush/issues?q=is%3Aopen+assignee%3AShynixn) [![Coverage Status](https://img.shields.io/coveralls/lukasbindreiter/white-brush/developer/christoph.svg?style=flat-square)](https://coveralls.io/github/lukasbindreiter/white-brush?branch=developer%2Fchristoph) |
| Philipp   | [![Build Status](https://img.shields.io/travis/lukasbindreiter/white-brush/philipp.svg?style=flat-square)](https://travis-ci.org/lukasbindreiter/white-brush) |[Assigned Issues/Todos](https://github.com/lukasbindreiter/white-brush/issues?q=assignee%3Ap-hofer+is%3Aopen) [![Coverage Status](https://img.shields.io/coveralls/lukasbindreiter/white-brush/philipp.svg?style=flat-square)](https://coveralls.io/github/lukasbindreiter/white-brush?branch=philipp) |
| Lukas   | [![Build Status](https://img.shields.io/travis/lukasbindreiter/white-brush/developer/lukas.svg?style=flat-square)](https://travis-ci.org/lukasbindreiter/white-brush) |[Assigned Issues/Todos](https://github.com/lukasbindreiter/white-brush/issues?q=assignee%3Alukasbindreiter+is%3Aopen) [![Coverage Status](https://img.shields.io/coveralls/lukasbindreiter/white-brush/developer/lukas.svg?style=flat-square)](https://coveralls.io/github/lukasbindreiter/white-brush?branch=developer%2Flukas) |


### Usage
#### As executable  
```bash
python -m white_brush test_images/01.jpg 01_enhanced.jpg
```
#### As library
```python
import white_brush as wb

# enhance a single image
wb.enhance("test_images/01.jpg", "01_enhanced.jpg")

# multiple files at once
files = [("test_images/01.jpg", "01_enhanced.jpg"), ("test_images/02.jpg", "02_enhanced.jpg")]
wb.enhance_all(files)
```

### Contributing / Development
1. Checkout the repository
2. Install the requirements
```bash
pipenv install --dev
```
3. Run the tests
```bash
pytest
```
