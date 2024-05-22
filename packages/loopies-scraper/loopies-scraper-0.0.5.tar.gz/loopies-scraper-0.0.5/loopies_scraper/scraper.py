#!/usr/bin/python
from .webdriver_controller import WebDriverController

class Scraper(WebDriverController):
    def __init__(self, driver_name: str, proxy: str = None) -> None:
        super().__init__(driver_name, proxy)

def main():
    pass

if __name__ == "__main__":
    main()