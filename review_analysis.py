import re
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

class CarReviewAnalyzer():
    def __init__(self, num_reviews_print=0, url_list=[]):
        """CarReviewAnalyzer constructor."""
        self.num_reviews_print = num_reviews_print
        self.url_list = url_list
        self.reviews = {}
        self.top_users = []

    def find_rating(self, rating_element):
        rating_string = rating_element["class"][4].split('-')[1]
        rating = int(rating_string) / 10
        return rating

    def parse_username(self, user_element):
        temp = user_element.text.split('-')[1]
        user = temp.strip()
        return user

    def get_reviews(self):
        """Scrapes pages and puts reveiws into dictionary."""
        for url in self.url_list:
            # try to scrape each page
            try:
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
                user = self.parse_username(user_element)
                rating_element = review.find('div', attrs={'class': 'rating-static'})
                rating = self.find_rating(rating_element)
                content = review.find('p', attrs={'class': 'review-content'}).text
                recommend = review.find('div', attrs={'class': 'boldest'}).text.strip()
                date = review.find('div', attrs={'class': 'font-20'}).text
                title = review.find('h3').text
                # only save reviews that are consistent
                if (rating >= 2.5 and recommend == "Yes") or (rating < 2.5 and recommend == "No"):
                    if user not in self.reviews:
                        self.reviews[user] = {"review": content, "rating": rating, "recommend": recommend,
                                         "date": date, "title": title}

    def clean_review(self, review):
        # cleans the review by removing links and special characters
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", review).split())

    def get_review_sentiment(self):
        # calculate sentiment score of each review
        for user in self.reviews:
            analysis = TextBlob(self.clean_review(self.reviews[user]['review']))
            score = analysis.sentiment.polarity
            self.top_users.append({"user": user, "rating": self.reviews[user]["rating"], "sentiment": score})

    def sort_results(self):
        self.top_users = sorted(self.top_users, key=lambda i: (-i['rating'], -i['sentiment']))

    def print_results(self):
        # sort
        self.sort_results()
        # print
        print("TOP " + str(self.num_reviews_print) + " OVERLY POSITIVE REVIEWS")
        print("--------------------------------------------------------------------")
        for i in range(self.num_reviews_print):
            print(self.reviews[self.top_users[i]["user"]]["date"])
            print("rating: " + str(self.top_users[i]["rating"]) + "/5.0")
            print(self.top_users[i]["user"] + ": " + self.reviews[self.top_users[i]["user"]]["title"])
            print(self.reviews[self.top_users[i]["user"]]["review"])
            print("--------------------------------------------------------------------")

def main():
    NUM_REVIEWS_PRINT = 3
    url_list = ['https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page1/?filter=ALL_REVIEWS#link',
                'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page2/?filter=ALL_REVIEWS#link',
                'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page3/?filter=ALL_REVIEWS#link',
                'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page4/?filter=ALL_REVIEWS#link',
                'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page5/?filter=ALL_REVIEWS#link']

    analyzer = CarReviewAnalyzer(NUM_REVIEWS_PRINT, url_list)
    analyzer.get_reviews()
    analyzer.get_review_sentiment()
    analyzer.print_results()
    # scrape reviews, clean them, and get sentiment score
    # then sort based off of rating, then sentiment score
    """reviews = get_reviews(PAGES_TO_SCRAPE)
    top_users = get_review_sentiment(reviews)
    top_users = sorted(top_users, key=lambda i: (-i['rating'], -i['sentiment']))

    # printing
    print("TOP " + str(NUM_REVIEWS_PRINT) + " OVERLY POSITIVE REVIEWS")
    print("--------------------------------------------------------------------")
    for i in range(NUM_REVIEWS_PRINT):
        print(reviews[top_users[i]["user"]]["date"])
        print("rating: " + str(top_users[i]["rating"]) + "/5.0")
        print(top_users[i]["user"] + ": " + reviews[top_users[i]["user"]]["title"])
        print(reviews[top_users[i]["user"]]["review"])
        print("--------------------------------------------------------------------")"""


if __name__ == "__main__":
    main()