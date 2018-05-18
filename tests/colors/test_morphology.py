import numpy as np
from numpy.testing import assert_allclose

from white_brush.colors.morphology import erode, dilate, smooth


class TestMorphology:

    def test_erosion(self):
        input = """
                #------
                -#-----
                --#----
                ---#--- 
                ----#--
                """
        expected_output = """
                -------
                -------
                -------
                ------- 
                -------
                """
        input_mask = self._generate_mask_from_str(input)
        expected_mask = self._generate_mask_from_str(expected_output)
        eroded = erode(input_mask, 3)
        assert_allclose(eroded, expected_mask)
        input = """
                -------
                --###--
                --###--
                --###-- 
                -------
                """
        expected_output = """
                -------
                -------
                ---#---
                ------- 
                -------
                """
        input_mask = self._generate_mask_from_str(input)
        expected_mask = self._generate_mask_from_str(expected_output)
        eroded = erode(input_mask, 3)
        assert_allclose(eroded, expected_mask)

    def test_dilation(self):
        input = """
                -------
                -#---#-
                -------
                ------- 
                ---#---
                """
        expected_output = """
                ###-###
                ###-###
                ###-###
                --###-- 
                --###--
                """
        input_mask = self._generate_mask_from_str(input)
        expected_mask = self._generate_mask_from_str(expected_output)
        dilated = dilate(input_mask, 3)
        assert_allclose(dilated, expected_mask)
        input = """
                -------
                --###--
                --###--
                --###-- 
                -------
                """
        expected_output = """
                -#####-
                -#####-
                -#####-
                -#####- 
                -#####-
                """
        input_mask = self._generate_mask_from_str(input)
        expected_mask = self._generate_mask_from_str(expected_output)
        dilated = dilate(input_mask, 3)
        assert_allclose(dilated, expected_mask)

    def test_smoothing(self):
        input = """
                --####--------
                ---####-------
                ----###-------
                ---#####------
                ---####-------
                ---####-------
                --#####-------
                ---####-------
                """
        expected_output = """
                ---####-------
                ---####-------
                ---####-------
                ---####-------
                ---####-------
                ---####-------
                ---####-------
                ---####-------
                """
        input_mask = self._generate_mask_from_str(input)
        expected_mask = self._generate_mask_from_str(expected_output)
        smoothed = smooth(input_mask, 3)

        assert_allclose(smoothed, expected_mask)

    def _generate_mask_from_str(self, str_mask):
        """
        Parse a boolean mask from a given string

        The given str_mask may look something like this:
        ##-#-#
        -#--#-
        ##---#
        ###--#

        # will be replaced by True, space by False
        """
        # remove the first and last line, since they are just empty
        str_array = np.asarray(
            [list(row.strip()) for row in str_mask.strip().split("\n")])
        assert str_array.ndim == 2, \
            "Each row in the mask has to contain the same number of characters"

        def str_to_bool(s):
            return s == "#"

        mask = np.vectorize(str_to_bool)(str_array)
        return mask
