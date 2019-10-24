import requests
import urllib.request
import time
from bs4 import BeautifulSoup

def find_rating(rating_element):
	# put all classes into dictionary
	classes = {}
	for element in rating_element["class"]:
		classes[element] = 1

	# check which rating it is
	if "rating-50" in classes:
		return 5
	elif "rating-40" in classes:
		return 4
	elif "rating-30" in classes:
		return 3
	elif "rating-20" in classes:
		return 2
	elif "rating-10" in classes:
		return 1
	else:
		return -1


def main():
	reviews = {}
	top_users = {}

	url = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page1/?filter=ALL_REVIEWS#link'
	page1 = requests.get(url)

	if page1.status_code == 200:
		print("got page 1!")
	else:
		print("didn't get it :(")
		exit(1)

	soup = BeautifulSoup(page1.text, "html.parser")
	for review in soup.findAll('div', attrs={'class': 'review-entry'}):
		user = review.find('span', attrs={'class': 'italic'}).text.split()[1]
		rating_element = review.find('div', attrs={'class': 'rating-static'})
		rating = find_rating(rating_element)
		content = review.find('p', attrs={'class': 'review-content'}).text
		recommend = review.find('div', attrs={'class': 'boldest'}).text.strip()
		
		print(rating)
		if user not in reviews:
			reviews[user] = {"review": content, "rating": rating, "recommend": recommend}
	
	


if __name__ == "__main__":
	main()