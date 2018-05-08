from white_brush import calc_colors
import numpy as np


class TestCalcColors:
    def test_choose_representative_colors_only_black(self):
        input = np.array(
            [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        (colors, assigned) = calc_colors.choose_representative_colors(input)
        assert (colors == input).all(), "Wrong representative colors are returned, expect to get 8 times zeroes"