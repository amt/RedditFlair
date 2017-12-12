"""
Reddit Search Thing
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

    primaryFlairs = Counter(primaryFlairs)
    secondaryFlairs = Counter(secondaryFlairs)

    print("Primary flairs:")
    for flair in primaryFlairs.most_common():
        print("{}, {}".format(flair[0], flair[1]))

    print("\nSecondary flairs:")
    for flair in secondaryFlairs.most_common():
        print("{}, {}".format(flair[0], flair[1]))

def main():
    """ MAIN """

    parser = argparse.ArgumentParser(description='Search Reddit Thing')

    parser.add_argument(
        'subreddit',
        help="Enter the name of the subreddit to search.")
    parser.add_argument(
        'query',
        help=("Enter search query. See {} for information on how to form search queries.".format("https://www.reddit.com/wiki/search")))
    parser.add_argument('-p', '--print', action="store_true", default=False,
                        help=("Pass this argument to print out detailed data."))
    parser.add_argument('-e', '--export', action="store_true", default=False,
                        help=("Pass this argument to export data."))

    arg = parser.parse_args()

    reddit = praw.Reddit()

    sub_exists(reddit, arg.subreddit)

    subreddit = reddit.subreddit(arg.subreddit)

    primaryFlairs = []
    secondaryFlairs = []
    numberResults = 0

    for submission in subreddit.search(arg.query):
        # Split flair in to primary and secondary flair
        # On /r/CFB they are separated by a /
        # Some flairs contain /r/ so use ' / '
        formattedFlair = str(submission.author_flair_text).split(' / ', 1)

        primaryFlairs.append(formattedFlair[0].strip())
        secondaryFlairs.append(formattedFlair[-1].strip())

        numberResults += 1

    print("\nNumber of results: {}\n".format(numberResults))

    if arg.print:
        print_details(primaryFlairs, secondaryFlairs)

if __name__ == '__main__':
    main()
