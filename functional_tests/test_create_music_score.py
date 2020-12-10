from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewMusicScoreTest(FunctionalTest):

    def test_can_create_basic_music_score(self):
        # Edith is connected to her activated account
        test_email = 'edith.usertest@yahoo.com'
        test_password = 'Python4521'
        self.create_pre_authenticated_session(test_email, test_password)

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

        # She sees a message that says she has not yet access to any music score
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_no_score_message').text,
            "Il n'existe pas encore de partition à laquelle vous avez accès."
        ))

        # She click on the "add music score" button
        self.browser.find_element_by_id('id_new_score_button').click()

        # She is redirected to a form to create a music score
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Nouvelle partition".upper()
        ))

        # she is invited to complete the form
        inputbox_name = self.browser.find_element_by_id('id_name')
        self.check_for_placeholder_value_of_element(inputbox_name, 'Nom de la partition')
        inputbox_author = self.browser.find_element_by_id('id_author')
        self.check_for_placeholder_value_of_element(inputbox_author, "Nom de l'auteur")
        inputbox_editor = self.browser.find_element_by_id('id_editor')
        self.check_for_placeholder_value_of_element(inputbox_editor, "Nom de l'éditeur")

        # There she fills the form with required informations and hits enter
        music_sheet_name = 'T-Bones In Swing'
        music_sheet_author = 'George Gershwin'
        music_sheet_editor = 'Molenaar Edition'
        inputbox_name.send_keys(music_sheet_name)
        inputbox_author.send_keys(music_sheet_author)
        inputbox_editor.send_keys(music_sheet_editor)
        inputbox_name.send_keys(Keys.ENTER)

        # She is then redirected to the page of the music score she just created
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            f'{music_sheet_name} - {music_sheet_author}'.upper()
        ))

        # She then goes back to the music library index page
        self.browser.find_element_by_link_text('Partothèque'.upper()).click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Partothèque".upper()
        ))

        # And she sees that her new music score now appears on the page
        music_score = self.browser.find_elements_by_class_name('music_score')[0]
        score_name = music_score.find_elements_by_class_name('score_name')[0]
        self.assertEqual(score_name.text, f'{music_sheet_name}')
        score_author = music_score.find_elements_by_class_name('score_author')[0]
        self.assertEqual(score_author.text, f'{music_sheet_author}')
