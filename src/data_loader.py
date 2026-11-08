from pathlib import Path
import pandas as pd
import yfinance as yf

# 1. Define the assets 
TICKERS = ['XLK', 'XLF', 'XLE', 'XLI', 'XLP'] # ETFs for technology, financials, energy, industrials, and consumer staples

# 2. Define the historical period
START_DATE = '2015-01-01'
END_DATE = '2026-10-28'

# 3. Define the output directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'raw'

def download_prices():
    """Download daily adjusted ETF prices"""

    print('Downloading historical ETF prices...')

    data = yf.download(
        tickers=TICKERS,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,
        progress=False,
        threads=False,
    )

    if data.empty:
        raise RuntimeError('No data was downloaded.')

    # Select adjusted closing prices
    prices = data['Close'].copy()

    # Ensure consistent column ordering
    prices = prices.reindex(columns=TICKERS)

    # Remove dates with missing values
    prices = prices.dropna()
    
    if prices.empty:
        raise RuntimeError('No complete observations available.')

    # Create output folder
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / 'etf_prices.csv'
    prices.to_csv(output_path, index_label='Date')

    print(f'Saved data to: {output_path}')
    print(f'Dataset shape: {prices.shape}')
    print(prices.head())

    return prices


if __name__ == '__main__':
    download_prices()

# %%
prices = pd.read_csv(
    "/Users/ady/Proyectos/bayesian-basket-trading/data/raw/etf_prices.csv",
    index_col=0,
    parse_dates=True
)

print("Dimensiones:", prices.shape)
print("Primera fecha:", prices.index.min())
print("Última fecha:", prices.index.max())

print("\nValores faltantes:")
print(prices.isna().sum())

print("\nPrimeras 5 observaciones:")
print(prices.head())