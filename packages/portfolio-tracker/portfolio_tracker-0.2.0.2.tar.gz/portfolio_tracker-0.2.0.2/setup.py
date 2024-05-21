from setuptools import setup, find_packages
import os
import codecs

# version = '{{VERSION_PLACEHOLDER}}'
version = '0.2.0.2'

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='portfolio_tracker',
    python_requires='>=3.10',
    packages=find_packages(include=['portfolio_tracker']),
    version=version,
    description='A portfolio tracker library, that allows to track a portfolio of stocks and their performance.',
    author='Poli Luca',
    install_requires=['pandas', 'yfinance', 'numpy', 'pandas_market_calendars', 'openpyxl'],
    package_data={'docs': ['manager.html', 'price_repo.html', 'utils.html', 'xlsx_example.xlsx', 'example.ipynb']},

    long_description=long_description,
    long_description_content_type="text/markdown",
)
