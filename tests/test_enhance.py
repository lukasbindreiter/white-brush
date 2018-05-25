from pytest_mock import MockFixture

from tests.resources import get_test_image
from white_brush.enhance import enhance
from white_brush.entities.color_configuration import ColorConfiguration
from white_brush.services import enhance_service


class TestEnhance:
    def test_enhancing_a_single_image_no_color_config(self):
        """
        Enhancing a single Image with the default color configuration
        should run through without any errors
        """
        img_name, img = get_test_image()
        enhanced = enhance(img, ColorConfiguration())
        assert img.shape == enhanced.shape

    def test_enhancing_a_single_image_only_bg_color(self):
        """
        Enhancing a single Image with the default foreground color and
        a user specified background color should run through without
        any errors
        """
        img_name, img = get_test_image()
        enhanced = enhance(img, ColorConfiguration(background_color="green"))
        assert img.shape == enhanced.shape

    def test_enhancing_a_single_image_only_fg_color(self):
        """
        Enhancing a single Image with the default background color and
        a user specified foreground color should run through without
        any errors
        """
        img_name, img = get_test_image()
        enhanced = enhance(img, ColorConfiguration(foreground_color="red"))
        assert img.shape == enhanced.shape

    def test_enhancing_a_single_image_fg_and_bg_color(self):
        """
        Enhancing a single Image with a user specified foreground and
        background color should run through without any errors
        """
        img_name, img = get_test_image()
        enhanced = enhance(img, ColorConfiguration(foreground_color="black",
                                                   background_color="white"))
        assert img.shape == enhanced.shape


class TestEnhanceService:
    def test_enhance_service(self, mocker: MockFixture):
        # mock the io module
        name, img = get_test_image()
        mock_io = mocker.patch("white_brush.io")()
        mock_io.read_image.return_value = img
        enhance_service.io = mock_io

        service = enhance_service.EnhanceService()
        service.enhance_file("input.jpg", "output.jpg", 0, ColorConfiguration())

        mock_io.read_image.assert_called_with("input.jpg")
        mock_io.write_image.assert_called_once()
