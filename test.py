import requests
import urllib.request
import time
from bs4 import BeautifulSoup

def main():
	url = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page1/?filter=ALL_REVIEWS#link'
	page1 = requests.get(url)

	if page1.status_code == 200:
		print("got page 1!")
		f = open("ratings.txt", "w+")
		f.write(page1.text)
	else:
		print("didn't get it :(")
		exit(1)


if __name__ == "__main__":
	main()