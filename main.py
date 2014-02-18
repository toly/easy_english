#!/usr/bin/env python
# coding: utf-8
__author__ = 'toly'
"""
    script for make per-page dictionaries according to user personal list of known words
"""

import os
import sys
import argparse

PERSONAL_USER_DIR = os.path.join(os.path.expanduser('~'), '.easy_english')
KNOWN_WORDS_FILE = 'known_words.txt'
UNKNOWN_WORDS_FILE = 'unknown_words.txt'
BAD_WORDS_FILE = 'bad_words.txt'

PERSONAL_FILES = [KNOWN_WORDS_FILE, UNKNOWN_WORDS_FILE, BAD_WORDS_FILE]
PERSONAL_FILES = map(lambda x: os.path.join(PERSONAL_USER_DIR, x), PERSONAL_FILES)
KNOWN_WORDS_FILE, UNKNOWN_WORDS_FILE, BAD_WORDS_FILE = PERSONAL_FILES


def main():
    """
        main func - entry point
    """
    # if not created - make work directory for personal user lists of words
    if not os.path.exists(PERSONAL_USER_DIR):
        os.mkdir(PERSONAL_USER_DIR)

    # make arguments parser and parse arguments
    arg_parser = make_arguments_parser()
    args = arg_parser.parse_args()

    # load lists of known words and "bad" (like "the", "a", etc) words
    known_words, unknown_words, bad_words = map(get_user_words, PERSONAL_FILES)

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


def get_user_words(filename):
    """
        get list of user words from file <filename>
            or
        create file if not exists
    """
    if not os.path.exists(filename):
        open(filename, 'a').close()
        return []

    with open(filename, 'r') as f:
        return f.readlines()


if __name__ == "__main__":
    sys.exit(main())