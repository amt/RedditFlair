"""
Reddit Flair Analyzer
Anthony Torres
torresam@umich.edu
"""
# !/usr/bin/env python3

from collections import Counter
import argparse
import sys
import praw
from prawcore import NotFound
import matplotlib.pyplot as plt
import numpy
import pandas


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
        '-t', '--title', action="store_true", default=False,
        help=("Pass this argument to include post titles in data."))
    parser.add_argument(
        '-l', '--limit', action="store", type=int, default=None,
        metavar='AMOUNT',
        help=("Number of posts to grab. Default is as many as possible."))
    parser.add_argument(
        '-e', '--export', action="store", type=str, default=None,
        metavar='FILENAME',
        help=("Filename to export data to."))
    parser.add_argument(
        '-g', '--graph', action="store", type=str,
        metavar='FILENAME',
        help=("Export a graph of the data.")
    )
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
    print("---------------")
    for flair in primaryFlairs.most_common():
        print("{}, {}".format(flair[0], flair[1]))

    print("\nSecondary flairs:")
    print("-----------------")
    for flair in secondaryFlairs.most_common():
        print("{}, {}".format(flair[0], flair[1]))


def print_titles(titles):
    """
    Print post titles that were found and what flair posted the title
    ARGS:
        titles: list of post titles with primary and secondary flairs
    """
    print("\"Post Title\", Primary Flair, Secondary Flair")
    print("--------------------------------------------")
    for t in titles:
        print("{}, {}, {}".format(t[0], t[1], t[2]))
    print('\n')


def export_data(numberResults, titles, primaryFlairs, secondaryFlairs, args):
    """
    Print data to filename
    ARGS:
        numberResults: total number of posts
        titles: list of titles
        primaryFlairs: list of primaryFlairs
        secondaryFlairs: list of secondaryFlairs
        args: args from command line to check filename and what data to output
    """
    stdout = sys.stdout

    f = open(args.export, 'w')
    sys.stdout = f

    print("Number of results: {}\n".format(numberResults))

    if args.title:
        print_titles(titles)

    print_details(primaryFlairs, secondaryFlairs)

    sys.stdout = stdout
    f.close()


def make_graph(primaryFlairs, filename):
    """
    Make a visual graph of the primary flair data.
    ARGS:
        primaryFlairs: list of primaryFlairs
        filename: name of output file from command line args
    """
    keys, counts = zip(*primaryFlairs.most_common())
    y_pos = numpy.arange(len(keys))
    plt.figure(figsize=(20,10))
    plt.barh(y_pos, counts, height=0.5)
    plt.yticks(y_pos, keys)
    plt.xlabel('Flair Count')
    plt.title('FLAIRS OF REDDIT USERS')
    plt.savefig(filename, bbox_inches='tight', dpi=100)


def main():
    """ MAIN """

    args = setup()

    reddit = praw.Reddit()

    sub_exists(reddit, args.subreddit)

    subreddit = reddit.subreddit(args.subreddit)

    primaryFlairs = Counter()
    secondaryFlairs = Counter()
    titles = []
    numberResults = 0

    for submission in subreddit.search(args.query, sort='new', limit=args.limit):
        # Split flair in to primary and secondary flair
        # On /r/CFB they are separated by a •
        # Example flair text:
        # ':centralmichigan: :michigan: Central Michigan • Michigan'
        formattedFlair = str(submission.author_flair_text).split(': ')[-1]
        formattedFlair = formattedFlair.split(' • ')
        formattedTitle = "\"{}\"".format(submission.title)

        titles.append([formattedTitle, formattedFlair[0], formattedFlair[-1]])

        primaryFlairs[formattedFlair[0]] += 1

        if len(formattedFlair) == 2:
            secondaryFlairs[formattedFlair[-1]] += 1


        numberResults += 1

    print("Number of results: {}".format(numberResults))

    if args.title:
        print_titles(titles)

    if args.print:
        print_details(primaryFlairs, secondaryFlairs)

    if args.export:
        export_data(numberResults, titles, primaryFlairs, secondaryFlairs, args)

    if args.graph:
        make_graph(primaryFlairs, args.graph)


if __name__ == '__main__':
    main()
