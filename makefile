.PHONY: run


run:
	@echo "" > $(spider).log
	@echo "" > $(spider).csv
	@scrapy crawl $(spider) --logfile $(spider).log -o $(spider).csv

json:
	@echo "" > $(spider).log
	@echo "" > $(spider).json
	@scrapy crawl $(spider) --logfile $(spider).log -o $(spider).json


gen:
	@scrapy genspider $(spider) $(spider).$(name)  