# Marketing Campaign Insights Generator

A Python tool that reads marketing campaign data, cleans it, stores it in a SQL database, calculates key metrics, and uses the Gemini API to generate a performance summary and ad copy suggestions.

## What it does
- Cleans campaign data with pandas (removes duplicates, fills missing values)
- Stores data in SQLite and runs SQL queries
- Calculates CTR, CPC, conversion rate and cost per conversion
- Sends metrics to an LLM API as JSON and receives structured JSON back
- Saves the results as a markdown report

## Tech used
Python, pandas, SQL (SQLite), Gemini API, JSON

## How to run
1. Install Python 3.
2. Install the libraries: `pip install pandas google-genai`
3. Get a Gemini API key from Google AI Studio and save it as an environment variable named GEMINI_API_KEY.
4. Run: `python main.py`
5. Open `report.md` to see the output.

## Sample output
See `report.md` in this repo.
