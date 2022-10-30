import requests
import json
from bs4 import BeautifulSoup


# Taking first paragraph from wikiPEDIA
url_wikipedia = 'https://en.wikipedia.org/wiki/Nevada_State_Railroad_Museum'

r_wikipedia = requests.get(url_wikipedia)
soup_wikipedia = BeautifulSoup(r_wikipedia.text, 'html.parser')
html_doc_wikipedia = soup_wikipedia.find('div', class_ = 'mw-body-content mw-content-ltr')
paragraph = html_doc_wikipedia.find('p').text



# Taking all images links from wikiMEDIA
url_wikimedia = "https://commons.wikimedia.org/wiki/Category:Nevada_State_Railroad_Museum"

r_wikimedia = requests.get(url_wikimedia)
soup_wikimedia = BeautifulSoup(r_wikimedia.text, 'html.parser')
html_doc_wikimedia = soup_wikimedia.find('ul', class_ ='gallery mw-gallery-traditional')

list_images = []
for image in html_doc_wikimedia.find_all('li', class_ = 'gallerybox'):
    rows = image.find('div')
    for link in rows.find('a'):
        images_links = link.get('src')
        list_images.append(images_links)



#  Info about Images
img_url = "https://commons.wikimedia.org/wiki/"
end_points = ['4-4-0 Inyo.jpg', 'AKC 2014 pics7 019.jpg']

for end_point in end_points:
    images_url = f'{img_url} + {end_points}'


r_images = requests.get(images_url)
soup_images = BeautifulSoup(r_images.text, 'html.parser')
html_doc_images = soup_images.find_all('table', class_ = 'fileinfotpl-type-information toccolours vevent mw-content-ltr' )

for image in html_doc_images.find_all('tbody'):
    rows = image.find('tr')
    for row in rows:
        image_description = row.find('td', class_ = 'description')
        print(image_description)
        






# Taking all information about event from API
response_museum = requests.get('https://nominatim.openstreetmap.org/details.php?osmtype=W&osmid=407063554&class=tourism&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json')

data = json.loads(response_museum.text)

experience_name = data['names']['name']
address_1 = data['addresstags']['street']
address_2 = data['addresstags']['housenumber']
city = data['addresstags']['city']
state = data['addresstags']['state']
zip = data['addresstags']['postcode']


# Put all information I got, into the dict
all_info = {
    'experience_name': experience_name,
    'city' : city,
    'state' : state,
    'zip': zip,
    'address1': address_1,
    'address2' : address_2,
    'wikipedia' : url_wikipedia,
    'experience_description' : paragraph,
    'experience_images' : list_images,
}

all_info_json = json.dumps(all_info)