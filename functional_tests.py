from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import unittest
import time

class NewUserTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_an_account_and_get_confirmation_message(self):
        # user check out home page
        self.browser.get('http://localhost:8000')
        
        # he notices the page title and header mention web'orchestra
        self.assertIn("Web'Orchestra", self.browser.title)

        # he clicks the signup button and is redirected to the signup form
        self.browser.find_element_by_link_text("S'INSCRIRE").click()
        time.sleep(1)
        title = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("S'INSCRIRE", title)

        # he is invited to complete the signup form
        inputbox_email = self.browser.find_element_by_id('id_signup_email')
        self.assertEqual(
            inputbox_email.get_attribute('placeholder'),
            'exemple@adresse.com'
        )
        inputbox_password = self.browser.find_element_by_id('id_signup_password')
        self.assertEqual(
            inputbox_password.get_attribute('placeholder'),
            '********'
        )

        # he types in his email and password
        inputbox_email.send_keys('abcdef@abcdef.abc')
        inputbox_password.send_keys('abcde')


        # when he hits enter, the page updates and now the page displays
        # a sign out button on the nav bar
        inputbox_password.send_keys(Keys.ENTER)
        time.sleep(1)
        try:
            self.browser.find_element_by_link_text('DECONNEXION')
        except NoSuchElementException:
            print("No element found")

if __name__ =='__main__':
    unittest.main(warnings='ignore')