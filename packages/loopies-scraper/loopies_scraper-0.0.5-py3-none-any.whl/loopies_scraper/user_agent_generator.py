#!/usr/bin/python
import os, random
from fake_useragent import UserAgent, FakeUserAgentError

class UserAgentGenerator:
    user_agent: str = None

    def __init__(self) -> None:
        try:
            self.user_agent = UserAgent().random
        except FakeUserAgentError:
            lines = []
            file_path = os.path.normpath(f'{os.getcwd()}/fake_user_agent_list.txt')
            with open(file_path, 'r') as file:
                lines = [line.rstrip() for line in file]
            self.user_agent = random.choices(lines)[0]

    def get_fake_user_agent_list(self):
        fake_user_agent_list = []
        while len(fake_user_agent_list) < 100:
            try:
                random_user_agent = UserAgent().random
                if random_user_agent not in fake_user_agent_list:
                    fake_user_agent_list.append(random_user_agent)
            except FakeUserAgentError:
                pass

        file_path = os.path.normpath(f'{os.getcwd()}/fake_user_agent_list.txt')
        with open(file_path, 'w') as file:
            for ua in fake_user_agent_list:
                file.write(f'{ua}\n')

def main():
    fake_user_agent = UserAgentGenerator()
    fake_user_agent.get_fake_user_agent_list()

if __name__ == "__main__":
    main()