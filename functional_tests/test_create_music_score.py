import os

from selenium.webdriver.common.keys import Keys
from override_storage import override_storage
from override_storage.storage import LocMemStorage

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

        # She sees a message that says she has not yet access
        # to any music score
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
        self.check_for_placeholder_value_of_element(
            inputbox_name,
            'Nom de la partition'
        )
        inputbox_author = self.browser.find_element_by_id('id_author')
        self.check_for_placeholder_value_of_element(
            inputbox_author,
            "Nom de l'auteur"
        )
        inputbox_editor = self.browser.find_element_by_id('id_editor')
        self.check_for_placeholder_value_of_element(
            inputbox_editor,
            "Nom de l'éditeur"
        )

        # There she fills the form with required informations and hits enter
        music_score_name = 'T-Bones In Swing'
        music_score_author = 'George Gershwin'
        music_score_editor = 'Molenaar Edition'
        inputbox_name.send_keys(music_score_name)
        inputbox_author.send_keys(music_score_author)
        inputbox_editor.send_keys(music_score_editor)
        inputbox_name.send_keys(Keys.ENTER)

        # She is then redirected to the page of the music score
        # she just created
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            f'{music_score_name} - {music_score_author}'.upper()
        ))

        # She then goes back to the music library index page
        self.browser.find_element_by_link_text('Partothèque'.upper()).click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Partothèque".upper()
        ))

        # And she sees that her new music score now appears on the page
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

    @override_storage(storage=LocMemStorage())
    def test_can_add_instrument_and_stand_to_a_music_score(self):
        # Edith is connected to her activated account
        test_email = 'edith.usertest@yahoo.com'
        test_password = 'Python4521'
        self.create_pre_authenticated_session(test_email, test_password)

        # She wants to add an instrument to a music
        # score she previously created
        music_score_name = 'T-Bones In Swing'
        music_score_author = 'George Gershwin'
        music_score_editor = 'Molenaar Edition'
        self.create_basic_music_score(
            music_score_name,
            music_score_author,
            music_score_editor
        )

        # She checks out home page and sees she is logged in
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(test_email)

        # She clicks on the music library link and
        # she is redirected to the music library pages
        self.browser.find_element_by_link_text('Partothèque'.upper()).click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            "Partothèque".upper()
        ))

        # she sees that her previously created music score appears on the page
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

        # She clicks on the music_score and is redirected to the score page
        music_score.click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            f'{music_score_name} - {music_score_author}'.upper()
        ))
        score_page = self.browser.current_url

        # She sees a message saying there is no instruments in the score yet
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_no_instruments_message').text,
            "Il n'existe pas encore d'instrument pour cette partition."
        ))

        # She clicks on the button that says "Add an instrument"
        self.browser.find_element_by_id('id_new_instrument_button').click()

        # She is redirected to a form to create an instrument
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            'Ajouter un instrument'.upper()
        ))

        # She is invited to complete the form
        inputbox_name = self.browser.find_element_by_id('id_name')
        self.check_for_placeholder_value_of_element(
            inputbox_name,
            "Nom de l'instrument"
        )

        # She fills the form and hit enter
        instrument_name = 'Hautbois'
        inputbox_name.send_keys(instrument_name)
        inputbox_name.send_keys(Keys.ENTER)

        # She is then redirected to the page of the instrument she just created
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            f'{instrument_name}'.upper()
        ))
        instrument_page = self.browser.current_url

        # Edith now sees a message saying that there are no stands
        # for her new score-instrument
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_no_stands_message').text,
            "Il n'existe pas encore de pupitre pour cet instrument."
        ))

        # She clicks on the button that says "Add a stand"
        self.browser.find_element_by_id('id_new_stand_button').click()

        # She is redirected to a form to add a stand
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            'Ajouter un pupitre'.upper()
        ))

        # She is invited to complete the form
        inputbox_name = self.browser.find_element_by_id('id_name')
        self.check_for_placeholder_value_of_element(
            inputbox_name,
            "Nom du pupitre"
        )
        inputbox_score = self.browser.find_element_by_id('id_score')
        self.assertEqual(inputbox_score.get_attribute('type'), 'file')

        # She fills the form and hit enter
        stand_name = f'{instrument_name} 1'
        inputbox_name.send_keys(stand_name)
        test_dir = os.path.dirname(os.path.abspath(__file__))
        inputbox_score.send_keys(f'{test_dir}/test_file/test.txt')
        inputbox_name.send_keys(Keys.ENTER)

        # She is then redirected to the page of the stand she just created
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h1').text,
            f'{stand_name}'.upper()
        ))

        # she checks that the name she set and the file she uploaded appears
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_name').text,
            stand_name
        ))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_score_link').text,
            'Télécharger la partition'
        ))

        # She goes back on music score page and checks
        # the new instrument is there
        self.browser.get(score_page)
        instrument = self.browser.find_elements_by_class_name('instrument')[0]
        self.wait_for(lambda: self.assertEqual(
            instrument.find_elements_by_class_name('instrument_name')[0].text,
            instrument_name
        ))

        # She then goes on the instrument page and checks the stand is there
        self.browser.get(instrument_page)
        stand = self.browser.find_elements_by_class_name('stand')[0]
        self.wait_for(lambda: self.assertEqual(
            stand.find_elements_by_class_name('stand_name')[0].text,
            stand_name
        ))
