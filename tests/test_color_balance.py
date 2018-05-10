import cv2
import numpy as np
from hypothesis import given, assume
from hypothesis.extra.numpy import arrays

from tests.resources import get_test_images
from white_brush.color_balance import balance_color


class TestColorBalance:

    def test_color_balance_with_test_images(self):
        """
        Given the test images located in the test_images directory

        Performing color balancing on an image

        Should result in an image where the color values of each channel
        are distributed from 0 to 255
        """
        for name, img in get_test_images():
            balanced_img = balance_color(img)

            assert balanced_img.max() == 255, \
                "Maximum of a balanced image should be 255"
            assert balanced_img.min() == 0, \
                "Minimum of a balanced image should be 0"
            for channel in cv2.split(balanced_img):
                assert channel.max() == 255, \
                    "Maximum of each channel should be 255"
                assert channel.max() == 255, \
                    "Minimum of each channel should be 0"

    @given(arrays(shape=(100, 100, 3), dtype=np.uint8))
    def test_color_balance_random_images(self, img):
        """
        Given random test images

        Assuming that the image contains two different values in every
        channel

        Performing color balancing on the image

        Should result in an image where the color values of each channel
        are distributed from 0 to 255
        """

        # color balance only works if every channel has at least two different
        # values, otherwise everything in that channel would be mapped to 0
        for channel in cv2.split(img):
            assume(len(np.unique(channel)) >= 2)

        balanced_img = balance_color(img)

        assert balanced_img.max() == 255, \
            "Maximum of a balanced image should be 255"
        assert balanced_img.min() == 0, \
            "Minimum of a balanced image should be 0"
        for channel in cv2.split(balanced_img):
            assert channel.max() == 255, \
                "Maximum of each channel should be 255"
            assert channel.max() == 255, \
                "Minimum of each channel should be 0"
