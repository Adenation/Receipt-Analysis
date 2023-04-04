# Receipt-Analysis
Python Scripts to generate receipts, utilize Microsoft Azure Computer Vision API's OCR tool to analyze the receipts and then use various algorithms to determine matches.

# Description

The Scripts have been split into 3 parts, with an additional script 'Receipt-Analysis-Generate-env' to generate your own .env file as required to store
your subscription key, endpoint and filename to persist JSON payloads.

The scripts can be run individually for each step in the process

# Receipt-Analysis-Generate-Receipts

This script allows you to create your own receipts using the PIL library.

Near the top of the script you can customize the number of receipts to generate from a selected list of shops and products.

# Receipt-Analysis-Generate-JSON

This script will take your subscription key and endpoint and contact the Microsoft Azure Computer Vision API's OCR tool to
read the .png receipts you have generated or created using another tool and produce JSON payloads with the analysis.
The script has delays to allow users using the free plan to not exceed the 20 calls per minute as well as print off
logs to show if there are errors in analyzing a particular receipt.

The script will then store these JSON payloads in one file with a newline separator '\n'.

# Receipt-Analysis-Analyze-JSON

This script will process all of the JSON payloads, attempt to match the analyzed words to words in the lists and if the match is close but not
already present will append it to the list. For example TE5CO --> TESCO will be added with the same id.

This script is still being optimized so that the matching algorithm is as accurate as possible.
