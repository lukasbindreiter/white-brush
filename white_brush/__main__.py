import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    return parser.parse_args()


def main():
    args = parse_args()

    print("Input: {}, Output: {}".format(args.input_file, args.output_file))


if __name__ == "__main__":
    main()