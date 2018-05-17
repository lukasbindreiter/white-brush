import numpy as np
import shutil
import pytest

from white_brush import io
from tests.resources import get_test_images


class TestIO:
    def test_read_image(self):
        """
        Test reading the example images
        """

        # make sure that the image files are read correctly, by
        # asserting that the sum of all colors matches to the pre-
        # calculated values defined here
        # this is the reason why the test images are only png and not
        # jpg, because a lossless format is needed in order for the
        # the loaded images to be identical regardless of the platform
        expected_image_sums = {
            "01.png": 266790403,
            "02.png": 191207327,
            "03.png": 330462814,
            "04_crop_and_rotate.png": 568133589,
            "05_blackboard.png": 128896018,
            "06_crop.png": 305926340,
            "07_multi_color.png": 264732912,
            "08_shadows.png": 266218455,
            "09_lightning.png": 351523889,
            "10.png": 553886964,
            "11.png": 468139733
        }

        for img_name, img in get_test_images():
            if img_name in expected_image_sums:
                assert img.ndim == 3
                assert img.sum() == expected_image_sums[img_name]

    def test_read_image_errors(self):
        """
        Trying to read a file which does not exist should result in an error
        """
        nonexistent_file = "this_file_doesnt_exist.jpg"
        with pytest.raises(FileNotFoundError) as error:
            io.read_image(nonexistent_file)
        assert nonexistent_file in str(error)

        # try to read the current source file as image
        nonimage_file = __file__
        with pytest.raises(IOError) as error:
            io.read_image(nonimage_file)
        assert "not a valid image file" in str(error)


    def test_writing_random_image(self):
        """
        Test writing a random image to disk
        """
        random_img = np.random.randint(0, 255, (100, 100, 3), np.uint8)
        img_out_dir = f"img_test_dir_{random_img.sum()}"
        file_name = f"{img_out_dir}/random_test_image.jpg"

        io.write_image(file_name, random_img)
        shutil.rmtree(img_out_dir)
