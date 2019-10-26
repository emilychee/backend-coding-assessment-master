"""Test web scraping functions."""

import pytest
import requests
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from review_analysis import *

class TestWebScraping:
	"""Test web scraping and HTML parsing."""

	def test_parse_html_valid_inputs(self):
		"""Test HTML parsing of page."""
		#answer key
		answers = {'B Muench', 'Britt87', 'dcarlile2', 'goldbergjan',
				   'Marquita Phelps', 'Megan m', 'Mekmo52091', 'Brittani Griffin',
				   'Patti Stinson', 'Jessica cargil'}
		# open test page
		f = open('tests/testdata/testpage.txt')
		page = f.read()
		# pass to function
		analyzer = CarReviewAnalyzer()
		analyzer.parse_html(page)
		# compare answers
		for user in analyzer.reviews:
			assert(user in answers)
		# check that they have same number of users too
		assert(len(analyzer.reviews) == len(answers))

	def test_parse_html_invalid_inputs(self):
		"""Test HTML parsing of page."""
		#answer key
		answers = {'dcarlile2', 'goldbergjan',
				   'Marquita Phelps', 'Megan m', 'Mekmo52091',
				   'Brittani Griffin', 'Patti Stinson', 'Jessica cargil'}
		# open test page
		f = open('tests/testdata/testpage2.txt')
		page = f.read()
		# pass to function
		analyzer = CarReviewAnalyzer()
		analyzer.parse_html(page)
		# compare answers
		for user in analyzer.reviews:
			assert(user in answers)
		# check that they have same number of users too
		assert(len(analyzer.reviews) == len(answers))

	def test_find_rating_00(self):
		"""Test find_rating with rating of 0."""
		# test data
		rating_element = {"class": ['rating-static', 'visible-xs', 'pad-none',
									'margin-none', 'rating-00', 'pull-right']}
		answer = 0.0
		# set up
		analyzer = CarReviewAnalyzer()
		# compare
		assert(answer == analyzer.find_rating(rating_element))

	def test_find_rating_32(self):
		"""Test find_rating with rating of 3.2."""
		# test data
		rating_element = {"class": ['rating-static', 'visible-xs', 'pad-none',
									'margin-none', 'rating-32', 'pull-right']}
		answer = 3.2
		# set up
		analyzer = CarReviewAnalyzer()
		# compare
		assert(answer == analyzer.find_rating(rating_element))

	def test_parse_username_spaces(self):
		"""Test parse_username with username with spaces."""
		user_element_spaces = "- B Muench"
		user = "B Muench"
		analyzer = CarReviewAnalyzer()
		assert(user == analyzer.parse_username(user_element_spaces))

	def test_parse_username_3parts(self):
		"""Test parse_username with 3-part username."""
		user_3_parts = "- E D C"
		user = "E D C"
		analyzer = CarReviewAnalyzer()
		assert(user == analyzer.parse_username(user_3_parts))

	def test_parse_username_hyphen(self):
		"""Test parse_username with username with hyphen."""
		user_hyphen = "- Em-123"
		user = "Em-123"
		analyzer = CarReviewAnalyzer()
		assert(user == analyzer.parse_username(user_hyphen))