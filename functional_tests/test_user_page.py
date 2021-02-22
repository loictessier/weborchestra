from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class UserPageTest(FunctionalTest):

    def test_user_check_and_modify_his_information(self):
        # Edith is connected to her active account
        test_email = 'edith.usertest@yahoo.com'
        test_password = 'Python4521'
        self.create_pre_authenticated_session(test_email, test_password)

        # She checks out home page and sees she is logged in
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(test_email)

        # She clicks on her username link and she is redirected
        # to the user page
        self.browser.find_element_by_link_text(test_email.upper()).click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            test_email.upper()
        ))

        # Edith can see her personnal informations such as
        # email adress and a button to modify the password
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_email').text,
            test_email
        ))
        modify_password_button = (
            self.browser.find_element_by_id('id_modify_password'))
        self.wait_for(lambda: self.assertEqual(
            modify_password_button.text,
            'Modifier le mot de passe'.upper()
        ))

        # She can clicks on the modify password button and is redirected to
        # a page where she can set a new password
        modify_password_button.click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Créer un nouveau mot de passe".upper()
        ))

        # she is invited to complete the new password form
        inputbox_password = self.browser.find_element_by_id('id_new_password1')
        self.check_for_placeholder_value_of_element(
            inputbox_password,
            '********'
        )
        inputbox_confirm_password = self.browser.find_element_by_id(
            'id_new_password2'
        )
        self.check_for_placeholder_value_of_element(
            inputbox_confirm_password,
            '********'
        )

        # She complete the form
        inputbox_password.send_keys(test_password)
        inputbox_confirm_password.send_keys(test_password)
        inputbox_confirm_password.send_keys(Keys.ENTER)

        # She is then logged in
        self.wait_to_be_logged_in(email=test_email)
