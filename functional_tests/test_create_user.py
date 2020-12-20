import re

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewUserTest(FunctionalTest):

    def test_can_create_an_account_and_get_confirmation_message(self):
        # Edith check out home page
        self.browser.get(self.live_server_url)

        # she notices the page title and header mention web'orchestra
        self.assertIn("Int'Aire'Mezzo | Accueil", self.browser.title)

        # she clicks the signup button and is redirected to the signup form
        self.browser.find_element_by_link_text("S'INSCRIRE").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "S'INSCRIRE"
        ))

        # she is invited to complete the signup form
        inputbox_email = self.browser.find_element_by_id('id_email')
        self.check_for_placeholder_value_of_element(inputbox_email, 'exemple@adresse.com')
        inputbox_password1 = self.browser.find_element_by_id('id_password1')
        self.check_for_placeholder_value_of_element(inputbox_password1, '********')
        inputbox_password2 = self.browser.find_element_by_id('id_password2')
        self.check_for_placeholder_value_of_element(inputbox_password2, '********')

        # she types in his email and password
        test_email = 'edith.usertest@yahoo.com'
        test_password = 'Python4521'
        inputbox_email.send_keys(test_email)
        inputbox_password1.send_keys(test_password)
        inputbox_password2.send_keys(test_password)

        # when she hits enter, the page updates and now the page displays
        # a message stating that the confirmation email has been sent
        inputbox_email.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            'ACTIVATION DU COMPTE'
        ))
        message = self.browser.find_element_by_id('activation_sent_message').text
        self.assertIn("Votre lien d'activation a été envoyé !", message)

        # she checks her emails and finds a message
        body = self.wait_for_email(
            test_email,
            f'Veuillez activer votre compte sur {self.live_server_url.replace("http://", "")}'
        )

        # It has a url link in it
        self.assertIn('Veuillez cliquer sur le lien suivant pour confirmer la création de votre compte:', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is redirected to home and
        # she is logged in to her new activated account
        self.wait_to_be_at_home_page()
        self.wait_to_be_logged_in(test_email)
