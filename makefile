
file_name = handyman-20.csv

run:
	echo "" > yellow.log && scrapy crawl yellowpages --logfile yellow.log -o $(file_name) 