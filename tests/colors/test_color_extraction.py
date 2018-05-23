from numpy.testing import assert_allclose

import white_brush.colors.color_extraction as ce
from tests.resources import *
from white_brush.colors.color_balance import balance_color


class TestColorExtraction:

    def test_hsv_thresholding_with_example_images(self):
        """Test thresholding using the hsv distance method"""
        # these values were precalculated once, this test is to make
        # sure that the calculation works the same on all platforms
        # (which e.g. is not the case if the images were in a lossy
        # format like jpg)
        expected_masked_pixels = {
            "01.png": 16352,
            "02.png": 18696,
            "03.png": 28549
        }

        for name, img in get_test_images():
            if name in expected_masked_pixels:
                img = balance_color(img)
                bg_colors = ce.extract_background_colors(img, thresh=0.4)
                mask = ce.hsv_distance_threshold(img, bg_colors)
                assert mask.sum() == expected_masked_pixels[name]

        # if no bg_colors are specified, they should be calculated from
        # the image automatically, using the default thresh value
        name, img = get_test_image()
        mask_auto = ce.hsv_distance_threshold(img)
        assert mask_auto.shape == (img.shape[0], img.shape[1])

    def test_adaptive_thresholding_with_example_images(self):
        expected_masked_pixels = {
            "01.png": 138641,
            "02.png": 96992,
            "03.png": 150182
        }

        for name, img in get_test_images():
            if name in expected_masked_pixels:
                img = balance_color(img)
                mask = ce.adaptive_threshold(img, 9, 3)
                assert mask.sum() == expected_masked_pixels[name]

    def test_extract_background_colors(self):
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
            background = ce.extract_background_colors(img,
                                                      thresh=1)

            if img_name in expected_colors:
                bg_color = expected_colors[img_name]
                assert_allclose(background.ravel(), bg_color)

            # make sure multiple background color extraction works as well
            backgrounds = ce.extract_background_colors(img)
            assert backgrounds.ndim == 2
            assert backgrounds.shape[1] == 3

