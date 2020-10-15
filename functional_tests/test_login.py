from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class SigninTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('weborchestra@signin.test', 'weborchestra@signin.test', 'Python4521')
        self.user.is_active = True
        self.user.profile.signup_confirmation = True
        self.user.save()

    def test_can_login_to_existing_account(self):
        # user checks out home page
        test_email = 'weborchestra@signin.test'
        self.browser.get(self.live_server_url)

        # he clicks on signin link and is redirected to signin form
        self.browser.find_element_by_link_text("SE CONNECTER").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "SE CONNECTER"
        ))

        # he is invited to complete the signin form
        inputbox_email = self.browser.find_element_by_id('id_email')
        self.check_for_placeholder_value_of_element(inputbox_email, 'exemple@adresse.com')
        inputbox_password = self.browser.find_element_by_id('id_password')
        self.check_for_placeholder_value_of_element(inputbox_password, '********')

        # he types in his email and password
        inputbox_email.send_keys(test_email)
        inputbox_password.send_keys('Python4521')

        # when he hits enter, the page updates and he is redirected to
        # the index page and the navbar displays a signout link
        inputbox_email.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.title,
            "Int'Aire'Mezzo | Accueil"
        ))
        self.wait_to_be_logged_in(test_email)

        # he clicks on signout link and the page reload
        self.browser.find_element_by_link_text('Se déconnecter'.upper()).click()

        # he is logged out
        self.wait_to_be_logged_out(test_email)
