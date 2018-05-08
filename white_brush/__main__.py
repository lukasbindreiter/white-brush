import argparse
from white_brush import calc_colors
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    return parser.parse_args()


def main():
    input = np.array(
        [[0, 10, 30], [10, 15, 12], [8, 6, 4], [56, 50, 45], [45, 2, 45], [0, 0, 0], [10, 56, 4], [5, 7, 9],
         [1, 4, 7], [1, 54, 8], [9, 65, 4], [6, 5, 47], [5, 78, 5], [6, 1, 54], [6, 57, 45], [1, 1, 1]])
    calc_colors.choose_representative_colors(input)
    # args = parse_args()

    # print("Input: {}, Output: {}".format(args.input_file, args.output_file))


if __name__ == "__main__":
    main()
