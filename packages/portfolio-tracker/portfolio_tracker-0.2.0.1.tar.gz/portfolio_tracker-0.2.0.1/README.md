
# Stock Portfolio Tracker

This library provides a set of Python modules for managing and tracking a stock portfolio.

## Description

The project includes the following modules:

- `price_repo.py`: Manages the stock prices repository, which is a csv file containing the prices of the stocks. This is used to avoid downloading the prices every time the program is executed.
- `manager.py`: Contains the portfolio class and the functions to manage it. It allows for portfolio rebalancing, rolling forward, and other operations.
- `utils.py`: Includes utility functions used in the project, such as functions for computing returns and rolling dates to business days.

For a more detailed documentation check the `docs` folder on GitHub: https://github.com/LucaPoli59/PortfolioTrackerLib/tree/master/docs

## Installation

To install the library, run the following command:

```bash 
pip install portfolio_tracker
```

## Usage

To use this library, import the necessary modules and use the provided classes and functions.

For example, the following code shows how to use the Portfolio class to manage a stock portfolio:

```python
import os
from portfolio_tracker.price_repo import PriceRepo
from portfolio_tracker.manager import Portfolio

#Define the path to the stock prices repository and the portfolios
STOCK_PRICES_REPO = os.path.join(os.path.dirname(os.getcwd()), 'data', 'stock_repo.csv') # Example of a price repository path
STOCK_PRICES_REPO_OPEN = os.path.join(os.path.dirname(os.getcwd()), 'data', 'stock_repo_open.csv') # Example of a price repository path
PORTFOLIOS_PATH = os.path.join(os.path.dirname(os.getcwd()), 'data', 'portfolios') # Example of a portfolio path

# Initialize the PriceRepo objects
price_repo = PriceRepo(STOCK_PRICES_REPO, 'Adj Close')
price_repo_open = PriceRepo(STOCK_PRICES_REPO_OPEN, 'Open')

# Initialize the Portfolio object
portfolio_path1 = os.path.join(PORTFOLIOS_PATH, "portfolio_10_2023.xlsx")
portfolio = Portfolio(portfolio_path1, price_repo, price_repo_open)

# Roll the portfolio forward to the next month
portfolio.roll_forward("1M")
print(portfolio.get_weights())

# Rebalance the portfolio
portfolio_path2 = os.path.join(PORTFOLIOS_PATH, "portfolio_01_2024.xlsx")
portfolio.rebalancing_from_file(portfolio_path2)

# We can roll again the portfolio forward
portfolio.roll_forward(20)

# Print the weights and returns
print(portfolio.get_weights(normalize=True))
print(portfolio.get_returns(weighted=True))
```

For more examples, check the `example.ipynb` notebook.


## Development

This library is meant to be a simple tool for tracking a stock portfolio, it has been developed by Luca Poli from the quant team of the MIURA group, for the group itself.

For any bug or suggestion, please contact me through discord at https://discordapp.com/users/326499540540588032