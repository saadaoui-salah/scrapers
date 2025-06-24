#!/bin/bash

# Activate the virtual environment
source ~/scrappers/env/bin/activate

# Navigate to the Scrapy project directory
cd ~/scrappers

# Run the spider
echo '' > suruga-ya.log
scrapy crawl suruga-ya --logfile suruga-ya.log