from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import re
from datetime import datetime, timedelta
from dateutil.parser import parse
import sys, traceback

BASE_URL = "http://modthesims.info";
BASE_URL_BEFORE = "/browse.php?f=414&";
BASE_URL_END = "&showType=1&gs=4";
# connect to db
client = MongoClient('localhost', 27017);
db = client.sims_test_db;
collection = db.sims_new;

# prepare pages urls by parsing total pages and putting urls into a list
def prepare_pages_urls(url):
    page_urls = [];
    data = requests.get(url).text;
    prefix = BASE_URL;
    soup = BeautifulSoup(data, 'html.parser');

    total_page = 1;

    try:
      pages = soup.find_all('div', class_="row")[3];
      pages_details = pages.find('div', class_="pull-right");
      total_page = pages.find_all('div', class_="pull-right")[2].strong.text.split("of")[1].strip();
    except:
      print('total page not found');
      pass;

    for i in range(1, int(total_page) + 1):
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


def insertAndUpdate(item):
    item_record = collection.find_one({"title": item['title']});

    if item_record is not None:
      # calculate differences from last snapshot data
      views_dif = item['views'] - item_record['views'];
      downloads_dif = item['downloads'] - item_record['downloads'];
      fav_dif = item['favourited'] - item_record['favourited'];
      thanks_dif = item['thanks'] - item_record['thanks'];

      dif_data = {
        'date': str(datetime.now().date()),
        'views': views_dif,
        'downloads': downloads_dif,
        'favourited': fav_dif,
        'thanks': thanks_dif
      };

      # perform update with new daily data;
      collection.update_one(
        {"title": item['title']}, 
        { 
          "$addToSet": { "time_series_data" : dif_data },
          "$set" : {
            "views": item['views'],
            "downloads": item['downloads'],
            "thanks": item['thanks'],
            "favourited": item['favourited']
          }
        }, 
        upsert=True);

    else:
      # simply insert the record
      collection.insert(item);

# this should get item detail and store the data into db
# item = {
#   title: string
#   artist: string
#   artist_url: string
#   preview_image: string
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
#   time_serties_data: object array
#   game_version: string
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
    game_version = "";
    date_object = None;
    comments = [];


    artist = "";
    artist_link = "";

    pack_requirement = [];
    preview_image = "";
    downloads = 0;

    # comments_total = "";
    thanks = 0;
    favourited = 0;
    views = 0;
    comments_cnt = 0;

    files = [];
    tags = [];
    types = [];

    description = "";
    url = item_url;

    item_header = soup.find('div', class_='well profilepic well-small well-inline clearfix');
    creation_info = soup.find_all('div', class_="row-fluid")[1];

    item_nav_bar = soup.find('div', class_='navbitsbreadcrumbs font-large');
    #stats_section = soup.find('div', id="carouselrow");

    stats_section = soup.find('div', class_='infobox well nopadding noborder');

    files_section = soup.find('div', id='actualtab1').find('table');

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
            published_date = section.text.split("Posted")[1].split("-")[0].strip().replace('\xa0', ' ');
            break;

        print ("Artist Name: %s" % artist);
        print ("Artist Link: %s" % artist_link);

        # format 30th Sep 2014 at 5:08 PM
        if "Today" and "Yesterday" not in published_date:
          date_object = parse(published_date);
        elif "Today" in published_date:
          date_object = datetime.today();
        elif "Yesterday" in published_date:
          date_object = datetime.today() - timedelta(days=1);

        print("Published Date: %s" % str(date_object));

        # preview_image = item_section.find('a', class_='magnific-gallery-image').get('href');
        # print("Image URL: %s" % preview_image);

    except:
      traceback.print_exc(file=sys.stdout);
      print('Basic info not FOUND');
      return;

    try:
        image_section = soup.find('div', id="screenshots");
        images = image_section.find_all('img');

        if len(images) > 0:
          preview_image = images[0].get('src');

        print('Image url is: %s' % preview_image);
    except:
      print('Image url not FOUND');
      pass;

    try:
        stats = stats_section.find('div', class_="well well-small").find_all('p');
        thanks = int(soup.find('span', id="numthanksf").text);
        # print (stats.text);

        for stat in stats:
          # find corresponding sections
          # then convert to number

          stripped_stats = stat.text.strip();
          if "Expansion" in stripped_stats:
            for img in stat.find_all('img'):
              print(img.get('alt'));
              pack_requirement.append(img.get('alt'));
          elif "Favourited" in stripped_stats:
            favourited = int(stripped_stats.split("Favourited")[0].replace(",", ""));
          elif "Downloads" in stripped_stats:
            downloads = int(stripped_stats.split("Downloads")[0].replace(",", ""));
          elif "Views" in stripped_stats:
            views = int(stripped_stats.split("Views")[0].replace(",", ""));
          elif "Comments" in stripped_stats:
            comments_cnt = int(stripped_stats.split("Comments")[0].replace(",", ""));
          elif "Game Version" in stripped_stats:
            game_version = stripped_stats.split(":")[1].strip();
          elif "Type" in stripped_stats:
            print("Type info: ");
            for mod_type in stat.find_all('em'):
              print (mod_type.text);
              types.append(mod_type.text);
          elif "Tags" in stripped_stats:
            print("Tags info: ");
            for tag in stat.find_all('a'):
              print (tag.text);
              tags.append(tag.text);

        # print("Pack requirement: %s" % pack_requirement);
        print("Thanks: %d, Favourited: %d, Downloads: %d, Views: %d, Game Version: %s" % (thanks, favourited, downloads, views, game_version));
    except:
      traceback.print_exc(file=sys.stdout);
      print('stats info not INCOMPLETE');
      pass;

    try:
      description = soup.find('div', class_= "downloadDescription").text.strip();
      # print("Item description: %s" % (description));
    except:
      print('description not FOUND');
      pass;

    # parse files info, optional
    try:
      file_entries = files_section.find('tbody').find_all('tr');

      # name, size, downloads, date
      for file in file_entries:
        temp_file = {};
        file_infos = file.find_all('td');
        for i in range(0, len(file_infos)):
          if i == 0:
            temp_file['name'] = file_infos[i].find('a').text.strip();
          elif i == 1:
            temp_file['size'] = file_infos[i].text.strip();
          elif i == 2:
            temp_file['downloads'] = int(file_infos[i].text.strip().replace(",", ""));
          elif i == 3:
            temp_file['date'] = parse(file_infos[i].text.strip().replace('\xa0', ' '));

        files.append(temp_file);
        print(temp_file);

      # print("Item description: %s" % (description));
    except:
      print('File info not FOUND');
      pass;



    # # collect tags

    # try:
    #   for tag in tags_section.find_all('a'):
    #     print (tag.text);
    #     tags.append(tag.text);
    # except:
    #   print('tags info not FOUND');
    #   pass;


    # # collect types
    # try:
    #   if type_section is not None:
    #     for mod_type in type_section.find_all('em'):
    #       print (mod_type.text);
    #       types.append(mod_type.text);
    # except:
    #   print('type info not FOUND');
    #   pass;


    item = {
      'title': title,
      'artist': artist,
      'artist_url': artist_link,
      'category': category,
      'game_version': game_version,
      'publish_date': date_object,
      'preview_image': preview_image,
      'pack_requirement': pack_requirement,
      'comments_cnt': comments_cnt,
      'views': views,
      'thanks': thanks,
      'favourited': favourited,
      'downloads': downloads,
      'comments': comments,
      'description': description,
      'url': url,
      'tags': tags,
      'types': types,
      'files': files,
      'time_series_data': []
    };

    # insert into db
    insertAndUpdate(item);

  

if __name__ == "__main__":

    # base_url = "https://www.thesimsresource.com"
    # url = "https://www.thesimsresource.com/downloads/browse/category/sims4-clothing";
    base_url = "http://modthesims.info/";
    url = "http://modthesims.info/browse.php?f=414&showType=1&gs=4";
    page_urls = [];
    # get pages urls

    # need to generate page urls for each category
    urls = ["http://modthesims.info/browse.php?f=637&showType=1&gs=4",
            "http://modthesims.info/browse.php?f=638&showType=1&gs=4",
            "http://modthesims.info/browse.php?f=639&showType=1&gs=4",
            "http://modthesims.info/browse.php?f=427&showType=1&gs=4"]

    for url in urls:
      page_urls += prepare_pages_urls(url);

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





