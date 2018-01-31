from bs4 import BeautifulSoup
import requests


# TODO, make URL generation dynamic
url = "https://www.thesimsresource.com/downloads/browse/category/sims4-clothing";
r = requests.get(url);
data =  r.text;


# TODO, fetch detail info


# TODO, store info into mongodb/dynamo

soup = BeautifulSoup(data, 'html.parser');

print(soup.prettify());