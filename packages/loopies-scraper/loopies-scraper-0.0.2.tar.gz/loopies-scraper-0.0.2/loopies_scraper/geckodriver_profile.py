#!/usr/bin/python
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from user_agent_generator import UserAgentGenerator

class GeckodriverProfile:
	firefox_profile: FirefoxProfile = None
	
	def __init__(self, proxy: str = None) -> None:
		if proxy == None:
			self.firefox_profile = FirefoxProfile()
		if proxy == 'default':
			self.firefox_profile = FirefoxProfile()
			user_agent = UserAgentGenerator().user_agent
			self.firefox_profile.set_preference('general.useragent.override', user_agent)
			self.firefox_profile.update_preferences()
		elif proxy == 'tor':
			self.firefox_profile = FirefoxProfile()
			self.firefox_profile.set_preference('network.proxy.type', 1)
			self.firefox_profile.set_preference('network.proxy.socks', '127.0.0.1')
			self.firefox_profile.set_preference('network.proxy.socks_port', 9050)
			self.firefox_profile.set_preference("network.proxy.socks_version", 5)
			self.firefox_profile.set_preference("network.proxy.socks_remote_dns", True)
			self.firefox_profile.set_preference("dom.webdriver.enabled", False)
			self.firefox_profile.set_preference('useAutomationExtension', False)
			user_agent = UserAgentGenerator().user_agent
			self.firefox_profile.set_preference('general.useragent.override', user_agent)
			self.firefox_profile.update_preferences()

def main():
	pass

if __name__ == "__main__":
	main()