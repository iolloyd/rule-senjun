# Outfit engine

Lightweight rules engine for matching items based on their tagged attributes.

## The Why

Manually matching items with other items is fine when you just have to manage a
small amount, but as that list grows, there are better things you could be
using your time for.

## The How

I started writing this in php, then switched to python after finding a great
library called bitmapist for handling bitstrings in redis. However, early on I realised
another way to store combinations, so stayed with python anyway. It's backed by the wonderful redis.

## The Next

TODO Provide an easy way to interface with popular relational databases,
starting with MySql.




