from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest


class ResetPasswordTest(FunctionalTest):

    def test_user_forgot_password(self):
        # Edith has an activated account
        test_email = 'edith.usertest@yahoo.com'
        test_password = 'Python4521'
        self.create_activated_account(test_email, 'ForgettablePassword1234')

        # She wants to login but she doesn't remember her password
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text("SE CONNECTER").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "SE CONNECTER"
        ))

        # She clicks on the "Forgot my password" link on the login page
        self.browser.find_element_by_link_text("Mot de passe oublié ?").click()

        # She is then redirected to the forgot password page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Demander la réinitialisation du mot de passe"
        ))

        # She is invited to complete a form
        inputbox_email = self.browser.find_element_by_id('id_email')
        self.check_for_placeholder_value_of_element(inputbox_email, 'exemple@adresse.com')

        # She types in her email address used to create her account
        inputbox_email.send_keys(test_email)

        # When she hits enter the page reload and a confirmation message appear
        inputbox_email.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('reset_password_sent_message'),
            "Si un compte est bien associé à l'email fourni vous devriez recevoir un"
            " lien pour réinitialiser votre mot de passe."
        ))

        # She checks her emails and finds a message
        body = self.wait_for_email(test_email, 'Demande de réinitialisation de mot de passe')

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is redirected to a page where she can set a new password
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Créer un nouveau mot de passe"
        ))

        # she is invited to complete the new password form
        inputbox_password = self.browser.find_element_by_id('id_password')
        self.check_for_placeholder_value_of_element(inputbox_password, '********')
        inputbox_confirm_password = self.browser.find_element_by_id('id_confirm_password')
        self.check_for_placeholder_value_of_element(inputbox_confirm_password, '********')

        # She complete the form
        inputbox_password.send_keys(test_password)
        inputbox_confirm_password.send_keys(test_password)
        inputbox_confirm_password.send_keys(Keys.ENTER)

        # She is then logged in
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)
