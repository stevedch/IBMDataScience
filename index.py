import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
else:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'historical_data_table table'})

    rows = table.find_all('tr')[1:]
    data = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 2:
            date = cols[0].text.strip()
            revenue = cols[1].text.strip().replace('$', '').replace(',', '')
            if revenue and revenue != '':  # filtrar vacíos
                try:
                    data.append([date, float(revenue)])
                except ValueError:
                    continue

    df = pd.DataFrame(data, columns=['Fecha', 'Ingresos (en millones USD)'])
    print(df)