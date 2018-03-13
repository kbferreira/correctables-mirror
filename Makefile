
LATEXMK      = latexmk -f
LATEXMKFLAGS = -pdf -g
LATEXMKCLEAN = -C
export TEXINPUTS:=./include:${TEXINPUTS}
export BSTINPUTS:=./include:${BSTINPUTS}

SOURCES      = paper.tex
PDF	     = $(SOURCES:.tex=.pdf)
BASE         = $(SOURCES:.tex=)

TEXSRC       = $(filter-out $(SOURCES), $(shell ls *.tex))

BIBSRC       = $(shell ls *.bib)
BBL          = $(notdir $(BIBSRC:.bib=.bbl))

FIGS         = $(shell ls figs/*.eps figs/*.pdf)

DEPS         = $(DEP) $(TEXSRC) $(BIBSRC) $(FIGS) all.bib

all: plots $(PDF)

plots:
	${MAKE} -C plot	

$(PDF): %.pdf : %.tex $(DEPS)
	$(LATEXMK) $(LATEXMKFLAGS) $<
	$(LATEXMK) $(LATEXMKFLAGS) $<

$(BBL): $(BIBSRC)
	bibtex $(BASE)

all.bib : $(filter-out all.bib, $(BIBSRC))
	-rm all.bib
	bibtool -s -d -- check.double.delete=on -- preserve.key.case=on $(filter-out all.bib, $(BIBSRC)) > all.bib
	emacs --batch all.bib -l untabify.el -f save-buffer

view:	all
	$(LATEXMK) -pvc -view=ps -r latexmkrc paper

clean:
	-$(LATEXMK) $(LATEXMKCLEAN)
	${MAKE} -C plot clean
	-rm -f *~
	-rm -f *.bak
	-rm -f all.bib
	-rm -f *.bbl
