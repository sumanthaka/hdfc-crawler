# Web Scraping with Scrapy
This is a web scraping project that extracts information about credit card products from the HDFC Bank website using Scrapy. The extracted information includes the name of the credit card, the annual fee, the reward points or cashback percentage per Rs. 100 spent, lounge access benefits, milestone benefits, and card fee reversal conditions.

## Requirements
- Python 3.x
- Scrapy

## Usage
1. Clone the repository:
`git clone https://github.com/sumanthaka/hdfc-crawler.git`

2. Navigate to the project directory:
`cd hdfc-crawler`

3. Run the spider:
`run`  

This will scrape the HDFC Bank website, extract the credit card information, and save it to a CSV file named `creditcard.csv`.

## Output
The spider will extract the following information for each credit card:
- Card name
- Annual fee
- Reward points or cashback percentage per Rs. 100 spent
- Lounge access benefits
- Milestone benefits
- Card fee reversal conditions (if any)
The output will be saved to a CSV file named cards.csv in the project directory.
