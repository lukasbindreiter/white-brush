import os

from white_brush.io import read_image
from white_brush import color_extraction


class TestColorExtraction:
    def get_test_images(self):
        for image in os.listdir("test_images"):
            yield read_image(os.path.join("test_images", image))

    def test_color_sample(self):
        for img in self.get_test_images():
            sample05 = color_extraction.color_sample(img, p=0.05)
            assert sample05.size < (img.size // 20) + 5
            sample50 = color_extraction.color_sample(img, p=0.5)
            assert sample50.size < (img.size // 2) + 5
            sample20 = color_extraction.color_sample(img, p=0.2)
            assert sample20.size < (img.size // 5) + 5
