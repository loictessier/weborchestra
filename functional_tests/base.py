from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_to_be_logged_in(self, email):
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('Se déconnecter'.upper(), navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('Se connecter'.upper(), navbar.text)
        self.assertIn("S'inscrire".upper(), navbar.text)

    def check_for_placeholder_value_of_element(self, element, placeholder_value):
        self.assertEqual(
            element.get_attribute('placeholder'),
            placeholder_value
        )
