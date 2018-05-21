from unittest.mock import Mock

from pytest_mock import MockFixture

from tests.resources import get_test_image
from white_brush.services import enhance_service
from white_brush.enhance import enhance


class TestEnhance:
    def test_enhancing_a_single_imge(self):
        """
        Enhancing a single Image should run through without any errors
        """
        img_name, img = get_test_image()
        enhanced = enhance(img)
        assert img.shape == enhanced.shape


class TestEnhanceService:
    def test_enhance_service(self, mocker: MockFixture):
        name, img = get_test_image()

        def mock_io_read(filename):
            return img

        def mock_io_write(filename, img):
            pass

        mocker.patch("enhance_service.io.read_image", mock_io_read)
        mocker.patch("enhance_service.enhance", lambda x: x)
        mocker.patch("enhance_service.io.write_image", mock_io_write)

        service = enhance_service.EnhanceService()
        service.enhance_file("input.jpg", "output.jpg")

        enhance_service.io.read_image.assert_called_once_with("input.jpg")
        enhance_service.io.write_image.assert_called_once()
        enhance_service.enhance.assert_called_once()
