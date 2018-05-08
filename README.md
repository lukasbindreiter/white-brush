# White Brush [![GitHub license](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/lukasbindreiter/white-brush/blob/master/LICENSE)

| branch        | status        | information |
| ------------- | --------------| ------- |
| **master**        | [![Build Status](https://travis-ci.org/lukasbindreiter/white-brush.svg?branch=master)](https://travis-ci.org/lukasbindreiter/white-brush) | [![Coverage Status](https://coveralls.io/repos/github/lukasbindreiter/white-brush/badge.svg)](https://coveralls.io/github/lukasbindreiter/white-brush) |
| Christoph   | [![Build Status](https://travis-ci.org/lukasbindreiter/white-brush.svg?branch=developer%2Fchristoph)](https://travis-ci.org/lukasbindreiter/white-brush) |[Assigned Issues/Todos](https://github.com/lukasbindreiter/white-brush/issues?q=is%3Aopen+assignee%3AShynixn)
| Philipp   | [![Build Status](https://travis-ci.org/lukasbindreiter/white-brush.svg?branch=philipp)](https://travis-ci.org/lukasbindreiter/white-brush) |[Assigned Issues/Todos](https://github.com/lukasbindreiter/white-brush/issues?q=assignee%3Ap-hofer+is%3Aopen)
| Lukas   | [![Build Status](https://travis-ci.org/lukasbindreiter/white-brush.svg?branch=developer%2Flukas)](https://travis-ci.org/lukasbindreiter/white-brush) |[Assigned Issues/Todos](https://github.com/lukasbindreiter/white-brush/issues?q=assignee%3Alukasbindreiter+is%3Aopen)

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

#### Docker Usage
Instead of installing the `pipenv` dependencies on your system,
you can also use the `Dockerfile` which is provided in the root directory:

```bash
docker build -t white-brush .
docker run -it --rm white-brush python -m white_brush test_images/01.jpg 01_enhanced.jpg
```

Or to start a jupyter to which you can connect to take a look at the provided notebooks:
```bash
# First use docker build command above, then
docker run -d --rm -p 8888:8888 white_brush
```
Then go ahead and connect to `http://localhost:8888` in your browser.

