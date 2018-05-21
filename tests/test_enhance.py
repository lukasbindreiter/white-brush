from pytest_mock import MockFixture

from tests.resources import get_test_image
from white_brush.enhance import enhance
from white_brush.services import enhance_service


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
        # mock the io module
        name, img = get_test_image()
        mock_io = mocker.patch("white_brush.io")()
        mock_io.read_image.return_value = img
        enhance_service.io = mock_io

        service = enhance_service.EnhanceService()
        service.enhance_file("input.jpg", "output.jpg", None)

        mock_io.read_image.assert_called_with("input.jpg")
        mock_io.write_image.assert_called_once()

