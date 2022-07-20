
# Overview

1. _FantasyService_ contains resources implementing a simple
[fantasy baseball](https://en.wikipedia.org/wiki/Fantasy_baseball) league.
2. _LahmanService_ contains resources for querying information from the Lahman's 
Baseball Database.
3. _LikesFollows_ contains resources for implementing a simple network of people who "like"
or "follow" other fantasy baseball participants, as well as fantasy and real world
teams and players.

   

# Services

## DataServices

This package contains libraries for read, querying and writing to various databases, including:
- RDBDataTable.py provides functions for accessing MySQL.
- MongoDBTable (in progress) provides functions for accessing MongoDB.
- Neo4jDataTable provides functions for Neo4j.



BaseDataTable.py is an abstract class that defines a logical interface.


## LahmanService

This package contains classes that provide access to individual tables in Lahman's Baseball Database by
using RDBDataTable.

## FantasyService

This package contains classes that provide access to individual tables in the fantasy baseball DB by
using RDBDataTable/Neo4JDataTable.

## CommentLikeService

This package contains classes that implement the commenting, liking, following, etc. functions.

# unit_tests

This package contains files that do unit test for various services and classes.





