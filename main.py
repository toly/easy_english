# coding: utf-8
__author__ = 'toly'
"""
    script for make per-page dictionaries according to user personal list of known words
"""

import sys
import argparse


def main():
    """
        main func - entry point
    """
    # make arguments parser and parse arguments
    arg_parser = make_arguments_parser()
    args = arg_parser.parse_args()

    # if not created - make work directory for personal user lists of words

    # load lists of known words and "bad" (like "the", "a", etc) words

    # main loop-for by pages in input file

        # loop-for by words in current page

            # get lemmatized word

            # if in known or "bad" word - continue

            # ask user about word - to known, to unknown or to "bad"
            # process answer

    # output result file


def make_arguments_parser():
    """
        make arguments parser and set options
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-i', '--input-file', type=str, required=True, help="input txt file")
    argument_parser.add_argument('-o', '--output-file', type=str, help="output file (default: <input_file>_d.txt )")
    return argument_parser


if __name__ == "__main__":
    sys.exit(main())