.PHONY: run


run:
	@echo "" > $(spider).log
	@echo "" > $(spider).csv
	@scrapy crawl $(spider) --logfile $(spider).log -o $(spider).csv

gen:
	@scrapy genspider $(spider) $(spider).$(name)  