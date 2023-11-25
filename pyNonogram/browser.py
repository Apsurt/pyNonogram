from typing import Optional, Literal

from selenium import webdriver
from selenium.webdriver.common import action_chains, by

class Browser:
    def __init__(self, headless: Optional[bool] = False) -> None:
        self.driver = webdriver.Chrome
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless=new")
        self.initialize_driver()
    
    def initialize_driver(self) -> None:
        self.driver = self.driver(options=self.options)
    
    def reset_driver(self) -> None:
        self.driver.quit()
        self.driver = webdriver.Chrome
        self.initialize_driver()
    
    def set_headless(self, headless: bool) -> None:
        self.driver.quit()
        self.driver = webdriver.Chrome
        if headless:
            self.options.add_argument("--headless=new")
        else:
            self.options.remove_argument("--headless")
        self.initialize_driver()
    
    def open_url(self, url: str) -> None:
        self.driver.get(url)
    
    def get_html(self, url: Optional[str] = None) -> str:
        if url:
            self.open_url(url)
        html = self.driver.page_source
        return html
    
    def get_element(self, by: Literal['ID', 'XPATH'], value: str) -> object:
        return self.driver.find_element(by.By.XPATH if by == 'XPATH' else by.By.ID , value)
    
    def click_element(self, by: Literal['ID', 'XPATH'], value: str, click_type: Optional[Literal[None, 'left', 'right']] = None) -> None:
        element = self.get_element(by, value)
        builder = action_chains.ActionChains(self.driver)
        if click_type == 'left':
            builder.click(element)
        elif click_type == 'right':
            builder.context_click(element)
        else:
            builder.click(element)
        builder.perform()
    
    def maximize(self) -> None:
        self.driver.maximize_window()

browser = Browser(True)
browser.open_url("https://www.nonograms.org/nonograms/i/67918")