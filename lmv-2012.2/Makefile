.PHONY: clean verylcean

all: antraege/all-meta.tex
	xelatex antragsbuch
	xelatex antragsbuch
	./splitindex.pl antragsbuch -- -s indices.ist
	xelatex antragsbuch
	xelatex antragsbuch

antraege/all-meta.tex:
	cd antraege ; ./getantraege.py

clean:
	@-rm -fv *.out *.toc *.aux *.log *.ilg *.ind *.idx

veryclean: clean
	@-rm -fv antraege/*.tex antraege/*.textile antragsbuch.pdf
