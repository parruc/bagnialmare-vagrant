"""
functional tests. The package layout for tests can be used as in the unittest
example in bagni application.
"""
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class HomePageTest(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        self.browser = webdriver.Remote(
                command_executor = "http://127.0.0.1:4444/wd/hub",
                desired_capabilities = DesiredCapabilities.FIREFOX,
                )
        self.browser.implicitly_wait(3)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()

    def test_home_page(self):
        self.browser.get("http://127.0.0.1:8081/it/")
        self.assertEqual(self.browser.title, "Homepage")

    def test_empty_search(self):
        self.browser.get("http://127.0.0.1:8081/it/")
        input = self.browser.find_element_by_id("search_q")        
        input.send_keys(Keys.RETURN)
        count = self.browser.find_element_by_class_name("hits-count")
        self.assertTrue(int(count.text) > 1000)

