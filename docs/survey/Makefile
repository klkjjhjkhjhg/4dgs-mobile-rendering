# Makefile for 综述 LaTeX 文档
# 用法: make        # 编译 survey.pdf
#       make clean  # 清理临时文件 (保留 survey.pdf)
#       make distclean  # 清理所有 (含 survey.pdf)
#       make view   # 用 Preview.app 打开 PDF (macOS)

LATEXMK = latexmk
LATEXMK_FLAGS = -pdf -xelatex -interaction=nonstopmode
TARGET = survey.pdf
SOURCES = survey.tex survey.bib sections/*.tex

.PHONY: all clean distclean view

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(LATEXMK) $(LATEXMK_FLAGS) survey.tex

clean:
	$(LATEXMK) -c

distclean:
	$(LATEXMK) -C

view: $(TARGET)
	open -a Preview $(TARGET)
