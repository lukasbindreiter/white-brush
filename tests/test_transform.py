from numpy.testing import assert_allclose

from tests.resources import get_test_image
from white_brush.transform import resize_if


class TestTransform:

    def test_resize_if_no_resizing(self):
        """
        Given:
            an image which should not be changed based on its size
        When:
            resize_if is called
        Then:
            The image should stay the same
        """
        img_name, img = get_test_image()
        # img.shape == (629, 919, 3)
        resized = resize_if(img, 500, 1000)
        assert_allclose(img, resized)

    def test_resize_if_no_resizing(self):
        """
        Given:
            an image which should be changed based on its size
        When:
            resize_if is called
        Then:
            The image should have the specified size
        """
        img_name, img = get_test_image()
        # img.shape == (629, 919, 3)
        resized = resize_if(img, 500, 800)
        assert resized.shape == (342, 500, 3)
