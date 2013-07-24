"""
functional tests. The package layout for tests can be used as in the unittest
example in bagni application.
"""
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class HomePageTest(LiveServerTestCase):

    #fixtures = ['bagni.json']

    def setUp(self):
        self.browser = webdriver.Remote(
                command_executor = "http://127.0.0.1:4444/wd/hub",
                desired_capabilities = DesiredCapabilities.FIREFOX,
                )
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        self.browser.get("http://127.0.0.1:8080/it/")
        h1 = self.browser.find_element_by_id("content-title")
        self.assertEqual(h1.text, "Homepage")

