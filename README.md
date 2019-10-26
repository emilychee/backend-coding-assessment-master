# “A Dealer For the People”

The KGB has noticed a resurgence of overly excited reviews for a McKaig Chevrolet Buick, a dealership they have planted in the United States. In order to avoid attracting unwanted attention, I've created a Python program to scrape reviews for this dealership from DealerRater.com and uncover the top three worst offenders of these overly positive endorsements.

What this program does:

- 1 scrapes the first five pages of reviews
- 2 identifies the top three most “overly positive” endorsements
- 3 outputs these three reviews to the console, in order of severity

## Getting Started

To run this program, you will need Python 3.5.2 and pip installed on your machine before you complete any of the other steps.

1. Clone this repository.
```bash
git clone https://github.com/emilychee/backend-coding-assessment-master.git
```

2. Install the following packages: re, requests, bs4, and textblob. Use the pip package manager to do this.

```bash
pip install re requests bs4 textblob
```

## Usage

To run this program:
```bash
python3 review_analysis.py
```

## Running the Tests

Install pytest, pydocstyle, pycodestyle and the sh library using pip.
```bash
pip3 install pytest pydocstyle pycodestyle sh
```

To run the tests, you must be in the backend-coding-assessment-master directory.
To run all the tests at once:
```bash
pytest -v
```
To run a single test file:
```bash
pytest -v tests/<filename_of_test>
```
For example:
```bash
pytest -v tests/test_python_style.py
```

## Criteria for Rating Reviews

My first step was to weed out the recommendations that weren't consistent (i.e. the person left high ratings but didn't recommend the dealer or vice versa). If the person left a rating greater than or equal to 2.5 and didn't recommend the dealer, I discarded that review. Similarly, if the person left a rating of less than 2.5 and did recommend the dealer, I discarded that review.

I then did sentiment analysis on the remaining reviews with help from the textblob library. Textblob uses a Movie Reviews dataset in which the reviews had been labelled as positive or negative. Positive and negative features were then extracted from the reviews and trained on Naive Bayes Classifier. The sentiment of the text is then classified using its polarity score. The polarity score is a value that ranges from -1 to 1, where the range [-1, 0) is a negative sentiment, 0 is a neutral sentiment and the range (0, 1] is a very positive sentiment.

At first, I sorted reviews in decreasing order by polarity score, but I noticed that a lot of the reviews with five star ratings got low polarity scores. After looking through some of those reviews, I observed that some of those reviews talked about past negative experiences and how this new experience changed their mind. However, the negative words tanked the polarity score even though it was actually a positive review. This is why I decided to make the assumption that people who leave high dealership ratings also leave positive reviews, even if it can't be detected by the polarity score.

For the reasons stated above, I sorted reviews first by their rating (in decreasing order) and then broke ties with polarity scores (in decreasing order). 