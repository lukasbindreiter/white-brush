import numpy as np
from hypothesis import given, assume
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers
from numpy.testing import assert_allclose

from tests.resources import get_test_images
from white_brush.colors.color_balance import balance_color
from white_brush.colors.color_extraction import extract_background_colors
from white_brush.colors.color_extraction import hsv_distance_threshold
from white_brush.colors.color_extraction import _pack_rgb_values, \
    _unpack_rgb_values, _generate_bitmask, _color_sample


class TestColorExtraction:

    def test_hsv_thresholding_with_example_images(self):
        """Test thresholding using the hsv distance method"""
        expected_masked_pixels = {
            "01.png": 561699,
            "02.png": 392820,
            "03.png": 695273,
            "04_crop_and_rotate.png": 1181497,
            "05_blackboard.png": 436050,
            "06_crop.png": 826985,
            "07_multi_color.png": 473495,
            "08_shadows.png": 658405,
            "09_lightning.png": 649505,
            "10.png": 921354,
            "11.png": 1082182
        }

        for name, img in get_test_images():
            if name in expected_masked_pixels:
                img = balance_color(img)
                bg_colors = extract_background_colors(img)
                mask = hsv_distance_threshold(img, bg_colors)
                assert mask.sum() == expected_masked_pixels[name]

    def test_extract_background_color(self):
        """Test the extraction of the background color in an image"""
        expected_colors = {
            # these four colors are different shades of grey
            "01.jpg": [164, 160, 156],
            "02.jpg": [156, 156, 156],
            "03.jpg": [156, 156, 152],
            "04_crop_and_rotate.jpg": [160, 160, 152],
            # green
            "05_blackboard.jpg": [72, 112, 60]
        }

        for img_name, img in get_test_images():
            # extract a single background color (by setting thresh to 1)
            background = extract_background_colors(img,
                                                   thresh=1)

            if img_name in expected_colors:
                bg_color = expected_colors[img_name]
                assert_allclose(background.ravel(), bg_color)

            # make sure multiple background color extraction works as well
            backgrounds = extract_background_colors(img)
            assert len(backgrounds) > 1

    def test_color_sample(self):
        """Test extracting a representative sample of pixels from an image"""
        for img_name, img in get_test_images():
            sample05 = _color_sample(img, p=0.05)
            assert sample05.size < (img.size // 20) + 5
            sample50 = _color_sample(img, p=0.5)
            assert sample50.size < (img.size // 2) + 5
            sample20 = _color_sample(img, p=0.2)
            assert sample20.size < (img.size // 5) + 5

    def test_bitmask(self):
        """Test creating a value that can be used to mask specific bits"""

        def int_to_binary_str(x: int) -> str:
            return "{:b}".format(x)

        mask = _generate_bitmask(2, 8)
        assert int_to_binary_str(mask) == "11111100"

        mask = _generate_bitmask(0, 8)
        assert int_to_binary_str(mask) == "11111111"

        mask = _generate_bitmask(4, 8)
        assert int_to_binary_str(mask) == "11110000"

        mask = _generate_bitmask(4, 16)
        assert int_to_binary_str(mask) == "1111111111110000"

    @given(integers(0, 255), integers(0, 255), integers(0, 255))
    def test_pack_rgb_values(self, r, g, b):
        """
        Test converting between a color in r, g, b format
        (three separate integers) to a single 24bit representation and back
        """
        rgb = _pack_rgb_values(r, g, b)
        assert _unpack_rgb_values(rgb) == (r, g, b)

    @given(arrays(np.uint8, (2, 3)))
    def test_pack_rgb_uniqueness(self, colors):
        """
        Assert that converting two different colors from r, g, b format
        (three separate integers) to a single 24bit representation
        results in two different values."""
        assume(np.any(colors[0] != colors[1]))
        c1 = _pack_rgb_values(*colors[0])
        c2 = _pack_rgb_values(*colors[1])
        assert c1 != c2

    @given(arrays(np.uint8, (100, 3)))
    def test_pack_rgb_values_array(self, rgb_arr):
        """
        Test converting between many colors in r, g, b format
        (three separate arrays) to a single 24bit representation and back
        """
        rgb = _pack_rgb_values(rgb_arr[:, 0],
                               rgb_arr[:, 1],
                               rgb_arr[:, 2])
        r, g, b = _unpack_rgb_values(rgb)
        rgb_back = np.stack([r, g, b], axis=1)
        assert_allclose(rgb_arr, rgb_back)
