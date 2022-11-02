from flask import Flask
from flask import jsonify
import requests
import json
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(all_info)


# Taking first paragraph from wikiPEDIA
url_wikipedia = 'https://en.wikipedia.org/wiki/Nevada_State_Railroad_Museum'

r_wikipedia = requests.get(url_wikipedia)
soup_wikipedia = BeautifulSoup(r_wikipedia.text, 'lxml')
paragraph = soup_wikipedia.find('p').text


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


#  description of images
img_url = 'https://commons.wikimedia.org/wiki/File:'
end_points = ['4-4-0 Inyo.jpg', 'AKC 2014 pics7 019.jpg', 'Dual_Coupling_Link_%26_Pin_with_Knuckle_Coupler.jpg', 'Engine_22,_2.JPG', 'Engine_22,_3.JPG', 'Engine 22.JPG', 'Locomotive 27.jpg', 'McKeen_Motor_Car_-22_Restoration.jpg', 'Nevada_State_Museum_at_Carson_City_NV_-_panoramio.jpg', 
'Nevada_State_Museum_Inside_-_panoramio.jpg', 'Nevada_State_Railroad_Museum_-_panoramio_(1).jpg', 'Nevada_State_Railroad_Museum_-_panoramio_(12).jpg',
'Nevada_State_Railroad_Museum_-_panoramio_(2).jpg', 'Nevada_State_Railroad_Museum_-_panoramio_(3).jpg', 'Nevada_State_Railroad_Museum_-_panoramio_(4).jpg', 'Nevada_State_Railroad_Museum_-_panoramio_(5).jpg', 'Nevada_State_Railroad_Museum_-_panoramio_(6).jpg', 'Nevada_State_Railroad_Museum_-_panoramio_(7).jpg', 
'Nevada_State_Railroad_Museum_-_panoramio_(8).jpg', 'Nevada_State_Railroad_Museum_-_panoramio_(9).jpg', 'Nevada_State_Railroad_Museum_-_panoramio.jpg', 'NSRRMCC031.jpg', 'Velocipede_at_NRM.jpg']

for end_point in end_points:
    images_url = img_url + end_point

    r_images = requests.get(images_url)
    soup_images = BeautifulSoup(r_images.text, 'lxml')
    description_list = []

    try:
        images_div = soup_images.find('td', class_ = 'description')
        for image in images_div.find('div', class_ = 'description mw-content-ltr en').text:
            description_list.append(image[1])         
    except:
        images_description_2part = soup_images.find('td', class_ = 'description')
        description_list.append(images_description_2part.text)


# Lisens of images
    try:
        r_images_licens = requests.get(images_url)
        soup_licens = BeautifulSoup(r_images_licens.text, 'lxml')  
        images_lincens = soup_licens.find(class_ = 'rlicense-declaration').find('a', class_ = 'extiw').text
        print(images_lincens)
    except:
        pass


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
    'images_licens' : images_lincens,
    'images_description' : description_list,
    'experience_images' : list_images,
}

with open('all_info_json', 'w') as file:
    json.dump(all_info, file, indent=4, ensure_ascii=False)