import pytest
import requests
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from review_analysis import *

class TestSentimentAnalysis:
	"""Test sentiment analysis part of program."""

	def test_clean_review_links(self):
		"""Test clean_review with links."""
		test_string = "OMG this car dealership is sooo amazing. also check out my insta https://www.instagram.com/?hl=en"
		answer = "OMG this car dealership is sooo amazing also check out my insta"
		analyzer = CarReviewAnalyzer()
		cleaned_string = analyzer.clean_review(test_string)
		assert(answer == cleaned_string)

	def test_clean_review_characters(self):
		"""Test clean_review with special characters."""
		test_string = "Hi i love this #dealership# because they have great service!!"
		answer = "Hi i love this dealership because they have great service"
		analyzer = CarReviewAnalyzer()
		cleaned_string = analyzer.clean_review(test_string)
		assert(answer == cleaned_string)

	def test_clean_review_twitterhandle(self):
		"""Test clean_review with special handles."""
		test_string = "Had great service. also follow me on twitter @carsareawesome"
		answer = "Had great service also follow me on twitter"
		analyzer = CarReviewAnalyzer()
		cleaned_string = analyzer.clean_review(test_string)
		assert(answer == cleaned_string)

	def test_get_review_sentiment(self):
		"""Test get_review_sentiment."""
		num_reviews = 10
		f = open('tests/testdata/testpage.txt')
		page = f.read()
		analyzer = CarReviewAnalyzer()
		analyzer.parse_html(page)
		analyzer.get_review_sentiment()
		assert(num_reviews == len(analyzer.top_users))

	def test_sort_results(self):
		"""Test sort_results."""
		sorted_ratings = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.4, 3.2, 2.5, 1.3]
		f = open('tests/testdata/testpage3.txt')
		page = f.read()
		analyzer = CarReviewAnalyzer()
		analyzer.parse_html(page)
		analyzer.get_review_sentiment()
		analyzer.sort_results()
		# compare to right answer
		i = 0
		for u in analyzer.top_users:
			assert(sorted_ratings[i] == u['rating'])
			i += 1
