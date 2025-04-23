"""
Author: Colin Rindge
"""
import argparse
from dataclasses import dataclass
import sys

import matplotlib.pyplot as plt

import util

START_SYMBOL = "ϕ"


def arg_parse_init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="The data directory to process")
    parser.add_argument("--mostCommon", type=int, help="Shows the X most common N-Grams for all shows")
    parser.add_argument("--frequency", type=str, nargs='+',
                        help="Calculates the frequency of the  n-gram(s) for each transcript.")
    parser.add_argument("-w", "--write", action="store_true", help="Writes values to the terminal")
    parser.add_argument('-p', '--plot', action='store_true', help='Creates a plot for the corresponding query')
    parser.add_argument('-n', type=int, help='Specify the number of words that make up an N - gram')
    args = parser.parse_args()
    if args.dir is not None and args.dir[-1] != "/":
        args.dir += "/"

    return args

@dataclass
class Podcast:
    date: str
    word_frequency: dict


def ngram_dictionary_1_most_common(files: list[str]) -> dict:
    """
    Creates n-grams of size 1 from files
    :param files: List of all text files
    :return: dict of word rarity
    """
    words = {}
    for file in files:
        with open(file, encoding='UTF-8') as f:
            for line in f:
                    line = line.split()
                    for word in line:
                        word = util.clean_string(word).lower()
                        if word in words:
                           words[word] += 1
                        else:
                            words[word] = 1
    return words

def ngram_dictionary_2_most_common(files: list[str], n: int) -> dict:
    """
    Creates n-grams of size 2 or more from files
    :param files: list of all text files
    :param n: n-gram size
    :return: dict of n-gram frequencies
    """
    ngrams = {}
    for file in files:
        with open(file, encoding='UTF-8') as f:
            for line in f:
                line = line.split()
                i = 0
                k = n
                line.insert(0, START_SYMBOL)
                while i < len(line):
                    if len(line) > 1:
                        ngram = ''
                        if len(line) < n:
                            k = len(line)
                        for v in range(i, k):
                            line[v] = util.clean_string(line[v]).lower()
                            ngram += line[v] + ' '
                        ngram = ngram.strip(' ')
                        if ngram in ngrams:
                            ngrams[ngram] += 1
                        else:
                            ngrams[ngram] = 1
                    i += 1
                    if k < len(line):
                        k += 1
    return ngrams

def most_common(total_frequencies: dict, num: int, n: int, write: bool, plot: bool):
    """
    Writes and/or plots a list of the num most common words
    :param total_frequencies: list of all word frequencies
    :param num: number of words to print
    :param n: length of n-grams
    :param write: if true, print top num n-grams
    :param plot: if true, plot n-grams
    :return: None
    """
    words = []
    frequencies = []
    i = 0
    if write:
        print('Top', num, str(n)+'-grams: ')
    for word in sorted(total_frequencies, key=total_frequencies.get, reverse=True):
        if i >= num:
            pass
        else:
            if write:
                print(str(i+1) + ': ' + word + ', ' + str(total_frequencies[word]))
            words.append(word)
            frequencies.append(total_frequencies[word])
            i += 1
    if plot:
        plt.bar(words, frequencies)
        plt.xlabel(str(n) + '-gram')
        plt.ylabel('Count')
        plt.title(str(n) + '-gram Ranking')
        plt.show()


def ngram_dictionary_1_frequency(file: str) -> Podcast:
    """
    Creates n-grams of size 1 from files
    :param file: Text file
    :return: dict of word rarity
    """
    words = {}
    with open(file, encoding='UTF-8') as f:
        for line in f:
                line = line.split()
                for word in line:
                    word = util.clean_string(word).lower()
                    if word in words:
                       words[word] += 1
                    else:
                        words[word] = 1
    return Podcast(file[len(file)-12:len(file)], words)

def ngram_dictionary_2_frequency(file: str, n: int) -> Podcast:
    """
    Creates n-grams of size 2 or more from files
    :param file: Text file
    :param n: n-gram size
    :return: dict of n-gram frequencies
    """
    ngrams = {}
    with open(file, encoding='UTF-8') as f:
        for line in f:
            line = line.split()
            i = 0
            k = n
            line.insert(0, START_SYMBOL)
            while i < len(line):
                if len(line) > 1:
                    ngram = ''
                    if len(line) < n:
                        k = len(line)
                    for v in range(i, k):
                        line[v] = util.clean_string(line[v]).lower()
                        ngram += line[v] + ' '
                    ngram = ngram.strip(' ')
                    if ngram in ngrams:
                        ngrams[ngram] += 1
                    else:
                        ngrams[ngram] = 1
                i += 1
                if k < len(line):
                    k += 1
    return Podcast(file[len(file) - 12:len(file)], ngrams)

def sort_by_date(podcasts: list[Podcast]) -> list[Podcast]:
    """
    Quick sorts a list of Podcast dataclasses by date
    :param podcasts: list of Podcast dataclasses
    :return: Podcast dataclasses sorted by date
    """
    if len(podcasts) == 0:
        return []
    else:
        pivot = podcasts[0].date
        less, equal, greater = [], [], []
        for podcast in podcasts:
            if podcast.date < pivot:
                less.append(podcast)
            elif podcast.date == pivot:
                equal.append(podcast)
            else:
                greater.append(podcast)
        return sort_by_date(less) + equal + sort_by_date(greater)

def frequency(podcasts: list[Podcast], word: str, write: bool, plot: bool):
    if write:
        print(word + ':')
    x_coords = []
    y_coords = []
    for podcast in podcasts:
        word_frequency = 0
        if word in podcast.word_frequency:
            word_frequency = podcast.word_frequency[word]
        x_coords.append(util.convert_to_date(podcast.date))
        y_coords.append(word_frequency)
        if write:
            better_date = str(util.convert_to_date(podcast.date))[:11]
            better_date = better_date[5:7] + '/' + better_date[8:10] + '/' + better_date[:4]
            print(better_date + ':', word_frequency)
    if plot:
       plt.plot(x_coords, y_coords, label=word)

def main():
    args = arg_parse_init()
    if args.n is None or args.n <= 0:
        print("N must be greater than 0", file=sys.stderr)
        sys.exit()
    if args.mostCommon is not None and args.mostCommon <= 0:
        print("X should be greater than 0", file=sys.stderr)
        sys.exit()
    if not args.frequency and not most_common:
        print("List should not be empty", file=sys.stderr)
        sys.exit()
    all_txts = util.get_all_text_files_in_dir(args.dir)
    if not all_txts:
        print("DIR must contain at least one .txt file or contain a subdirectory that does.", file=sys.stderr)
        sys.exit()
    if args.mostCommon:
        if args.n == 1:
            full_dict = ngram_dictionary_1_most_common(all_txts)
        else:
            full_dict = ngram_dictionary_2_most_common(all_txts, args.n)
        if args.write or args.plot:
            most_common(full_dict, args.mostCommon, args.n, args.write, args.plot)
    if args.frequency:
        podcasts = []
        if args.n == 1:
            for file in all_txts:
                podcasts.append(ngram_dictionary_1_frequency(file))
        else:
            for file in all_txts:
                podcasts.append(ngram_dictionary_2_frequency(file, args.n))
        podcasts = sort_by_date(podcasts)
        if args.write or args.plot:
            for word in args.frequency:
                frequency(podcasts, word, args.write, args.plot)
            if args.plot:
                plt.xlabel('Date')
                plt.ylabel('Count')
                plt.legend(loc="upper left")
                plt.title(str(args.n) + '-gram Frequency')
                plt.show()

if __name__ == "__main__":
    main()