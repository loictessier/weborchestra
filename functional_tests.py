from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import logging

logger = logging.getLogger(__name__)

class NewUserTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_placeholder_value_of_element(self, element, placeholder_value):
        self.assertEqual(
            element.get_attribute('placeholder'),
            placeholder_value
        )

    def test_can_create_an_account_and_get_confirmation_message(self):
        # user check out home page
        self.browser.get('http://localhost:8000')
        
        # he notices the page title and header mention web'orchestra
        self.assertIn("Int'Aire'Mezzo | Accueil", self.browser.title)

        # he clicks the signup button and is redirected to the signup form
        self.browser.find_element_by_link_text("S'INSCRIRE").click()
        time.sleep(1)
        title = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("S'INSCRIRE", title)

        # he is invited to complete the signup form
        inputbox_email = self.browser.find_element_by_id('id_email')
        self.check_for_placeholder_value_of_element(inputbox_email, 'exemple@adresse.com')
        inputbox_password1 = self.browser.find_element_by_id('id_password1')
        self.check_for_placeholder_value_of_element(inputbox_password1, '********')
        inputbox_password2 = self.browser.find_element_by_id('id_password2')
        self.check_for_placeholder_value_of_element(inputbox_password2, '********')

        # he types in his email and password
        inputbox_email.send_keys('django@func.test')
        inputbox_password1.send_keys('Python4521')
        inputbox_password2.send_keys('Python4521')

        # when he hits enter, the page updates and now the page displays
        # a message stating that the confirmation email has been sent
        inputbox_email.send_keys(Keys.ENTER)
        time.sleep(1)
        title = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('ACTIVATION DU COMPTE', title)
        message = self.browser.find_element_by_id('activation_sent_message').text
        self.assertIn("Votre lien d'activation a été envoyé !", message)

if __name__ =='__main__':
    unittest.main(warnings='ignore')