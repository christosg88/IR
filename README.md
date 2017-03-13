# IR
Project in Information Retrieval

Auto
---
1. Put the files for indexing under the folder corpora. The files can be under their own subdirectories.
2. Run `make all`.

Manual
---
1. Put the files for indexing under the folder corpora. The files can be under their own subdirectories.
2. Run `make index` to create the index of the corpora. The index will be placed in `/index`.
3. Run `make topics` to concatenate all the topics under `/topics` to a single file. The topics file will be placed in `/topics`.
4. Run `make gen_queries` to create the respective queries from the topics. The queries will be placed in `/queries`.
5. Run `make queries` to run the queries with `IndriRunQuery`. The results of the runs will be placed under `/results`.
6. Run `make qrels` to concatenate all the qrels under `/qrels` to a single file. The qrels file will be placed in `/qrels`.
7. Run `make eval` to compare your results with the given qrels. The evaluation reports will be placed under `/evals`.
