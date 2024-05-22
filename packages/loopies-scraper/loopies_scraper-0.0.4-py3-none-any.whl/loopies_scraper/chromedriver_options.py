#!/usr/bin/python
from selenium.webdriver.chrome.options import Options as ChromeOptions
from .user_agent_generator import UserAgentGenerator

class ChromedriverOptions:
	chrome_options: ChromeOptions = None
	
	def __init__(self, proxy: str = None) -> None:
		if proxy == None:
			self.chrome_options = ChromeOptions()
		elif proxy == 'default':
			self.chrome_options = ChromeOptions()
			self.chrome_options.add_argument('--no-sandbox')
			self.chrome_options.add_argument('--disable-dev-shm-usage')
			self.chrome_options.add_argument('--disable-notifications')
			self.chrome_options.add_argument('--ignore-certificate-errors')
			self.chrome_options.add_argument('--disable-infobars')
			self.chrome_options.add_argument('--webhooks-notification-dismissed=true')
			self.chrome_options.add_argument("--disable-popup-blocking")
			user_agent = UserAgentGenerator().user_agent
			self.chrome_options.add_argument(f'--user-agent={user_agent}')
		elif proxy == 'tor':
			self.chrome_options = ChromeOptions()
			self.chrome_options.add_argument('--no-sandbox')
			self.chrome_options.add_argument('--disable-dev-shm-usage')
			self.chrome_options.add_argument('--disable-notifications')
			self.chrome_options.add_argument('--ignore-certificate-errors')
			self.chrome_options.add_argument('--disable-infobars')
			self.chrome_options.add_argument('--webhooks-notification-dismissed=true')
			# chrome_options.add_argument('--disable-extensions')
			# chrome_options.add_argument("--incognito")
			self.chrome_options.add_argument('--user-data=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
			user_agent = UserAgentGenerator().user_agent
			self.chrome_options.add_argument(f'--user-agent={user_agent}')
			self.chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
			# self.chrome_options.add_argument(f'--remote-debugging-port=9222')
		
def main():
	pass

if __name__ == "__main__":
	main()