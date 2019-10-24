import re
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from textblob import TextBlob

def find_rating(rating_element):
	rating_string = rating_element["class"][4].split('-')[1]
	rating = int(rating_string) / 10
	return rating

def parse_username(user_element):
	temp = user_element.text.split('-')[1]
	user = temp.strip()
	return user

def get_reviews(pages_to_scrape):
	reviews = {}
	for i in range(pages_to_scrape):
		# try to scrape each page
		try:
			index = str(i + 1)
			url = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page{}/?filter=ALL_REVIEWS#link'.format(index)
			page = requests.get(url)
		except requests.exceptions.ConnectionError:
			print("CONNECTION ERROR: Connection was refused. Double-check that you have the correct URL.")
		except requests.exceptions.Timeout:
			print("TIMEOUT ERROR: The request timed out. Re-run program to try again.")
		except requests.exceptions.TooManyRedirects:
			print("TOO MANY REDIRECTS ERROR: This URL is most likely bad. Try a new one.")
		except requests.exceptions.RequestException as e:
			print(e)

		# put data into a dictionary
		soup = BeautifulSoup(page.text, "html.parser")
		for review in soup.findAll('div', attrs={'class': 'review-entry'}):
			user_element = review.find('span', attrs={'class': 'italic'})
			user = parse_username(user_element)
			rating_element = review.find('div', attrs={'class': 'rating-static'})
			rating = find_rating(rating_element)
			content = review.find('p', attrs={'class': 'review-content'}).text
			recommend = review.find('div', attrs={'class': 'boldest'}).text.strip()
			# only save reviews that are consistent
			if (rating >= 2.5 and recommend == "Yes") or (rating < 2.5 and recommend == "No"):
				if user not in reviews:
					reviews[user] = {"review": content, "rating": rating}

	return reviews

def clean_review(review):
	# cleans the review by removing links and special characters
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", review).split())

def get_review_sentiment(reviews):
	scores = []
	# calculate sentiment score of each review
	for user in reviews:
		analysis = TextBlob(clean_review(reviews[user]['review']))
		score = analysis.sentiment.polarity
		scores.append({"user": user, "rating": reviews[user]["rating"], "sentiment": score})
	return scores

def main():
	PAGES_TO_SCRAPE = 5

	reviews = get_reviews(PAGES_TO_SCRAPE)
	top_users = get_review_sentiment(reviews)
	top_users = sorted(top_users, key=lambda i: (-i['rating'], -i['sentiment']))

	for u in top_users:
		print(u)


if __name__ == "__main__":
	main()