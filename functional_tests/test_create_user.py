from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewUserTest(FunctionalTest):

    def test_can_create_an_account_and_get_confirmation_message(self):
        # user check out home page
        self.browser.get(self.live_server_url)

        # he notices the page title and header mention web'orchestra
        self.assertIn("Int'Aire'Mezzo | Accueil", self.browser.title)

        # he clicks the signup button and is redirected to the signup form
        self.browser.find_element_by_link_text("S'INSCRIRE").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "S'INSCRIRE"
        ))

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
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            'ACTIVATION DU COMPTE'
        ))
        message = self.browser.find_element_by_id('activation_sent_message').text
        self.assertIn("Votre lien d'activation a été envoyé !", message)
