"""
Reddit Search Thing
Anthony Torres
torresam@umich.edu
"""
# !/usr/bin/env python3

# pip install praw --user
# pylint: disable=C0103
# https://www.reddit.com/wiki/search

from __future__ import print_function
from collections import Counter
import argparse
import sys
import praw
from prawcore import NotFound


def setup():
    """
    Parse command line arguments
    Returns parsed arguments
    """
    parser = argparse.ArgumentParser(description='Search Reddit Thing')

    parser.add_argument(
        'subreddit',
        help="Enter the name of the subreddit to search.")
    parser.add_argument(
        'query',
        help=("Enter search query. See {} for information on how to form search"
              " queries.".format("https://www.reddit.com/wiki/search")))
    parser.add_argument(
        '-p', '--print', action="store_true", default=False,
        help=("Pass this argument to print out detailed data."))
    parser.add_argument(
        '-e', '--export', action="store_true", default=False,
        help=("Pass this argument to export data."))
    parser.add_argument(
        '-t', '--title', action="store_true", default=False,
        help=("Pass this argument to include post titles in data."))
    parser.add_argument(
        '-l', '--limit', action="store", type=int, default=None,
        help=("Number of posts to grab. Default is as many as possible."))
    return parser.parse_args()


def sub_exists(reddit, sub):
    """
    Check if the subreddit exists
    ARGS:
        reddit: reddit object from PRAW
        sub: subreddit name from commandline
    """

    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        print("Error: {} is not a valid subreddit name.".format(sub))
        sys.exit()


def print_details(primaryFlairs, secondaryFlairs):
    """
    Print flair details
    ARGS:
        primaryFlairs: list of primary flairs
        secondaryFlairs: list of secondary flairs
    FORMAT:
        FlairName, CountNumber
    """

    print("Primary flairs:")
    for flair in primaryFlairs.most_common():
        print("{}, {}".format(flair[0], flair[1]))

    print("\nSecondary flairs:")
    for flair in secondaryFlairs.most_common():
        print("{}, {}".format(flair[0], flair[1]))


def print_titles(titles):
    """
    Print post titles that were found and what flair posted the title
    ARGS:
        titles: list of post titles with primary and secondary flairs
    """
    print("\"Post Title\", Primary Flair, Secondary Flair")
    print("-----------------------------------------------")
    for t in titles:
        print("{}, {}, {}".format(t[0], t[1], t[2]))
    print('\n')

def export_data():
    return 0


def main():
    """ MAIN """

    arg = setup()

    reddit = praw.Reddit()

    sub_exists(reddit, arg.subreddit)

    subreddit = reddit.subreddit(arg.subreddit)

    primaryFlairs = Counter()
    secondaryFlairs = Counter()
    titles = []
    numberResults = 0

    for submission in subreddit.search(arg.query, sort='new', limit=arg.limit):
        # Split flair in to primary and secondary flair
        # On /r/CFB they are separated by a /
        # Some flairs contain /r/ so use ' / '
        formattedFlair = str(submission.author_flair_text).split(' / ', 1)
        formattedTitle = "\"{}\"".format(submission.title)

        titles.append([formattedTitle, formattedFlair[0], formattedFlair[-1]])

        primaryFlairs[formattedFlair[0]] += 1

        if len(formattedFlair) == 2:
            secondaryFlairs[formattedFlair[-1]] += 1


        numberResults += 1

    print("Number of results: {}\n".format(numberResults))

    if arg.title:
        print_titles(titles)

    if arg.print:
        print_details(primaryFlairs, secondaryFlairs)
    
    if arg.export:
        export_data()


if __name__ == '__main__':
    main()
