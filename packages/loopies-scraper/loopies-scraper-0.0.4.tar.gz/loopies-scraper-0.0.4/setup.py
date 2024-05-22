from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Web scraper for basic and/or list of pages scraping'
LONG_DESCRIPTION = 'Wrapper for Selenium WebDriver and its configuration to turn it into web scraper to scrape list of pages or to use it as prebuilt scraper'

# Setting up
setup(
    name="loopies-scraper",
    version=VERSION,
    author="tmspsk",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(exclude=["tests*"]),
    install_requires=['selenium', 'fake_useragent'],
    keywords=['python', 'scraper', 'multiprocess scraper', 'list', 'selenium webdriver'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
