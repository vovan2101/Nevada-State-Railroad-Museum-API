from doctest import Example
import requests
from bs4 import BeautifulSoup
import json


# User put info about event that they are looking for
state = str(input('Please enter state: '))
print()
city = str(input('Please enter city name: '))
print()
event_name = str(input('Please enter an event name: '))
print()


# Taking osm id of event, to get more data about event
search_json = requests.get(f'https://nominatim.openstreetmap.org/search.php?q={state}+{city}+{event_name}&format=jsonv2')
osm_id_data = json.loads(search_json.text)
osm_id = osm_id_data[0]['osm_id']


# All data from json page
advanced_search_json = requests.get(f'https://nominatim.openstreetmap.org/details.php?osmtype=W&osmid={osm_id}&format=json')
data = json.loads(advanced_search_json.text)

place_id = data['place_id']
category = data['category']
experience_name = data['names']['name']
address_1 = data['addresstags']['street']
address_2 = data['addresstags']['housenumber']
city = data['addresstags']['city']
state = data['addresstags']['state']
zip = data['addresstags']['postcode']
wikipedia_name = data['calculated_wikipedia'][2:]
wikidata = data['extratags']['wikidata']


# Taking first paragraph from wikipedia if more then 50 elements, else taking two paragraphs
wikipedia = f'https://en.wikipedia.org/wiki/{wikipedia_name}'
wikipedia_request = requests.get(wikipedia)
soup_wikipedia = BeautifulSoup(wikipedia_request.text, 'lxml')
paragraph1 = soup_wikipedia.find('p').text.strip()

if len(paragraph1) < 50:
    paragraph2 = soup_wikipedia.find('p').find_next('p').text.strip()
try:
    experience_description = f'{paragraph1}\n\n{paragraph2}'
except:
    experience_description = paragraph1


# Website, phonenumber and socialmedia from wikidata
wikidata_url = requests.get(f'https://m.wikidata.org/wiki/Special:EntityData/{wikidata}.json?')
data_wikidata = json.loads(wikidata_url.text)

try:
    website = data_wikidata['entities'][f'{wikidata}']['claims']['P856'][0]['mainsnak']['datavalue']['value']
    phone_number = data_wikidata['entities'][f'{wikidata}']['claims']['P1329'][0]['mainsnak']['datavalue']['value']
    twitter_id = data_wikidata['entities'][f'{wikidata}']['claims']['P8687'][0]['qualifiers']['P6552'][0]['datavalue']['value']
    twitter = f'https://twitter.com/i/user/{twitter_id}'
except:
    website = data_wikidata['entities'][f'{wikidata}']['claims']['P856'][0]['mainsnak']['datavalue']['value']
    phone_number = None
    twitter = None
else:
    website = None
    phone_number = None
    twitter = None


# All event images links
images_url = requests.get(f'https://commons.wikimedia.org/wiki/Category{wikipedia_name}')
soup_images = BeautifulSoup(images_url.text, 'lxml')
images_wikimedia = soup_images.find('ul', class_ ='gallery mw-gallery-traditional')

for image in images_wikimedia.find_all('li', class_ = 'gallerybox'):
    images_title = image.find('a').get('href')
    images_links = f'https://en.wikipedia.org/{images_title}'


# Images description
    images_description_url = requests.get(f'https://commons.wikimedia.org{images_title}')
    soup_description = BeautifulSoup(images_description_url.text, 'lxml')
    try:
        description_wikimedia = soup_description.find('tbody').find('td', class_ = 'description').find('div', class_ = 'description mw-content-ltr en')
        for description in description_wikimedia:
                description_images = description.text.strip()
    except TypeError:
        print(None)
        continue
    except AttributeError:
        print(None)
        continue
    except Exception:
        description_wikimedia = soup_description.find('tbody').find('td', class_ = 'description')
        for description in description_wikimedia:
            description_images = description.text.strip()


# Images license
    soup_license = BeautifulSoup(images_description_url.text, 'lxml')
    try:
        license_wikimedia = soup_license.find('div', class_ = 'rlicense-declaration')
        for license in license_wikimedia.find('a'):
            images_license = license
    except Exception:
        license_wikimedia = soup_license.find('tbody')
        for license in license_wikimedia.find('a'):
            images_license = license


# All images information together
    images_info_list = []
    images_info = f'Image: {images_links} | description: {description_images} | license: {images_license}'
    images_info_list.append(images_info)


# All data about event
    all_info = {
        'place_id' : place_id,
        'category' : category,
        'experience_name': experience_name,
        'city' : city,
        'state' : state,
        'zip': zip,
        'address1': address_1,
        'address2' : address_2,
        'wikipedia_name' : wikipedia,
        'experience_description' : experience_description,
        'website' : website,
        'phone_number' : phone_number,
        'twitter' : twitter,
        'all_images_info' : images_info_list,
    }

with open('all_info_json', 'w') as file:
    json.dump(all_info, file, indent=4, ensure_ascii=False)

