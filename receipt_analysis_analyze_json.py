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
ExclusionList = ['Total', 'Subtotal', 'Multibuy']
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
def approximate_string_matching(string):
    # First, check if word matches anything in the exclusion list that could be
    # misinterpreted as a product
    #match_list = difflib.get_close_matches(string, ExclusionList, n=1, cutoff=0.9)
    #if match_list:
#        similarity_ratio = difflib.SequenceMatcher(None, string, match_list[0]).ratio()
   #     matchList.append([string, match_list, similarity_ratio])        
  #  else: # Check matches
        shop_match_list = difflib.get_close_matches(string, [shop[1] for shop in ShopList], n=3, cutoff=0.6)
        product_match_list = difflib.get_close_matches(string, [product[1] for product in ProductList], n=3, cutoff=0.6)
        
        if len(shop_match_list) > 0 and len(product_match_list) > 0:
            shop_best_match = shop_match_list[0]
            shop_similarity_ratio = difflib.SequenceMatcher(None, string, shop_best_match).ratio()
            shop_match_prob = 1 - (1 - shop_similarity_ratio) ** len(shop_best_match)
            product_best_match = product_match_list[0]
            product_similarity_ratio = difflib.SequenceMatcher(None, string, product_best_match).ratio()
            product_match_prob = 1 - (1 - product_similarity_ratio) ** len(product_best_match)
            
            if shop_match_prob > product_match_prob:
                best_match = shop_best_match
                similarity_ratio = shop_similarity_ratio
                match_type = 'shop'
            else:
                best_match = product_best_match
                similarity_ratio = product_similarity_ratio
                match_type = 'product'
        elif len(shop_match_list) > 0:
            best_match = shop_match_list[0]
            similarity_ratio = difflib.SequenceMatcher(None, string, best_match).ratio()
            match_type = 'shop'
        elif len(product_match_list) > 0:
            best_match = product_match_list[0]
            similarity_ratio = difflib.SequenceMatcher(None, string, best_match).ratio()
            match_type = 'product'
        else:
            return None
        
        print(f'Best match: {best_match}, match probability: {similarity_ratio:.2f}')
        best_match_tuple = (string, best_match, levenshtein_distance(string, best_match))
        print(best_match_tuple)
        print(f'Matching {best_match_tuple[0]} to {best_match_tuple[1]} with a Levenshtein distance of {best_match_tuple[2]}')
        matchList.append([string, best_match_tuple[1], similarity_ratio, best_match_tuple[2]])
        return best_match_tuple, match_type



# Define a function to process the JSON payload and update the lists
def process_json(json_payload):
    if __name__ == '__main__':
        for recognized_text in json_payload['analyzeResult']['readResults']:
            for line in recognized_text['lines']:
                for word in line['words']:
                    print(f'Matching to ' + word['text'])
                    # Check if the word matches a shop or product name
                    match = approximate_string_matching(word['text'])
                    print(f'Match: {match}')
                    if match:
                        match_text = match[0][1]
                        print(f'Match Text: {match_text}')
                        match_type = match[1]
                        print(f'Match Type: {match_type}')
                        match_id = [item[0] for item in ShopList+ProductList if item[1]==match_text][0]
                        print(f'Match ID: {match_id}')
                        match_distance = match[0][2]
                        if match_distance > 0:
                            if match_type == "shop":
                                ShopList.append((match_id, match[0][0]))
                            elif match_type == "product":
                                ProductList.append((match_id, match[0][0]))
                            writer.writerow([match_type, match_id, match[0][0], match_text, match_distance])
                        else:
                            writer.writerow([match_type, match_id, match[0][0], match_text, "exact match"])

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
    filename = os.getenv('JSON_STORAGE') # Computer Vision
    #filename = os.getenv('JSON_STORAGE_FORM_RECOGNIZER') # Form Recognizer    
    
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