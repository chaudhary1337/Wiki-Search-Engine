# Wiki-Search-Engine

## The Idea
Create a search engine from scratch.

## Indexer
Run: `bash index.sh ./path/to/wikidump /tmp/indices && cat stats.txt`.

### `indexer.py`

We start from `indexer.py` file. 

We use the sax parser since it allows us to go over the pages of the dump one-by-one, which is *very* helpful for larger `xml` files.


### `handle.py`

The `ContentHandler` is present in `handle.py` which parses the file by finding the appropriate tags.

We keep on `title` and `text` information to the page. Rest is ignored.

For a `endElement()` which is page, a `save_page()` function is triggered, which saves the page.

Every `help.PRINT_LIMIT` pages, a log is printed saying how much time has been taken to parse the pages.

How does the saving happen then?

### `page.py`

`save_page()` does two big things. First, it saves the title of the page without any processing (except lowercasing). Second, it creates an inverted index in the following format:

`self.inverted_index[word][page_id] = [tf+field_id]`

`word` is the set of words encountered after page extraction (check the next section).

`page_id` is the unique index given to each (its just a counter of the number of pages).

`tf` is the term frequency of the given word, in the given page in the corresponding `field_id`. 

Meaning, the word, `word` occurs with a frequency of `tf` in the field `field_id` in the page `page_id`. This is information that we get out of the `extract.py` file.

Note that we do not store `page_id`s directly as integers - we first encode them to hexadecimal using `help.enc()`.

Now, a special thing happens when the `page_id` exceeds the `help.DUMP_LIMIT`. As you can guess, we have to use the `save_pages()` function to save all the information of inverted index up till now. That is, it auto-initiates a save for the previous `help.DUMP_LIMIT` pages. *It is also triggered when the last element, `mediawiki` is reached!*

### `extract.py`

I spent most of my time trying to parse these pages, sometimes to success and mostly to slow failures. The `extract()` function extracts the field elements into the `self.extracted_page` variable, which is flushed (reset) after every page.

There is no point going in details about the extraction process, since at this point, it is either:
1. Self explanatory
2. I don't care anymore

## Searcher
Run: `bash search.sh && cat queries_op.txt`.


### `searcher.py`

The `/src/searcher.py` is the "main" indexer file that runs everything else.

### `extract.py`

The function `extract()` returns a dictionary with keys as the fields and values as string of all the tokens of that field.

### `parse.py`

This file provides helper functions that deal with reading information from the merged indices. We use `get_tf_bonus()` which gets us both the term frequencies and the bonus scoring multiplier. This multiplier is used to weigh the fields and rank the documents.

### `handle.py`

This is where we do the primary computations. Using the help of `parser.py`'s functions, we get the line of documents associated with a token and then extract out all the documents which satisfy the field conditions. Scores are thus assigned to all the documents for a given token.

Now, a `Counter` of all the information of the tokens is created, to add up all the rankings of each token - giving us the final `query_counter`. We then find the `topk` elements and print out the titles out to a file (specified in the shell input line).

## Conclusion

This project was long, cumbersome and tiring.

The entire code base of ~869 lines represents a single idea: the inverted index.

It takes 9 hours, 17 minutes and 33 seconds to index on ada with 15 CPUs. (Thanks Shivansh S. for running!) To merge the files, it takes 13 minutes and 54 seconds on my VM (6 CPUs Ryzen 5 4th gen).

So, 9 hours and 30 minutes approximately to index and merge.

And, 21 GB (exact) space, lesser than 1/4th.


But, all in all, worth it. 

I had never created a search engine before and this was a fun learning experience.
