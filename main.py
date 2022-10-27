import requests
import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib import response


# Taking first paragraph from wikiPEDIA
# This one is not working properly anymore like it use to. I don't know what happen to it. Use to give me first paragraph from wiki. Now it says "This category has the following 4 subcategories, out of 4 total".

session = HTMLSession()

wikipedia_url = "https://commons.wikimedia.org/wiki/Category:Nevada_State_Railroad_Museum"

response = session.get(wikipedia_url)

wikipedia_data = response.html.find('p')[0]

for row in wikipedia_data.find('p'):
    paragraph = row.text
    # print(paragraph)



# Taking all images links from wikiMEDIA
# This one is working good by it self, but when I added to my DICT, it shows only one picture link instead all of it.

wikimedia_url = "https://commons.wikimedia.org/wiki/Category:Nevada_State_Railroad_Museum"


req = requests.get(wikimedia_url)

html = BeautifulSoup(req.text, 'html.parser')

img_tag = html.find_all('img')
for image in img_tag:
    images_links = image['src']
    # print(images_links)
        

# Taking all information about event
response_museum = requests.get('https://nominatim.openstreetmap.org/details.php?osmtype=W&osmid=407063554&class=tourism&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json')


data = json.loads(response_museum.text)

experience_name = data['names']['name']
address_1 = data['addresstags']['street']
address_2 = data['addresstags']['housenumber']
city = data['addresstags']['city']
state = data['addresstags']['state']
zip = data['addresstags']['postcode']


all_info ={
    'activity_name': experience_name,
    'city' : city,
    'state' : state,
    'zip': zip,
    'address1': address_1,
    'address2' : address_2,
    'wikipedia' : wikipedia_url,
    'experience description' : paragraph,
    'experience_images' : [images_links]
}


all_info_json = json.dumps(all_info)
print(all_info)

# Info about Images
# Wasn't able to figure out 


# img_url = "https://commons.wikimedia.org/wiki/File:4-4-0_Inyo.jpg"

# res = session.get(img_url)

# img_data = response.html.find('tr')[0]

# for row in img_data.find('td'):
#     img_description = row.text
#     print(img_description)

