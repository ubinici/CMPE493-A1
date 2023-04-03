# CMPE 493 - Assignment 1 Report

***Before running the script, see: [`README`](README.txt)***

## Data Preprocessing and Indexing

While preprocessing the given data, `tokenize()` function was defined in order to convert the raw text into a list of tokens. To carry out this process in an efficient way and store a cleaner data to work with later on, the raw text was case-folded and cleansed from the punctuations. Additionally, the stopwords were also filtered out in order to speed up indexing and query operations.

Here is a rundown of the change in the amount of terms and tokens before and after running the `tokenize()` function:

| | Before | After |
| :-: | :-: | :-: |
| **Token count** | 2586293 | 1557782 |
| **Term count** | 112357 | 47325 |

You may also find the top 100 most frequent words [at the end of the report](#top-100-words).

After preprocessing, `index_doc()` and `build_index()` functions were defined in order to iterate through the `.sgm` files, compile the document IDs and the relevant text respectively and store them alongside one another. These functions also carry out the necessary operations in order to flesh out a positional index for the tokens along with the document IDs of the respective document they belong to.

## Inverted index

As a result, an inverted index was created to store each token with the IDs of the respective document they were found in, as well as the positions they are found among other tokens found within the same document. To exemplify the way they are stored, here is a sample unit within the inverted index:

```json
"tunnel": {         # Token
    "2430": [       # ID of the document that the token was found in
        7           # Position of the token
    ],
    "3568": [       # Document ID
        52          # Position
    ],
    "5526": [       # Document ID
        14          # Position
    ],
    ...
},
```

As can be seen here, the inverted index was constructed via a dictionary (hash-table), where keys are the unique terms (tokens) found in the text and the values are postings lists associated with each term. The dictionary offers constant-time (O(1)) average-case complexity for insertion, deletion, and search operations, making it efficient for managing the inverted index.

As for the postings lists, they are represented by simple Python lists, which are convenient thanks to their dynamic nature as arrays able to grow and shrink where needed.  They provide O(1) complexity for accessing elements at specific indices and O(n) complexity for inserting or deleting elements in the middle of the list. In the context of an inverted index, the use of lists for postings is a reasonable choice, as the primary operations involve appending new document IDs and positions, which can be performed efficiently.

## Screen capture

### `indexer` running

![Indexer running](https://zeu.s-ul.eu/jeuKYXvN.png "Screenshot while indexer is running on VSCode Interactive Window")

### `query_processor` running

![Processor running](https://zeu.s-ul.eu/hDUMjVo9.png "Screenshot while query processor is running on VSCode Interactive Window")

## Top 100 words

```
said: 52901
mln: 25513
dlrs: 20527
reuter: 18915
pct: 17013
vs: 14586
year: 10312
billion: 10210
would: 9171
cts: 8846
us: 8772
company: 8215
bank: 6631
inc: 6442
new: 6421
net: 6057
last: 5862
corp: 5582
market: 5382
stock: 5177
also: 5173
one: 5010
loss: 4988
shares: 4961
share: 4573
two: 4275
trade: 4274
shr: 4083
co: 3786
sales: 3727
may: 3721
oil: 3681
first: 3609
april: 3544
banks: 3515
government: 3449
debt: 3437
exchange: 3356
march: 3253
profit: 3109
per: 3076
prices: 3075
price: 3019
told: 2907
group: 2900
interest: 2861
foreign: 2850
international: 2820
years: 2809
agreement: 2778
could: 2754
rate: 2753
dlr: 2749
ltd: 2722
three: 2681
tonnes: 2672
securities: 2650
quarter: 2564
expected: 2523
president: 2453
week: 2445
february: 2372
revs: 2367
due: 2358
total: 2319
five: 2312
tax: 2281
today: 2268
common: 2247
japan: 2227
offer: 2216
dollar: 2195
added: 2182
economic: 2157
financial: 2156
production: 2108
january: 2091
rates: 2089
rose: 2069
trading: 2069
board: 2069
month: 2056
increase: 2045
meeting: 2011
japanese: 2001
officials: 1997
current: 1989
spokesman: 1978
capital: 1953
months: 1912
made: 1901
record: 1874
world: 1870
issue: 1866
earlier: 1863
major: 1843
industry: 1822
markets: 1812
business: 1811
system: 1809
```
