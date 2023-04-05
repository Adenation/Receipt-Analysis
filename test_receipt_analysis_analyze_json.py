# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 05:54:53 2023

@author: Adenation
"""
#%% Imports
import unittest
from receipt_analysis_analyze_json import (levenshtein_distance, 
    approximate_string_matching, process_json)
from receipt_analysis_analyze_json import (ShopList, ProductList)
#%% Test Classes
class TestLevenshteinDistance(unittest.TestCase):

    def test_levenshtein_distance_same_strings(self):
        s1 = "Apples"
        s2 = "Apples"
        self.assertEqual(levenshtein_distance(s1, s2), 0)

    def test_levenshtein_distance_different_lengths(self):
        s1 = "Tomatoes"
        s2 = "Tomato"
        self.assertEqual(levenshtein_distance(s1, s2), 2)

    def test_levenshtein_distance_different_strings(self):
        s1 = "Tomatoes"
        s2 = "Potatoes"
        self.assertEqual(levenshtein_distance(s1, s2), 2)


class TestApproximateStringMatching(unittest.TestCase):

    def test_approximate_string_matching_no_match(self):
        string = "apple"
        options_list = ["banana", "orange", "grape"]
        self.assertEqual(approximate_string_matching(string, options_list), None)

    def test_approximate_string_matching_with_match(self):
        string = "appel"
        options_list = ["apple", "banana", "orange", "grape"]
        self.assertEqual(approximate_string_matching(string, options_list), (string, "apple", 2))


class TestProcessJSON(unittest.TestCase):

    def test_process_json_no_matches(self):
        json_payload = {
            "analyzeResult": {
                "readResults": [
                    {
                        "lines": [
                            {
                                "words": [
                                    {
                                        "text": "fufu"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        self.assertEqual(len(ShopList), 6)
        self.assertEqual(len(ProductList), 77)
        process_json(json_payload)
        self.assertEqual(len(ShopList), 6)
        self.assertEqual(len(ProductList), 77)

    def test_process_json_one_product_match(self):
        json_payload = {
            "analyzeResult": {
                "readResults": [
                    {
                        "lines": [
                            {
                                "words": [
                                    {
                                        "text": "apple"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        self.assertEqual(len(ShopList), 6)
        self.assertEqual(len(ProductList), 77)
        process_json(json_payload)
        self.assertEqual(len(ShopList), 6)
        self.assertEqual(len(ProductList), 77)
        self.assertEqual(ProductList[0], (1, "Apples"))
        
    def test_process_json_one_shop_match(self):
        json_payload = {
            "analyzeResult": {
                "readResults": [
                    {
                        "lines": [
                            {
                                "words": [
                                    {
                                        "text": "Tesco"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        self.assertEqual(len(ShopList), 6)
        self.assertEqual(len(ProductList), 77)
        process_json(json_payload)
        self.assertEqual(len(ShopList), 6)
        self.assertEqual(len(ProductList), 77)
        self.assertEqual(ShopList[0], (1, "Tesco"))
#%% Execute Tests
if __name__ == '__main__':
    unittest.main()
