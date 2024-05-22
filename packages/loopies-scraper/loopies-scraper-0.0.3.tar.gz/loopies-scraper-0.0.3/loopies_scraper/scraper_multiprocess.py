#!/usr/bin/python
import multiprocessing, json
from functools import lru_cache 
from .data_manager import DataManager, QueueStatus
from .scraper import Scraper
import os, json

class MultiprocessScraper():
    def __init__(self, driver_name: str = None, proxy: str = None, processes_count: int = 1, file_path: str = './data.json') -> None:
        self.processes_count = processes_count
        self.driver_name = driver_name
        self.proxy = proxy
        self.file_path = file_path
        self.data_manager = DataManager()

    lru_cache(maxsize=None)
    def process_target(self, task_function: object = None, list_function: object = None):
        scraper = Scraper(driver_name=self.driver_name, proxy=self.proxy)

        if multiprocessing.current_process().name == "Process-1":
            if self.data_manager.queue_status.value is QueueStatus.NOT_STARTED.value:
                with self.data_manager.lock:
                    self.data_manager.queue_status.value = QueueStatus.STARTED.value
                
                list_function(scraper, self.data_manager)

                with self.data_manager.lock:
                    self.data_manager.queue_status.value = QueueStatus.DONE.value

        while self.data_manager.ready_to_get_url():
            page_url = None
            try:
                page_url = self.data_manager.queue.get()
            except Exception as e:
                print(e)

            if page_url is not None:
                try:
                    page_data = None
                    page_data = task_function(scraper, page_url)
                    if page_data is not None:
                        with self.data_manager.lock:
                            if not os.path.exists(self.file_path):
                                with open(self.file_path, 'w') as file:
                                    json.dump({'data':[]}, file)

                            with open(self.file_path, 'r+') as file:
                                scraped_data = json.load(file)
                                scraped_data['data'].append(page_data)
                                file.seek(0)
                                json.dump(scraped_data, file)
                except Exception as e:
                    print(e)
        
        scraper.driver.close()
        scraper.driver.quit()

    def process_target_basic(self, task_function: object = None):
        scraper = Scraper(driver_name=self.driver_name, proxy=self.proxy)

        try:
            page_data = None
            page_data = task_function(scraper)
            if page_data is not None:
                with self.data_manager.lock:
                    if not os.path.exists(self.file_path):
                        with open(self.file_path, 'w') as file:
                            json.dump({'data':[]}, file)

                    with open(self.file_path, 'r+') as file:
                        scraped_data = json.load(file)
                        scraped_data['data'].append(page_data)
                        file.seek(0)
                        json.dump(scraped_data, file)
        except Exception as e:
            print(e)
        
        scraper.driver.close()
        scraper.driver.quit()

    def start_processes(self, task_function: object = None, list_function: object = None):
        processes = []
        for _ in range(self.processes_count):
            if list_function is None and task_function is not None:
                process = multiprocessing.Process(target=self.process_target_basic, args=(task_function,))
            elif list_function is not None and task_function is not None:
                process = multiprocessing.Process(target=self.process_target, args=(list_function, task_function,))
            processes.append(process)
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    def basic_task(self, task_function: object = None):
        self.start_processes(task_function=task_function)

    def list_task(self, task_function: object = None, list_function: object = None):
        self.start_processes(task_function=task_function, list_function=list_function)


def main():
    pass

if __name__ == "__main__":
    main()