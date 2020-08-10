from selenium import webdriver
import unittest

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
        self.fail('Finish the test!')

        # he clicks the sign up button and is redirected to the sign up form

        # he complete the form with his username, mail and password

        # when he hits enter, the account is created and he is redirected to the front page
        # the user reads a confirmation message that confirm his account was created

if __name__ =='__main__':
    unittest.main(warnings='ignore')