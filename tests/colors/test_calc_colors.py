from white_brush.colors import calc_colors
import numpy as np


class TestCalcColors:
    def test_choose_representative_colors_only_black(self):
        input = np.array(
            [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        (colors, assigned) = calc_colors.choose_representative_colors(input)
        assert (colors == input).all(), "Wrong representative colors are returned, expect to get 8 times zeroes"

    def test_choose_representative_colors_only_black(self):
        input = np.array(
            [[254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254],
             [254, 254, 254], [10, 10, 10]])

        expected = np.array(
            [[255, 255, 254], [0, 0, 10], [0, 0, 10], [255, 255, 254], [255, 255, 254], [255, 255, 254],
             [255, 255, 254], [255, 255, 254]])

        (colors, assigned) = calc_colors.choose_representative_colors(input)

        assert np.allclose(expected, colors), "Wrong representative colors are returned."
