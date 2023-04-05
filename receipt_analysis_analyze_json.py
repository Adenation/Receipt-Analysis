# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 15:00:57 2023

@author: Adenation
"""
#%% Imports

import difflib
import os
import json
import csv
from dotenv import load_dotenv

#%% Lists

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

# Define the ShopList and ProductList
ShopList = [(1, 'Tesco'), (2, 'Asda'), (3, 'Lidl'), (4, "Sainsbury's"), (5, 'M&S'), (6, 'Aldi')]
ProductList =  [(i+1, item[0]) for i, item in enumerate(items)]

# Persist matches for review
matchList = []

#%% Defintions

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
    match_list = difflib.get_close_matches(string, options_list, n=3, cutoff=0.6)
    if len(match_list) > 0:
        best_match = match_list[0]
        similarity_ratio = difflib.SequenceMatcher(None, string, best_match).ratio()
        match_prob = 1 - (1 - similarity_ratio) ** len(best_match)
        print(f'Best match: {best_match}, match probability: {match_prob:.2f}')
        best_match = string, match_list[0], levenshtein_distance(string, match_list[0])
        print(best_match)
        print(f'Matching {best_match[0]} to {best_match[1]} with a Levenshtein distance of {best_match[2]}')
        matchList.append([string, match_list, similarity_ratio, best_match])
        return best_match
    else:
        return None



# Define a function to process the JSON payload and update the lists
def process_json(json_payload):
    if __name__ == '__main__':
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

#%% Main
if __name__ == "__main__":
    
#%% Change Directory

    # Ensure Working Directory is the same as the folder
    os.getcwd()
    #os.chdir('[Your Directory]')
    
    #%% Load JSONs from a file
    
    # Load environment variables from .env file
    load_dotenv()
    
    
    # You can either call the filename from the .env file, uncomment based
    # on your storage type
    #filename = os.getenv('JSON_STORAGE') # Computer Vision
    filename = os.getenv('JSON_STORAGE_FORM_RECOGNIZER') # Form Recognizer    
    
    # Or comment the above line of code out and replace filename with the
    # string literal of the file name you desire
    # Open the file and read its contents
    with open(filename, 'r') as f:
        file_contents = f.read()
    
    # Change the separator as required if you have a different json file
    
    # Split the file contents into individual JSON payloads
    json_payloads = file_contents.strip().split('\n')
    
    # Parse each JSON payload into a dictionary
    json_data_list = [json.loads(payload) for payload in json_payloads]
    
    
    #%% Fuzzy Matching
    
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