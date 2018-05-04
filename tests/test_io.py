from white_brush import io


class TestIO:
    def test_read_image(self):
        img = io.read_image("test_images/01.jpg")
        assert img.ndim == 3, "Image matrix is three dimensional"
        assert img.shape == (629, 919, 3), "Image has wrong dimensions"
