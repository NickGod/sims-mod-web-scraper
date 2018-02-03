from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import re
from datetime import datetime

BASE_URL = "https://www.thesimsresource.com";
# connect to db
client = MongoClient('localhost', 27017);
db = client.sims_test_db;
collection = db.sims_item_col;

# prepare pages urls by parsing total pages and putting urls into a list
def prepare_pages_urls(url):
    page_urls = [];
    data = requests.get(url).text;
    soup = BeautifulSoup(data, 'html.parser');
    pages = soup.find('div', class_="pager group");
    pages_details = pages.find('div', class_="pages");
    total_page = [text for text in pages_details.stripped_strings][2].split("/")[1].strip();

    prefix = BASE_URL;

    for p in pages.ul.find_all('li', attrs={'class': None}):
      postfix = p.a['href'];
      break;

    page_url_template = prefix + postfix;

    # limit total_page to 1 for testing purpose
    total_page = 1;

    # for every page number make a new url 
    for i in range(1, int(total_page)+1):
      url = re.sub('/page/([0-9])+', '/page/'+str(i), page_url_template);
      print(url);
      page_urls.append(url);

    return page_urls;

# this should return items urls in a page
def parse_items_in_page(page_url):
    items_urls = [];
    data = requests.get(page_url).text;
    soup = BeautifulSoup(data, 'html.parser');
    items = soup.find_all('div', class_="browse-file");

    for item in items:
      item_url = BASE_URL + item.a['data-href'];
      print(item_url);
      items_urls.append(item_url);

    return items_urls;

# this should get item detail and store the data into db
# item = {
#   title: string
#   artist: string
#   publish_date: date
#   downloads: number
#   comments: number
#   description: string
#   short_url: string
#   item_id: number
#   revision: number
#   type: string
#   preview_image: string
# }

def parse_item_page(item_url):
    print("\n========================\n");
    print("Processing: %s" % item_url);
    print("\n========================\n");

    item = {};
    data = requests.get(item_url).text;
    soup = BeautifulSoup(data, 'html.parser');

    item_section = soup.find('div', id='big-image');
    creation_info = soup.find('div', id='creation-info');

    title = item_section.find('div', class_='big-header').text.strip();
    print("Title: %s" % title);

    published_date = item_section.find('div', class_='big-published-details').text.strip().split(' ', 1)[1];
    print("Published Date: %s" % published_date);
    date_object = datetime.strptime(published_date, '%b %d, %Y');

    preview_image = item_section.find('a', class_='magnific-gallery-image').get('href');
    print("Image URL: %s" % preview_image);


    artist = item_section.find('p', class_='artist-name').text.strip();
    print("Artist Name: %s" % artist);

    downloads = int(item_section.find_all('span', class_='stats-size')[0].text.replace(',', ''));
    comments = int(item_section.find_all('span', class_='stats-size')[1].text.replace(',', ''));
    print("Downloads: %s" % downloads);
    print("Comments: %s" % comments);

    # print(comments);

    # top_field_length = len(creation_info.find('div', id='info-description').find_all('p'));

    description = creation_info.find('div', id='info-description').text;
    # print(description);

    short_url = "";
    item_id = "";
    revision = "";
    mod_type = "";

    for info in creation_info.find('div', id='info-description').find_all('p'):
      # parse separate field info out
      content = info.text;
      if 'Short URL' in content:
          short_url = content.split(':', 1)[1].strip();
      if 'ItemID' in content:
          item_id = content.split(':')[1].strip();
      if 'Revision' in content:
          revision = int(content.split(':')[1]);

    print("Short_url: %s" % short_url);
    print("Item_id: %s" % item_id);
    print("Revision: %s" % revision);

    for c_info in creation_info.find('ul', class_='info-attributes group').find_all('li'):
      content = c_info.text;
      if 'Type' in content:
        mod_type = content.split(':')[1].strip();


    print("Mod type: %s" % mod_type);

    item = {
      'title': title,
      'artist': artist,
      'publish_date': date_object,
      'downloads': downloads,
      'comments': comments,
      'description': description,
      'short_url': short_url,
      'item_id': item_id,
      'revision': revision,
      'mod_type': mod_type,
      'preview_image': preview_image
    };

    # insert into db
    collection.insert(item);

if __name__ == "__main__":
    # TODO, make URL generation dynamic
    base_url = "https://www.thesimsresource.com"
    url = "https://www.thesimsresource.com/downloads/browse/category/sims4-clothing";

    # get pages urls
    page_urls = prepare_pages_urls(url);

    # parse every page and item, and persist the data into db
    for url in page_urls:
      item_urls = parse_items_in_page(url);
      for item in item_urls:
        parse_item_page(item);





