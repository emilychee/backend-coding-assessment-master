# “A Dealer For the People”

The KGB has noticed a resurgence of overly excited reviews for a McKaig Chevrolet Buick, a dealership they have planted in the United States. In order to avoid attracting unwanted attention, I've created a Python program to scrape reviews for this dealership from DealerRater.com and uncover the top three worst offenders of these overly positive endorsements.

What this program does:

- 1 scrapes the first five pages of reviews
- 2 identifies the top three most “overly positive” endorsements (using criteria of your choosing, documented in the README)
- 3 outputs these three reviews to the console, in order of severity

## Getting Started

To run this program, you need Python 3.5.2 and pip installed on your machine.

Clone this repository.
```bash
git clone https://github.com/emilychee/backend-coding-assessment-master.git
```

After cloning the repository, you will need to install the following packages: re, requests, bs4, and textblob.
Use the pip package manager to do this.

```bash
pip install re requests bs4 textblob
```

## Usage

To run this program:
```bash
python3 review_analysis.py
```