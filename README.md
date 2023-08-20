# Flask + Vercel

This example shows how to use Flask 2 on Vercel with Serverless Functions using the [Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python).

## Demo

https://mini-scrapper-zeabdelkhalek.vercel.app/

## How it Works

- This project utilizes Flask along with the Selenium library for web scraping.
- It automatically downloads the appropriate ChromeDriver based on the system's architecture and OS.
- With the /scrape endpoint, you can fetch the HTML content of any webpage by supplying a URL.

## Running Locally

```bash
npm i -g vercel
vercel dev
```

Your Flask application is now available at `http://localhost:3000`.

## Scraping a URL

To scrape a webpage:

1. Make a POST request to /api/scrape.
2. Include JSON data with a url key pointing to the page you wish to scrape.

Example using curl:


```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://finance.yahoo.com/quote/TWLO/financials?p=TWLO"}' http://localhost:3000/scrape
```

This will return the HTML content of the provided URL.