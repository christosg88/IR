.PHONY: all index topics gen_queries queries qrels eval

all: index queries eval

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
	python3 gen_queries_titles_syn.py
	python3 gen_queries_titles_desc_syn.py
	python3 gen_queries_titles_desc_narr_syn.py
	python3 gen_queries_titles_lem.py
	python3 gen_queries_titles_lem_cat.py

queries: gen_queries
	IndriRunQuery queries/IndriRunQuery.titles > results/titles.trec
	IndriRunQuery queries/IndriRunQuery.titles-desc > results/titles-desc.trec
	IndriRunQuery queries/IndriRunQuery.titles-desc-narr > results/titles-desc-narr.trec
	IndriRunQuery queries/IndriRunQuery.titles.syn > results/titles.syn.trec
	IndriRunQuery queries/IndriRunQuery.titles-desc.syn > results/titles-desc.syn.trec
	IndriRunQuery queries/IndriRunQuery.titles-desc-narr.syn > results/titles-desc-narr.syn.trec
	IndriRunQuery queries/IndriRunQuery.titles.lem > results/titles.lem.trec
	IndriRunQuery queries/IndriRunQuery.titles.lem.cat > results/titles.lem.cat.trec

qrels:
	rm -rf qrels/qrels.adhoc
	cat qrels/qrels.* > qrels/qrels.adhoc

eval: qrels
	rm -rf evals/*.eval
	./trec_eval qrels/qrels.adhoc results/titles.trec > evals/titles.eval
	./trec_eval qrels/qrels.adhoc results/titles-desc.trec > evals/titles-desc.eval
	./trec_eval qrels/qrels.adhoc results/titles-desc-narr.trec > evals/titles-desc-narr.eval
	./trec_eval qrels/qrels.adhoc results/titles.syn.trec > evals/titles.syn.eval
	./trec_eval qrels/qrels.adhoc results/titles-desc.syn.trec > evals/titles-desc.syn.eval
	./trec_eval qrels/qrels.adhoc results/titles-desc-narr.syn.trec > evals/titles-desc-narr.syn.eval
	./trec_eval qrels/qrels.adhoc results/titles.lem.trec > evals/titles.lem.eval
	./trec_eval qrels/qrels.adhoc results/titles.lem.cat.trec > evals/titles.lem.cat.eval
