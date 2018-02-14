from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import re
from datetime import datetime
from dateutil.parser import parse
import sys, traceback

BASE_URL = "http://modthesims.info";
BASE_URL_BEFORE = "/browse.php?f=414&";
BASE_URL_END = "&showType=1&gs=4";
# connect to db
client = MongoClient('localhost', 27017);
db = client.sims_test_db;
collection = db.sims_item_col;

# prepare pages urls by parsing total pages and putting urls into a list
def prepare_pages_urls(url):
    page_urls = [];
    data = requests.get(url).text;

    soup = BeautifulSoup(data, 'html.parser');
    soup.prettify();
    pages = soup.find_all('div', class_="row")[3];

    pages_details = pages.find('div', class_="pull-right");

    total_page = pages.find_all('div', class_="pull-right")[2].strong.text.split(" ")[3];

    prefix = BASE_URL;

    for i in range(2, int(total_page) + 1):
        url = prefix + BASE_URL_BEFORE + "page=" + str(i) + BASE_URL_END;
        # print url;
        page_urls.append(url);

    return page_urls;

# this should return items urls in a page
def parse_items_in_page(page_url):
    items_urls = [];
    data = requests.get(page_url).text;

    soup = BeautifulSoup(data, 'html.parser');
    items = soup.find_all('div', class_="downloadblock column");

    for item in items:
      item_url = BASE_URL + item.a['href'];
      items_urls.append(item_url);

    return items_urls;

# this should get item detail and store the data into db
# item = {
#   title: string
#   artist: string
#   artist_url: string
#   publish_date: date
#   downloads: number
#   views: number
#   favourited: number
#   thanks: number
#   comments: number
#   description: string
#   url: string
#   tags: string array
#   types: string array
# }

def parse_item_page(item_url):
    print("\n========================\n");
    print("Processing: %s" % item_url);
    print("\n========================\n");

    item = {};
    data = requests.get(item_url).text;
    soup = BeautifulSoup(data, 'html.parser');

    title = "";
    publish_date = "";
    preview_image = "";
    date_object = None;
    comments = [];


    artist = "";
    artist_link = "";

    downloads = "";
    # comments_total = "";
    thanks = "";
    favourited = "";
    views = "";

    tags = [];
    types = [];

    description = "";
    url = item_url;

    item_header = soup.find('div', class_='well profilepic well-small well-inline');
    creation_info = soup.find_all('div', class_="row-fluid")[1];

    item_nav_bar = soup.find('div', class_='navbitsbreadcrumbs font-large');
    stats_section = soup.find('div', id="carouselrow");

    tags_section = soup.find('div', id="threadtagsarea");

    type_section = soup.find('td', class_='smallfont');

    try:
        category = item_nav_bar.find('h3').text.strip();
        print("Category: %s" % category);

        title = item_header.find('h2').text.strip();
        print("Title: %s" % title);

        # second pull left section for artist profile
        # this is not necessarily true
        for section in item_header.find_all('div', class_="pull-left"):
          if "by" in section.text:
            artist = section.find('a').span.text;
            artist_link = section.find('a').get('href');
            published_date =section.text.split("Posted")[1].split("-")[0].strip().replace('\xa0', ' ');
            break;

        print ("Artist Name: %s" % artist);
        print ("Artist Link: %s" % artist_link);

        # format 30th Sep 2014 at 5:08 PM
        if "Today" not in published_date:
          date_object = parse(published_date);
        else:
          date_object = datetime.now();

        print("Published Date: %s" % str(date_object));

        # preview_image = item_section.find('a', class_='magnific-gallery-image').get('href');
        # print("Image URL: %s" % preview_image);


        stats = stats_section.find('div', class_="cf").find_all('div');

        # print (stats.text);

        for stat in stats:
          # find corresponding sections
          # then convert to number

          stripped_stats = stat.text.strip();
          if "Thanks" in stripped_stats:
            thanks = int(stripped_stats.split("\n")[0].replace(",", ""));
          elif "Favourited" in stripped_stats:
            favourited = int(stripped_stats.split("\n")[0].replace(",", ""));
          elif "Downloads" in stripped_stats:
            downloads = int(stripped_stats.split("\n")[0].replace(",", ""));
          elif "Views" in stripped_stats:
            views = int(stripped_stats.split("\n")[0].replace(",", ""));

        print("Thanks: %d, Favourited: %d, Downloads: %d, Views: %d" % (thanks, favourited, downloads, views));

    except:
      traceback.print_exc(file=sys.stdout);
      print('Basic info not FOUND');
      return;


    try:
      description = soup.find('div', class_= "downloadDescription").text.strip();
      # print("Item description: %s" % (description));
    except:
      print('description not FOUND');
      pass;


    # collect tags

    try:
      for tag in tags_section.find_all('a'):
        print (tag.text);
        tags.append(tag.text);
    except:
      print('tags info not FOUND');
      pass;


    # collect types
    try:
      if type_section is not None:
        for mod_type in type_section.find_all('em'):
          print (mod_type.text);
          types.append(mod_type.text);
    except:
      print('type info not FOUND');
      pass;


    item = {
      'title': title,
      'artist': artist,
      'artist_url': artist_link,
      'category': category,
      'publish_date': date_object,
      'views': views,
      'thanks': thanks,
      'favourited': favourited,
      'downloads': downloads,
      'comments': comments,
      'description': description,
      'url': url,
      'tags': tags,
      'types': types,
    };

    # insert into db
    collection.insert(item);

if __name__ == "__main__":
    # TODO, make URL generation dynamic

    # base_url = "https://www.thesimsresource.com"
    # url = "https://www.thesimsresource.com/downloads/browse/category/sims4-clothing";
    base_url = "http://modthesims.info/";
    url = "http://modthesims.info/browse.php?f=414&showType=1&gs=4";

    # get pages urls
    page_urls = prepare_pages_urls(url);

    # parse every page and item, and persist the data into db
    for i in range(0, len(page_urls)):
        item_urls = parse_items_in_page(page_urls[i]);
        for item in item_urls:
          parse_item_page(item);


    # for url in page_urls:
    #   i += 1;


      # print('Processing page %d out of %d' % (i, len(page_urls)));
      # item_urls = parse_items_in_page(url);
      # for item in item_urls:
      #   parse_item_page(item);





