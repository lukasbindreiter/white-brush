# White Brush [![GitHub license](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/lukasbindreiter/white-brush/blob/master/LICENSE)

| branch        | status        | information |
| ------------- | --------------| ------- |
| **master**        | [![Build Status](https://travis-ci.org/lukasbindreiter/white-brush.svg?branch=master)](https://travis-ci.org/lukasbindreiter/white-brush) |[Download latest release](https://github.com/lukasbindreiter/white-brush/releases)|
| Christoph   | [![Build Status](https://travis-ci.org/lukasbindreiter/white-brush.svg?branch=developer%2Fchristoph)](https://travis-ci.org/lukasbindreiter/white-brush) |[Assigned Issues/Todos](https://github.com/lukasbindreiter/white-brush/issues?q=is%3Aopen+assignee%3AShynixn)
| Philipp   | [![Build Status](https://travis-ci.org/lukasbindreiter/white-brush.svg?branch=philipp)](https://travis-ci.org/lukasbindreiter/white-brush) |[Assigned Issues/Todos](https://github.com/lukasbindreiter/white-brush/issues?utf8=%E2%9C%93&q=is%3Aopen+assignee%3AEthlaron)

 White Brush is a tool for enhancing hand-written notes.

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
4. Profit