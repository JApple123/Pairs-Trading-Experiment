import bs4 as bs
import pickle
import requests


def save_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    headers = {
        "User-Agent": "PairLab/1.0 (student quantitative finance research)"
    }

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", id="constituents")

    if table is None:
        raise ValueError("Could not find the S&P 500 constituents table.")

    tickers = []

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")

        if cells:
            ticker = cells[0].get_text(strip=True)
            ticker = ticker.replace(".", "-")
            tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(f"Saved {len(tickers)} tickers.")
    print(tickers[:10])

    return tickers


tickers = save_sp500_tickers()