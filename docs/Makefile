# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = $(DATADIR)/Projects.ghpg/AI_daily_precip.ghpg

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/html/* $(BUILDDIR)/html/.buildinfo $(BUILDDIR)/doctrees

.PHONY: html
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

