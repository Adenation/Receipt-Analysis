# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:08:06 2023

@author: Adenation
"""
#%% Imports

import os
import random
from PIL import Image, ImageDraw, ImageFont
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import requests
import json
import difflib
import time
import csv

import barcode
from barcode import EAN13
from barcode.writer import ImageWriter

from io import BytesIO

#%% Change working directory if needed

#os.chdir()
os.getcwd()

#%% Lists
# Define the shops list
shops = [["Tesco", "Te5co", "Tesc0", "Te5c0"], 
         ["Sainsbury's", "Sa1nsbury's", "Sainsburys", "Sa1nsburys"],
         ["Asda", "A5da", "Ada"],
         ["Lidl", "L1dl", "1idl"],
         ["Aldi", "Ald1", "A1di"],
         ["M&S", "M&5"]]

# Define a list of item names and prices
items = [("Apples", 1.50), ("Bananas", 0.80), ("Oranges", 1.20),
("Tomatoes", 2.00), ("Potatoes", 0.50), ("Carrots", 1.00),
("Lettuce", 1.50), ("Cucumber", 1.00), ("Spinach", 2.00),
("Bell Pepper", 1.50), ("Onions", 0.80), ("Garlic", 2.50),
("Ginger", 3.00), ("Broccoli", 1.80), ("Cauliflower", 2.00),
("Celery", 1.20), ("Mushrooms", 2.50), ("Zucchini", 1.50),
("Eggplant", 2.00), ("Pumpkin", 1.50), ("Sweet Potato", 1.00),
("Radish", 0.80), ("Beetroot", 1.20), ("Cabbage", 1.50),
("Leeks", 2.00), ("Spring Onion", 0.80), ("Kale", 2.50),
("Arugula", 1.50), ("Endive", 1.20), ("Fennel", 2.00),
("Artichokes", 3.00), ("Asparagus", 4.00), ("Chard", 1.80),
("Collard Greens", 1.50), ("Mustard Greens", 1.20), ("Okra", 2.00),
("Peas", 1.50), ("Beans", 1.80), ("Lima Beans", 2.50),
("Chickpeas", 1.50), ("Lentils", 1.20), ("Black Beans", 2.00),
("Kidney Beans", 1.50), ("Soybeans", 2.00), ("Tofu", 2.50),
("Quinoa", 3.00), ("Brown Rice", 1.50), ("White Rice", 1.20),
("Barley", 2.00), ("Bulgur", 2.50), ("Oats", 1.50),
("Whole Wheat Flour", 2.00), ("Almond Flour", 3.00), ("Coconut Flour", 4.00),
("Buckwheat Flour", 2.50), ("Cornmeal", 1.50), ("Polenta", 2.00),
("Pasta", 1.50), ("Ramen Noodles", 1.20), ("Soba Noodles", 2.00),
("Udon Noodles", 2.50), ("Egg Noodles", 1.50), ("Rice Noodles", 2.00),
("Bread", 1.50), ("Bagels", 1.20), ("Croissants", 2.00),
("Muffins", 2.50), ("Donuts", 1.50), ("Cake", 2.00),
("Cookies", 1.50), ("Brownies", 2.00), ("Pancake Mix", 2.50),
("Maple Syrup", 3.00), ("Honey", 2.00), ("Agave Nectar", 2.50),
("Molasses", 1.50), ("Pistachios", 5.00)]


# Define a list of addresses in the UK
addresses = ["123 High Street, London, E1 7XX", "456 Main Street, Manchester, M1 4XX",
             "789 Park Road, Birmingham, B1 5XX", "12 Station Road, Bristol, BS1 4XX",
             "34 Bridge Street, Liverpool, L1 5XX", "56 King's Road, Brighton, BN1 3XX"]

# Define the ShopList and ProductList
ShopList = [(1, 'Tesco'), (2, 'Asda'), (3, 'Lidl'), (4, "Sainsbury's"), (5, 'M&S'), (6, 'Aldi')]
ProductList =  [(i+1, item[0]) for i, item in enumerate(items)]

fonts = ["arial.ttf", "DejaVuSans.ttf", "FreeMono.ttf", "AdobeVFPrototype.ttf"]

#%% Definitions

# Define method to generate random spelling errors
def generate_spelling_error(word):
    options = ['omit', 'repeat', 'o_to_0', '0_to_o', 'i_to_1', '1_to_i', 'l_to_1', '1_to_l', 's_to_5', '5_to_s']
    error_type = random.choice(options)
    if error_type == 'omit':
        if len(word) > 1:
            index = random.randint(0, len(word) - 1)
            return word[:index] + word[index + 1:]
        else:
            return word
    elif error_type == 'repeat':
        index = random.randint(0, len(word) - 1)
        return word[:index] + word[index] + word[index:]
    elif error_type == 'o_to_0':
        return word.replace('o', '0').replace('O', '0')
    elif error_type == '0_to_o':
        return word.replace('0', 'o')
    elif error_type == 'i_to_1':
        return word.replace('i', '1').replace('I', '1')
    elif error_type == '1_to_i':
        return word.replace('1', 'i')
    elif error_type == 'l_to_1':
        return word.replace('l', '1').replace('L', '1')
    elif error_type == '1_to_l':
        return word.replace('1', 'l')
    elif error_type == 's_to_5':
        return word.replace('s', '5').replace('S', '5')
    elif error_type == '5_to_s':
        return word.replace('5', 's')
    
    
# Define a function to compute the Levenshtein distance
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1        # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# Define a function to perform the approximate string matching
def approximate_string_matching(string, options_list):
    match_list = difflib.get_close_matches(string, options_list, n=1, cutoff=0.7)
    
    if len(match_list) > 0:
        best_match = match_list[0]
        similarity_ratio = difflib.SequenceMatcher(None, string, best_match).ratio()
        match_prob = 1 - (1 - similarity_ratio) ** len(best_match)
        print(f'Best match: {best_match}, match probability: {match_prob:.2f}')
        best_match = string, match_list[0], levenshtein_distance(string, match_list[0])
        print(best_match)
        print(f'Matching {best_match[0]} to {best_match[1]} with a Levenshtein distance of {best_match[2]}')
        return best_match
    else:
        return None



# Define a function to process the JSON payload and update the lists
def process_json(json_payload):
    for recognized_text in json_payload['analyzeResult']['readResults']:
        for line in recognized_text['lines']:
            for word in line['words']:
                print(f'Matching to ' + word['text'])
                # Check if the word matches a shop name
                shop_match = approximate_string_matching(word['text'], [shop[1] for shop in ShopList])
                # If there's a match
                if shop_match:
                    shop_id = [shop[0] for shop in ShopList if shop[1] == shop_match[1]][0]
                    # If the Levenshtein distance is greater than 0
                    if shop_match[2] > 0:
                        # Add the shop to the list with the correct ID
                        ShopList.append((shop_id, shop_match[0]))
                        print(f'Matched {shop_match[0]} to {shop_match[1]} with ID {shop_id}')
                        writer.writerow(['shop', shop_id, shop_match[0], shop_match[1], shop_match[2]])
                    else:
                        print(f'{shop_match[0]} is already in list with ID {shop_id}')
                        writer.writerow(['shop', shop_id, shop_match[0], shop_match[1], shop_match[2]])
                    #if not shop_id:
                    #    new_id = max([shop[0] for shop in ShopList]) + 1
                    #    ShopList.append((new_id, shop_match))
                # Check if the word matches a product name
                product_match = approximate_string_matching(word['text'], [product[1] for product in ProductList])
                # If there's a match
                if product_match:
                    product_id = [product[0] for product in ProductList if product[1] == product_match[1]][0]
                    # If the Levenshtein distance is greater than 0
                    if product_match[2] > 0:
                       # Add the product to the list with the correct ID
                       ProductList.append((product_id, product_match[0]))
                       print(f'Matched {product_match[0]} to {product_match[1]} with ID {product_id}')
                       writer.writerow(['product', product_id, product_match[0], product_match[1], product_match[2]])
                    else:
                       print(f'{product_match[0]} is already in list with ID {product_id}')
                       writer.writerow(['product', product_id, product_match[0], product_match[1], product_match[2]])


#%% Generate receipts

# Decide how many receipts you want to generate
receipts_to_generate = 30

padding = 20

# Define the width and height of the image
image_width = 600
image_height = 800


receipt_list = []    

for j in range(receipts_to_generate):
    
    # Define the font sizes and padding
    title_font_size = random.randint(28, 30)
    address_font_size = random.randint(16, 18)
    item_font_size = random.randint(16, 18)
    total_font_size = random.randint(20, 24)
    
    # Choose a random shop title and address
    shop_title = random.choice(random.choice(shops))
    shop_address = random.choice(addresses)
    
    # Create a new image with a white background
    image = Image.new("RGB", (image_width, image_height), (255, 255, 255))
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Define the title font
    title_font = ImageFont.truetype(random.choice(fonts), title_font_size)
    
    # Draw the shop title
    title_width, title_height = draw.textsize(shop_title, font=title_font)
    draw.text((padding, padding), shop_title, fill=(0, 0, 0), font=title_font)
    
    # Define the address font
    address_font = ImageFont.truetype(random.choice(fonts), address_font_size)
    
    # Draw the shop address
    address_width, address_height = draw.textsize(shop_address, font=address_font)
    draw.text((padding, padding + title_height + padding), shop_address, fill=(0, 0, 0), font=address_font)
    
    # Define the item font
    item_font = ImageFont.truetype(random.choice(fonts), item_font_size)
    
    # Define the starting position of the item list
    item_x = padding
    item_y = padding + title_height*2 + padding + address_height*2 + padding
    
    # Define the number of items purchased and the subtotal
    num_items = random.randint(5, 10)
    sub_total = 0
    
    
    # Draw the item details
    for i in range(num_items):
        # Choose a random item and quantity
        item, price = random.choice(items)
        
        # Randomly generate spelling errors
        item = generate_spelling_error(item)
        
        quantity = random.randint(1, 5)
    
        # Calculate the item total
        item_total = price * quantity
    
        # Add the item total to the subtotal
        sub_total += item_total
    
        # Draw the item details
        item_name = f"{item}"
        item_quantity = f"{quantity} @ £{price:.2f}"  
        item_total_text = f"£{item_total:.2f}"
        item_width, item_height = draw.textsize(item_name, font=item_font)
        item_q_width, item_q_height = draw.textsize(item_quantity, font=item_font)
        item_total_width, item_total_height = draw.textsize(item_total_text, font=item_font)
        draw.text((item_x, item_y), item_name, fill=(0, 0, 0), font=item_font)
        draw.text((item_x + item_width + padding, item_y), item_quantity, fill=(0,0,0), font=item_font)
        draw.text((image_width - item_total_width - padding, item_y), item_total_text, fill=(0, 0, 0), font=item_font)
    
    
    
        # Move the item position down
        item_y += item_height + padding
    
    # Check if there are multibuy savings
    savings = 0
    if num_items > 2:
        savings = (num_items - 2) * random.uniform(0.5, 2.5)
        total_savings_text = f"Total savings: £{savings:.2f}"
        sub_total_text = f"Subtotal: £{sub_total:.2f}"
        total_text = f"Total to pay: £{sub_total-savings:.2f}"
        savings_width, savings_height = draw.textsize(total_savings_text, font=item_font)
        sub_total_width, sub_total_height = draw.textsize(sub_total_text, font=item_font)
        total_width, total_height = draw.textsize(total_text, font=item_font)
        draw.text((padding, item_y + padding), sub_total_text, fill=(0, 0, 0), font=item_font)
    if savings > 0:
        draw.text((padding, item_y + padding + sub_total_height), total_savings_text, fill=(0, 0, 0), font=item_font)
        draw.text((padding, item_y + padding + sub_total_height + savings_height), total_text, fill=(0, 0, 0), font=item_font)
        
        # Draw dotted line
        draw.line((padding, item_y + item_height + padding, image_width - padding, item_y + item_height + padding), fill=(0, 0, 0), width=1, joint="curve")
        
    else:    
        total_to_pay = sub_total - savings if num_items >= 2 else sub_total
        total_to_pay_text = f"Total to pay: £{total_to_pay:.2f}"
        draw.text((padding, item_y + item_height*2 + padding*2), total_to_pay_text, fill=(0, 0, 0), font=item_font)
        

    # Draw the image
    #image.show()
    image.save('receipt' + str(j+170) + '.png')
    #receipt_list.append(image)


#%% Generate JSON

# set up the Azure Computer Vision API endpoint and key
subscription_key = '<Your Subscription Key>'
endpoint = '<Your Endpoint>'

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# set up the image path
folder_path = os.getcwd()

# Get a list of all PNG files in the folder
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# Read each PNG file into a byte array and add it to a list
png_bytes_list = []
for png_file in png_files:
    with open(os.path.join(folder_path, png_file), 'rb') as f:
        png_bytes_list.append(f.read())

# Or if stored already in an earlier variable use that instead
# png_bytes_list = []
# buffer = BytesIO()
# for img in receipt_list:
#     img.save(buffer, format='png')
#     png_bytes_list.append(buffer.getvalue())

    
# set up the API headers and parameters
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key
}
params = {
    'language': 'en',
    'detectOrientation': 'true'
}



# call the API to analyze the images and load into a list of json payloads

headers_list = []
print(headers_list)
responses_list = []

json_data_list = []
for image_data in png_bytes_list:
    post = requests.post(endpoint, headers=headers, params=params, data=image_data)
    headers_list.append(post.headers)
    time.sleep(3) # Delay for 3 seconds to avoid going over 20 free calls per minute
    operation_url = post.headers['Operation-Location']
    attempts = 0; waiting = True
    while(waiting and attempts < 10):
        response = requests.get(operation_url, headers=headers)
        responses_list.append(response)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            while(json_data["status"] == "running"):
                # While operation is successful and runnin, wait for it to finish
                time.sleep(3)
            # Once it has finished running status should change to succeeded
            # extract the JSON payload from the response
            json_data_list.append(json_data)
            # print the JSON payload
            print(json.dumps(json_data, indent=2))
            # break out of loop
            waiting = False
        if response.status_code == 202:
            print("Waiting for server to process response.  Attempting again in 3 seconds")
            attempts += 1
        else:
            print("Error retrieving results:", response.text, response.status_code)
    
    time.sleep(3)


#print(response)
#print(response.status_code)
#print(response.headers)
print(json.loads(response.text)["status"])
#%% Fuzzy v2



# Process the example JSON payload and write matches to a CSV file
with open('matches.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['type', 'id', 'name', 'matched_name', 'Levenshtein Distance'])
    
    da_index = 0
    for json_data in json_data_list:
        writer.writerow(['Receipt', da_index])
        process_json(json_data)
        da_index +=1
    
    writer.writerow(['Updated Shop List'])
    for shop in sorted(ShopList, key=lambda x :x[0]):
        writer.writerow([shop[0], shop[1]])
    writer.writerow(['Updated Product List'])
    for product in sorted(ProductList, key=lambda x: x[0]):
        writer.writerow([product[0], product[1]])
     
# Print the updated lists
print(ShopList)
print(ProductList)


