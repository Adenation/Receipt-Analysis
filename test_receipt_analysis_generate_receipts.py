# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:25:56 2023

@author: Adenation
"""
import os
import unittest
import importlib
from unittest.mock import patch, MagicMock
from PIL import Image, ImageFont, ImageDraw

from receipt_analysis_generate_receipts import shops, items, addresses, fonts
from receipt_analysis_generate_receipts import generate_spelling_error, generate_receipts

#%%
class TestGenerateSpellingError(unittest.TestCase):
        
    def test_word_omit_0(self):
        with patch('random.choice', return_value='omit'), \
        patch('random.randint', return_value=1):
            result = generate_spelling_error('test')
            self.assertEqual(result, 'tst')
        
    def test_word_omit_1(self):   
        with patch('random.choice', return_value='omit'), \
        patch('random.randint', return_value=0):
            result = generate_spelling_error('test')
            self.assertEqual(result, 'est')
            
    def test_word_repeat_0(self):
        with patch('random.choice', return_value='repeat'), \
            patch('random.randint', return_value=0):
            result = generate_spelling_error('test')
            self.assertEqual(result, 'ttest')
            
    def test_word_repeat_1(self):
        with patch('random.choice', return_value='repeat'), \
            patch('random.randint', return_value=1):
            result = generate_spelling_error('test')
            self.assertEqual(result, 'teest')
            
    def test_word_o_to_0(self):
        with patch('random.choice', return_value='o_to_0'):
            result = generate_spelling_error('hello')
            self.assertEqual(result, 'hell0')
            
    def test_word_0_to_o(self):
        with patch('random.choice', return_value='0_to_o'):
            result = generate_spelling_error('100')
            self.assertEqual(result, '1oo')
            
    def test_word_i_to_1(self):
        with patch('random.choice', return_value='i_to_1'):
            result = generate_spelling_error('mississippi')
            self.assertEqual(result, 'm1ss1ss1pp1')
            
    def test_word_1_to_i(self):
        with patch('random.choice', return_value='1_to_i'):
            result = generate_spelling_error('1337')
            self.assertEqual(result, 'i337')
            
    def test_word_l_to_1(self):
        with patch('random.choice', return_value='l_to_1'):
            result = generate_spelling_error('hello')
            self.assertEqual(result, 'he11o')
            
    def test_word_1_to_l(self):
        with patch('random.choice', return_value='1_to_l'):
            result = generate_spelling_error('he11o')
            self.assertEqual(result, 'hello')
            
    def test_word_s_to_5(self):
        with patch('random.choice', return_value='s_to_5'):
            result = generate_spelling_error('mississippi')
            self.assertEqual(result, 'mi55i55ippi')
            
    def test_word_5_to_s(self):
        with patch('random.choice', return_value='5_to_s'):
            result = generate_spelling_error('5ausage5')
            self.assertEqual(result, 'sausages')
            
    def test_word_blank(self):
        with patch('random.choice', return_value='blank'), \
            patch('random.randint', return_value=0):
            result = generate_spelling_error('hello')
            self.assertEqual(result, ' ello')

#%%            
if __name__ == '__main__':
    unittest.main()

