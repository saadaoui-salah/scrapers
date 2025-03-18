.PHONY: run


run:
	@echo "" > $(spider).log
	@echo "" > $(spider).json
	@scrapy crawl $(spider) --logfile $(spider).log -o $(spider).json

gen:
	@scrapy genspider $(spider) $(spider).$(name)  