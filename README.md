### Reddit Flair Analyzer
* Search a subreddit for a post based on a query.
* Return information about the flairs of the post authors.

### Installation
```
Uses Python 3.5.2+
1. Head over to https://www.reddit.com/prefs/apps and get CLIENT_ID and CLIENT_SECRET
2. Put the CLIENT_ID and CLIENT_SECRET in their respective fields in the praw.ini file
3. pip install -r requirements.txt
```
### Usage
```
usage: main.py <subreddit> <query> [options]

positional arguments:
  subreddit     Enter the name of the subreddit to search.
  query         Enter search query. See https://www.reddit.com/wiki/search for
                information on how to form search queries.

optional arguments:
  -h, --help    show this help message and exit
  -p, --print   Pass this argument to print out detailed data.
  -t, --title   Pass this argument to include post titles in data.
  -l AMOUNT, --limit AMOUNT
                Number of posts to grab. Default is as many as
                possible.
  -e FILENAME, --export FILENAME
                Filename to export data to.
  -g FILENAME, --graph FILENAME
                Export a graph of the data.
```

### Examples
![alt-text](https://i.imgur.com/iVHx6Lw.png)
