# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:08:06 2023

@author: Adenation
"""
#%% Imports

import os
import random
from PIL import Image, ImageDraw, ImageFont

import barcode
from barcode import EAN13
from barcode.writer import ImageWriter

from io import BytesIO

#%% Change working directory if needed

#os.chdir('[Your Directory]')
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

fonts = ["arial.ttf", "georgia.ttf", "impact.ttf", "verdana.ttf"]

#%% Definitions

# Define method to generate random spelling errors
def generate_spelling_error(word):
    options = ['omit', 'repeat', 'o_to_0', '0_to_o', 'i_to_1', '1_to_i',
               'l_to_1', '1_to_l', 's_to_5', '5_to_s', 'blank']
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
    elif error_type == 'blank':
        index = random.randint(0, len(word) - 1)
        return word[:index] + ' ' + word[index + 1:]
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
    
def generate_receipts(receipts_to_generate, min_items, max_items,
                      min_quantity, max_quantity):
        
    # Define the width and height of the image
    image_width = 600
    image_height = 800
    padding = 20    
    
    
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
        num_items = random.randint(min_items, max_items)
        sub_total = 0
        
        
        # Draw the item details
        for i in range(num_items):
            # Choose a random item and quantity
            item, price = random.choice(items)
            
            # Randomly generate spelling errors
            item = generate_spelling_error(item)
            
            quantity = random.randint(min_quantity, max_quantity)
        
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
            
        # Generate barcode
        barcode_value = str(random.randint(1000000000000, 9999999999999))
        barcode_image = EAN13(barcode_value, writer=ImageWriter())
        barcode_pil_image = barcode_image.render()
        barcode_width, barcode_height = barcode_pil_image.size

        # Scale barcode to fit
        new_barcode_height = int(image_height/6)
        new_barcode_width = int(new_barcode_height * barcode_width / barcode_height)
        barcode_image = barcode_pil_image.resize((new_barcode_width, new_barcode_height))
        
        # Add the barcode to the image
        image.paste(barcode_image, (10, image_height - new_barcode_height - 20))
        # Draw the image
        image.save('receipt' + str(j) + '.png')

#%% Generate receipts

# Decide how many receipts you want to generate
receipts_to_generate = 30

# Customize Parameters of Receipt
min_items = 3
max_items = 7
min_quantity = 1
max_quantity = 5

generate_receipts(receipts_to_generate, min_items, max_items, min_quantity, max_quantity)


