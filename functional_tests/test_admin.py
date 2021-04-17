from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class AdminPageTest(FunctionalTest):

    def test_admin_modify_user_informations(self):
        # Ben signed up as a standard user
        ben_email = 'ben@test.com'
        ben_password = 'Test1234'
        self.create_activated_account(ben_email, ben_password)

        # Edith is connected as an administrator
        edith_email = 'edith.usertest@yahoo.com'
        edith_password = 'Python4521'
        self.create_pre_authenticated_session(
            edith_email,
            edith_password,
            roles=[1]
        )

        # She checks out home page and sees she is logged in
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(edith_email)

        # She clicks on the Administration link and is redirected
        # to the admin page
        self.browser.find_element_by_link_text('ADMINISTRATION').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            'Administration'.upper()
        ))

        # Edith can see the list of all users of the site, she
        # locate the account of Ben
        users = self.browser.find_elements_by_class_name('user')
        self.wait_for(lambda: self.assertEqual(
            len(users),
            2
        ))

        ben_element = self.get_element_in_list_by_text(ben_email, users)
        self.wait_for(lambda: self.assertTrue(
            ben_element,
            f'User with adress {ben_email} not found.'
        ))

        # Edith clicks on the "modify" button corresponding to Ben profile
        # and is redirected to a form to edit ben's informations
        ben_element = ben_element.find_element_by_link_text('Modifier').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            ben_email.upper()
        ))

        # Edith can now check the role 'Musician' she wants to add to
        # ben's profile and submit the form
        musician_checkbox = self.browser.find_element_by_id('id_roles_6')
        musician_checkbox.click()
        musician_checkbox.send_keys(Keys.ENTER)

        # Edith is redirected to the admin page and now ben's has the musician
        # role displayed in the list
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            'Administration'.upper()
        ))

        users = self.browser.find_elements_by_class_name('user')
        ben_element = self.get_element_in_list_by_text(ben_email, users)
        self.wait_for(lambda: self.assertIn(
            'Musicien',
            ben_element.text
        ))

    def test_user_not_admin_can_not_see_admin_page(self):
        # Edith is connected as an standard user
        edith_email = 'edith.usertest@yahoo.com'
        edith_password = 'Python4521'
        self.create_pre_authenticated_session(
            edith_email,
            edith_password
        )

        # She checks out home page and sees she is logged in
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(edith_email)

        # She doesn't see the Admin link in the navbar
        admin_link = self.browser.find_elements_by_link_text('ADMINISTRATION')
        self.wait_for(lambda: self.assertFalse(
            admin_link,
            "The Admin link shouldn't be visible."
        ))
