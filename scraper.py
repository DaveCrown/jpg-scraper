#! /usr/bin/env python3
import sys
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os

import argparse

ignore_files=('patchstrip.jpg',)

parser = argparse.ArgumentParser(description='Scraps a host and page for JPG files')
parser.add_argument('-f','--fdqn', help="Base Directory Location of YAMLs",required=True, action="store", dest="fdqn") 
parser.add_argument('-p','--top-page', help='Data Center Name',required=True, action="store", dest="top_page") 
args = parser.parse_args()

fdqn = args.fdqn
top_page = args.top_page
top_directory = "backups"


top_url = "http://{}/{}".format(fdqn,top_page)
response = requests.get(top_url)
if response.status_code != 200:
  print("HTTP get for {} failed with error {}".format(top_url,response.status_code))
  print("Chucking a rod and bailing")
  sys.exit()

if not os.path.exists(top_directory):
  os.mkdir(top_directory)

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all('a')
for link in links:
    if ('href' in link.attrs) and ('about' in link['href']) and ('.html' in link['href']):
        show = link['href']
        show = show.replace('about','')
        show = show.replace('.html','')
        print("Parsing URL {} for show {}".format(link['href'],show) )
        page_url = "http://{}/{}".format(fdqn,link['href'])
        page_get = requests.get(page_url)
        page_soup = BeautifulSoup(page_get.text, "html.parser")
        elements = page_soup.find_all('div')
        show_dir = "{}/{}".format(top_directory,show)
        if not os.path.exists(show_dir):
            os.mkdir(show_dir)
        index = 0
        for element in elements:

          file_name = None
          try:
            if ('href' in element.contents[0].attrs) and ('jpg' in element.contents[0]['href']):
              file_name = element.contents[0]['href']
          except:
            pass
          
          try: 
            if ('src' in element.contents[0].attrs) and ('jpg' in element.contents[0]['src']):
              file_name = element.contents[0]['src']
          except:
            pass

          if (file_name is not None) and (os.path.basename(file_name) not in ignore_files ):
              file_url = "http://{}/{}".format(fdqn,file_name)
              base_file = os.path.basename(file_name)
              download_path = "{}/{}".format(show_dir,base_file)
              print("  - Saving {} file {}".format(show,base_file))
              urllib.request.urlretrieve(file_url,download_path)
              # time.sleep(1)
          index += 1
        done = False
    elif ('href' in link.attrs) and ('cover' in link['href']) and ('.jpg' in link['href']):
        show = link['href']
        base_file = os.path.basename(show)
        show = show.replace('covers/','')
        show = show.replace('.jpg','')
        show = show.replace('cover','')
        print("Saving {} for show {}".format(link['href'],show) )
        show_dir = "{}/{}".format(top_directory,show)
        if not os.path.exists(show_dir):
            os.mkdir(show_dir)
        download_path = "{}/{}".format(show_dir,base_file)
        print("  - Saving {} file {}".format(show,base_file))
        file_url = "http://{}/{}".format(fdqn,link['href'])
        urllib.request.urlretrieve(file_url,download_path)
