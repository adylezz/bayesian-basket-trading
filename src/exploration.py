from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'etf_prices.csv'
RESULTS_DIR = PROJECT_ROOT / 'results'

def main():
    prices = pd.read_csv(
        DATA_PATH,
        index_col='Date',
        parse_dates=True
    )

    print('\nDataset information:')
    print(prices.info())

    print('\nMissing values:')
    print(prices.isna().sum())

    # Let's normalize each asset to 100 at the first observation
    normalized = (prices / prices.iloc[0]) * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    normalized.plot(ax=ax, linewidth=1.5)

    ax.set_title('Historical ETF prices - Base 100')
    ax.set_xlabel('Date')
    ax.set_ylabel('Normalized Price')
    ax.grid(alpha=0.3)

    plt.tight_layout()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        RESULTS_DIR / 'normalized_prices.png',
        dpi=200
    )

    plt.show()

if __name__ == '__main__':
    main()