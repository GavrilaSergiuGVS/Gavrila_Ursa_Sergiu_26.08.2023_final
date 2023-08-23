import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.support.select import Select
import constants as const


class Booking(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
        self.driver.get(const.BASE_URL)
        self.driver.find_element(*const.ACCEPT_COOKIE_BUTTON).click()

    def tearDown(self) -> None:
        self.driver.quit()

    def test_login_existing_account_sign_in(self):
        register_element = self.driver.find_element(*const.SIGN_IN_MAIN_BUTTON)
        register_element.click()
        self.driver.find_element(*const.REGISTER_EMAIL_INPUT).send_keys("gavrilasergiu@gmail.com")
        self.driver.find_element(*const.REGISTER_CONTINUE_WITH_EMAIL_BUTTON).click()
        self.driver.find_element(*const.REGISTER_PASSWORD_INPUT).send_keys("Uigressergiu3021984")
        self.driver.find_element(*const.PRESS_SIGNIN_BUTTON).click()
        expected_url = "https://www.booking.com/?auth_success=1"
        actual_url = self.driver.current_url
        assert expected_url == actual_url,"SIGN IN WITH SUCCESS!!"
        assert self.driver.find_element(*const.PRESS_SIGNIN_BUTTON).is_enabled()

    def test_change_currency(self):
        currency_element = self.driver.find_element(*const.CURRENCY_MENU)
        currency_element.click()
        self.driver.find_element(*const.CURRENCY_VALUE).click()
        currency_selected_value = self.driver.find_element(*const.CURRENCY_SELECTED_VALUE).text
        assert currency_selected_value == 'USD'

    def test_change_language(self):
        current_language = self.driver.find_element(*const.LANGUAGES_MENU)
        current_language.click()
        self.driver.find_element(*const.LANGUAGE_VALUE).click()
        sleep(2)
        language_selected_value = self.driver.find_element(*const.LANGUAGE_SELECTED_VALUE).get_attribute("aria-label")
        assert language_selected_value == 'Limba: Română'
    
    def test_login_existing_account_with_wrong_email(self):
        register_element = self.driver.find_element(*const.SIGN_IN_MAIN_BUTTON)
        register_element.click()
        self.driver.find_element(*const.REGISTER_EMAIL_INPUT).send_keys("gavrilasergiu@gmail.com")
        self.driver.find_element(*const.REGISTER_CONTINUE_WITH_EMAIL_BUTTON).click()
        create_account_value = self.driver.find_element(*const.CREATE_ACCOUNT).get_attribute("submit")
        assert create_account_value != 'Create account'

    def test_login_existing_account_with_wrong_password(self):
        register_element = self.driver.find_element(*const.SIGN_IN_MAIN_BUTTON)
        register_element.click()
        self.driver.find_element(*const.REGISTER_EMAIL_INPUT).send_keys("gavrilaseiu@gmail.com")
        self.driver.find_element(*const.REGISTER_CONTINUE_WITH_EMAIL_BUTTON).click()
        self.driver.find_element(*const.REGISTER_PASSWORD_INPUT).send_keys("Uigressergiu3021984")
        self.driver.find_element(*const.REGISTER_PASSWORD_CONFIRM).send_keys("Uigressergiu3021983")
        self.driver.find_element(*const.PRESS_SIGNIN_BUTTON).click()
        wrong_password_error = self.driver.find_element(*const.WRONG_PASSWORD_ERROR).text
        assert "The passwords you entered didn't match – try again" in wrong_password_error
    
    def test_place_to_go(self):
        self.driver.find_element(*const.PLACE_TO_GO).send_keys('Paris')
        first_result = self.driver.find_element(*const.CLICK_FIRST_RESULT)
        first_result.click()
        chosen_place = self.driver.find_element(*const.CHOSEN_PLACE).text
        assert "Paris" in chosen_place

    def test_select_dates(self):
        click_check_date = self.driver.find_element(*const.CLICK_CHECK_IN_DATE)
        click_check_date.click()
        click_check_in = self.driver.find_element(*const.DATE_CHECK_IN)
        click_check_in.click()
        click_check_out = self.driver.find_element(*const.DATE_CHECK_OUT)
        click_check_out.click()
        assert click_check_out == None
    
    def test_select_adults(self):
        selection_element = self.driver.find_element(*const.CLICK_ADULTS_CHILDS_ROOM)
        selection_element.click()
        select_adults = self.driver.find_element(*const.CLICK_ADDED_ADULTS)
        for _ in range(2):  # faceți 2 clicuri consecutive
            ActionChains(self.driver).click(select_adults).perform()
        # Verificați dacă select_adults are valoarea 4
        updated_value = self.driver.find_element(*const.UPDATE_VALUE_ADULTS)
        updated_value = int(updated_value.text.strip())
        assert updated_value == 2, f"Expected 4 but got {updated_value}"

    def test_select_childrens(self):
        selection_element = self.driver.find_element(*const.CLICK_ADULTS_CHILDS_ROOM)
        selection_element.click()
        select_childrens = self.driver.find_element(*const.CLICK_ADDED_CHILDS)
        ActionChains(self.driver).click(select_childrens).perform()
        age_needed_dropdown = Select(self.driver.find_element(*const.DROPDOWN_AGE_NEEDED))
        age_needed_dropdown.select_by_visible_text("12 years old")
        search_data = self.driver.find_element(*const.SEARCH_DATA).text
        assert search_data == '2 adults · 1 child · 1 room',f"Error: search data is not correct. Actual value: {search_data} "

    def test_find_getaway_deals(self):
        self.driver.find_element(*const.FIND_GETAWAY_DEALS).click()
        expected_url = 'https://www.booking.com/dealspage.html'
        actual_url = self.driver.current_url
        assert expected_url == actual_url ,"Error: the page navigation was not done properly"