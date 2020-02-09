# JPG Scrapper 

## Description  
A simple python3 script to parse an html page, and pull in jpg files from pages names aboutSomeShow and coverSomeShow.jpg, and sort them into SomeShow

## Requirements
> - python3
> - BeautifulSoup4 python library

## Installation

Simply install BeautifulSoup4 via your OS's package manager. If its not available, then use `pip3 install BeautifulSoup`. All other libraries are included in a standard python3 install.

## Usage

> `python3 scraper.py -f <site fdqn> -p <page to walk>`   
> Output will bin in the directory backups. 