#!/usr/bin/python
import time, os
from sys import platform
from selenium import webdriver
from .geckodriver_profile import GeckodriverProfile
from .chromedriver_options import ChromedriverOptions

class WebDriverController:
	driver: object = None

	def __init__(self, driver_name: str, proxy: str = None) -> None:
		if driver_name == "firefox":
			path = None
			if platform == "linux":
				path = os.path.normpath(f'{os.getcwd()}/webdrivers/geckodriver')
			if platform == "win32":
				path = os.path.normpath(f'{os.getcwd()}/webdrivers/geckodriver.exe')
			if path is not None:
				geckodriver_profile = GeckodriverProfile(proxy=proxy)
				self.driver = webdriver.Firefox(executable_path=path, firefox_profile=geckodriver_profile.firefox_profile)
				self.driver.set_window_position(0, 0)
				self.driver.set_window_size(1920, 1080)

		if driver_name == "chrome":
			path = None
			if platform == "linux":
				path = os.path.normpath(f'{os.getcwd()}/webdrivers/chromedriver')
			if platform == "win32":
				path = os.path.normpath(f'{os.getcwd()}/webdrivers/chromedriver.exe')
			if path is not None:
				chromedriver_options = ChromedriverOptions(proxy=proxy)
				self.driver = webdriver.Chrome(executable_path=path, options=chromedriver_options.chrome_options)
				self.driver.set_window_position(0, 0)
				self.driver.set_window_size(1920, 1080)
		
	def scroll_to_element(self, element):
		location = element.location
		window_size = self.driver.get_window_size()
		options = {
			"top": location["y"] - window_size["height"]/2,
			"left": 0,
			"behavior": "smooth"
		}
		self.driver.execute_script(f'window.scrollTo({options})')
		time.sleep(1)
		
	def click_on_element(self, element):
		location = element.location
		size = element.size
		action = webdriver.common.action_chains.ActionChains(self.driver)
		action.move_to_element_with_offset(element, 5, 5)
		action.click()
		action.perform()
		time.sleep(1)

	def hide_element(self, element):
		self.driver.execute_script("arguments[0].style.width = 200 !important;", element)

	def bypass_hcaptcha(self):
		pass

	def get_cookies(self):
		cookies = self.driver.get_cookies()
		for cookie in cookies:
		    print(cookie)

def main():
	pass

if __name__ == "__main__":
	main()