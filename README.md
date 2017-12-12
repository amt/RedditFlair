### Reddit Thing
* Search a subreddit for a post based on a query.
* Return information about the flairs of the post authors.

### Installation
```
Uses python 3.6
1. Head over to https://www.reddit.com/prefs/apps and get CLIENT_ID and CLIENT_SECRET
2. Put the CLIENT_ID and CLIENT_SECRET in their respective fields in the praw.ini file
3. pip install praw --user
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
  -e, --export  Pass this argument to export data.
```

### Examples
