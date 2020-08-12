from selenium import webdriver
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

        # he complete the form with his username, mail and password
        self.fail('Finish the test!')

        # when he hits enter, the account is created and he is redirected to the front page
        # the user reads a confirmation message that confirm his account was created

if __name__ =='__main__':
    unittest.main(warnings='ignore')