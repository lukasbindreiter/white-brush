# White Brush
 Enhancing hand-written notes

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