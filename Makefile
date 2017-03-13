.PHONY: all index topics gen_queries queries qrels eval

all: index queries qrels

index:
	IndriBuildIndex IndriBuildIndex.param

topics:
	rm -rf topics/topics.trec
	cat topics/topics.* > topics/topics.trec

gen_queries: topics
	rm -rf queries/*
	python3 gen_queries_titles.py
	python3 gen_queries_titles_desc.py
	python3 gen_queries_titles_desc_narr.py

queries: gen_queries
	IndriRunQuery queries/IndriRunQuery.titles > results/titles.trec
	IndriRunQuery queries/IndriRunQuery.titles-desc > results/titles-desc.trec
	IndriRunQuery queries/IndriRunQuery.titles-desc-narr > results/titles-desc-narr.trec

qrels:
	rm -rf qrels/qrels.adhoc
	cat qrels/qrels.* > qrels/qrels.adhoc

eval: qrels
	rm -rf evals/*.eval
	./trec_eval qrels/qrels.adhoc results/titles.trec > evals/titles.eval
	./trec_eval qrels/qrels.adhoc results/titles-desc.trec > evals/titles-desc.eval
	./trec_eval qrels/qrels.adhoc results/titles-desc-narr.trec > evals/titles-desc-narr.eval
