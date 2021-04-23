from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ExistingMusicScoreTest(FunctionalTest):

    def test_can_delete_basic_music_score(self):
        # Edith is connected to her activated account as
        # a music library moderator
        test_email = 'edith.usertest@yahoo.com'
        test_password = 'Python4521'
        self.create_pre_authenticated_session(
            test_email,
            test_password,
            roles=[2]
        )

        # She wants to delete a music score she previously created
        music_score_name = 'T-Bones In Swing'
        music_score_author = 'George Gershwin'
        music_score_editor = 'Molenaar Edition'
        self.create_basic_music_score(
            music_score_name,
            music_score_author,
            music_score_editor
        )

        # Edith checks out home page and sees she is logged in
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(test_email)

        # She clicks on the music library link and
        # she is redirected to the music library pages
        self.browser.find_element_by_link_text('Partothèque'.upper()).click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Partothèque".upper()
        ))

        # She sees that her previously created music score appears on the page
        music_score = (
            self.browser.find_elements_by_class_name('music_score')[0]
        )
        score_name = (
            music_score.find_elements_by_class_name('score_name')[0]
        )
        self.assertEqual(score_name.text, f'{music_score_name}')
        score_author = (
            music_score.find_elements_by_class_name('score_author')[0]
        )
        self.assertEqual(score_author.text, f'{music_score_author}')

        # She click on the delete button of the music score
        music_score.find_element_by_class_name('delete_score').click()

        # The page reload and the music score no longer appear
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Partothèque".upper()
        ))
        self.wait_for(lambda: self.assertEqual(
            len(self.browser.find_elements_by_class_name('music_score')),
            0
        ))

    def test_can_modify_basic_music_score(self):
        # Edith is connected to her activated account as
        # a music library moderator
        test_email = 'edith.usertest@yahoo.com'
        test_password = 'Python4521'
        self.create_pre_authenticated_session(
            test_email,
            test_password,
            roles=[2]
        )

        # She wants to modify a music score she previously created
        music_score_name = 'T-Bones In S'
        music_score_author = 'Gershwin'
        music_score_editor = 'Molenaar Edition'
        self.create_basic_music_score(
            music_score_name,
            music_score_author,
            music_score_editor
        )

        # Edith checks out home page and sees she is logged in
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(test_email)

        # She clicks on the music library link and
        # she is redirected to the music library pages
        self.browser.find_element_by_link_text('Partothèque'.upper()).click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Partothèque".upper()
        ))

        # She sees that her previously created music score appears on the page
        music_score = (
            self.browser.find_elements_by_class_name('music_score')[0]
        )
        score_name = (
            music_score.find_elements_by_class_name('score_name')[0]
        )
        self.assertEqual(score_name.text, f'{music_score_name}')
        score_author = (
            music_score.find_elements_by_class_name('score_author')[0]
        )
        self.assertEqual(score_author.text, f'{music_score_author}')

        # She click on the edit button of the music score
        music_score.find_element_by_class_name('edit_score').click()

        # She is redirected to a form where she can modify
        # the name, author and editor of the score
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            'Modifier une partition'.upper()
        ))
        inputbox_name = self.browser.find_element_by_id('id_name')
        self.wait_for(lambda: self.assertEqual(
            inputbox_name.get_attribute('value'),
            music_score_name
        ))
        inputbox_author = self.browser.find_element_by_id('id_author')
        self.wait_for(lambda: self.assertEqual(
            inputbox_author.get_attribute('value'),
            music_score_author
        ))

        # She modify the name and author and hit enter
        music_score_name = 'T-Bones In Swing'
        music_score_author = 'George Gershwin'
        inputbox_name.clear()
        inputbox_name.send_keys(music_score_name)
        inputbox_author.clear()
        inputbox_author.send_keys(music_score_author)
        inputbox_name.send_keys(Keys.ENTER)

        # She is then redirected to the page of the music score
        # she just modified with the new name and author
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            f'{music_score_name} - {music_score_author}'.upper()
        ))
