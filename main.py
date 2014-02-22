#!/usr/bin/env python
# coding: utf-8
__author__ = 'toly'
"""
    script for make per-page dictionaries according to user personal list of known words
"""

import re
import os
import sys
import argparse

from string import lower

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
stemmer = EnglishStemmer()
lemmatizer = WordNetLemmatizer()

NO_LETTER_REGEXP = re.compile(r'[^a-zA-Z]')

PERSONAL_USER_DIR = os.path.join(os.path.expanduser('~'), '.easy_english')
UNKNOWN_STEMS_FILE = 'unknown_stems.txt'
KNOWN_STEMS_FILE = 'known_stems.txt'
STUDY_DICT_FILE = 'dictionary.txt'

PERSONAL_FILES = [UNKNOWN_STEMS_FILE, KNOWN_STEMS_FILE, STUDY_DICT_FILE]
PERSONAL_FILES = map(lambda x: os.path.join(PERSONAL_USER_DIR, x), PERSONAL_FILES)
UNKNOWN_STEMS_FILE, KNOWN_STEMS_FILE, STUDY_DICT_FILE = PERSONAL_FILES


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

    # main loop-for by pages in input file
    big_page = ''
    for page_num, page in enumerate(file_pages(args.input_file)):
        big_page += page

    words = tokenizer.tokenize(big_page)
    words = map(lower, words)
    words = list(set(words))
    words = filter_non_words(words)

    tesaurus = Tesaurus()
    tesaurus.determine_words(words)


def make_arguments_parser():
    """
        make arguments parser and set options
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-i', '--input-file', type=str, required=True, help="input txt file")
    argument_parser.add_argument('-o', '--output-file', type=str, help="output file (default: <input_file>_d.txt )")
    return argument_parser


def filter_non_words(words):
    return filter(lambda x: not NO_LETTER_REGEXP.findall(x), words)


class Tesaurus(object):

    unknown_stems_file = None
    known_stems_file = None
    study_words_file = None

    unknown_stems = None
    known_stems = None
    study_words = None

    def __init__(self, unknown_stems_file=UNKNOWN_STEMS_FILE, known_stems_file=KNOWN_STEMS_FILE,
                 study_words_file=STUDY_DICT_FILE):

        self.unknown_stems_file = unknown_stems_file
        self.known_stems_file = known_stems_file
        self.study_words_file = study_words_file

        personal_files = (unknown_stems_file, known_stems_file, study_words_file)
        self.unknown_stems, self.known_stems, self.study_words = map(get_user_words, personal_files)

    def determine_words(self, words_list):
        """
            Determine words - known or unknown, and append to dictionary if need
        """
        # dict: lemma -> stem
        dict_lemmas = {}
        not_determined_words = []

        total_words = len(words_list)

        n = 0
        for word, part_of_speech in nltk.pos_tag(words_list):
            n += 1

            lemma, stemm = get_base_forms(word, part_of_speech)
            if stemm in self.known_stems or stemm in self.unknown_stems:
                continue

            not_determined_words.append(lemma)
            dict_lemmas[lemma] = stemm

            if len(not_determined_words) < 10:
                continue

            progress = 100 * float(n) / float(total_words)
            print "Progress: %d/%d [%f %%]" % (n, total_words, progress)

            known_words = input_known_words(not_determined_words)
            unknown_words = set(not_determined_words) - set(known_words)

            known_stems = map(lambda x: dict_lemmas[x], known_words)
            unknown_stems = map(lambda x: dict_lemmas[x], unknown_words)

            append_words(self.known_stems_file, known_stems)
            append_words(self.unknown_stems_file, unknown_stems)
            append_words(self.study_words_file, unknown_words)

            self.known_stems += known_stems
            self.unknown_stems += unknown_stems

            not_determined_words = []

        if not_determined_words:
            known_words = input_known_words(not_determined_words)
            unknown_words = set(not_determined_words) - set(known_words)

            known_stems = map(lambda x: dict_lemmas[x], known_words)
            unknown_stems = map(lambda x: dict_lemmas[x], unknown_words)

            append_words(self.known_stems_file, known_stems)
            append_words(self.unknown_stems_file, unknown_stems)
            append_words(self.study_words_file, unknown_words)


def append_words(filename, words):
    """
        append words to file
    """
    lines = map(lambda x: '%s\n' % x, words)
    with open(filename, 'a') as f:
        f.writelines(lines)


def get_base_forms(word, part_of_speech):
    """
        word, part_of_speech -> lemma, stemm
    """
    try:
        lemma = lemmatizer.lemmatize(word, lower(part_of_speech[0]))
    except Exception:
        lemma = lemmatizer.lemmatize(word)
    stemm = stemmer.stem(lemma)
    return lemma, stemm


def input_known_words(words):
    """
        Determine words through user input

        list of words -> [known words], [unknown words]
    """
    word_views = map(lambda item: '%d) %s' % item, enumerate(words))
    prompt = '\n'.join(word_views) + "\nWhat words are you know? "
    not_inputed = True

    while not_inputed:
        try:
            words_positions = raw_input(prompt)
            if not words_positions:
                words_positions
                break
            words_positions = map(int, words_positions.split(','))
            not_inputed = False
        except (ValueError, ):
            print "Input like a '0,3,8'"

    known_words = []
    for position in words_positions:
        try:
            known_words.append(words[position])
        except IndexError:
            pass

    return known_words


def get_user_words(filename):
    """
        get list of user words from file <filename>
            or
        create file if not exists
    """
    if not os.path.exists(filename):
        open(filename, 'a').close()
        return []

    def remove_end_of_line(line):
        if '\n' in line:
            return line.replace('\n', '')
        return line

    with open(filename, 'r') as f:
        return map(remove_end_of_line, f.readlines())


def file_lines(filename):
    """read file line by line"""
    with open(filename) as f:
        for line in f:
            yield line


def file_pages(filename, split_regexp=r'^===page #\d+$'):
    """read file page by page"""
    page = ''
    for line in file_lines(filename):
        if re.match(split_regexp, line):
            yield page
            page = ''
            continue
        page += line

    yield page


if __name__ == "__main__":
    sys.exit(main())