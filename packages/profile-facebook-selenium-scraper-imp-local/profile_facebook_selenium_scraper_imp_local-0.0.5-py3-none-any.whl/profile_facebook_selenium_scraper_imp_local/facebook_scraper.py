"""
FacebookScraper Class:

This class defines a Facebook scraper to gather
information about friends on Facebook.
It uses Selenium for web scraping and provides methods for logging in,
extracting data about friends."""
import inspect
from datetime import datetime

from language_remote.lang_code import LangCode
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from profile_local.comprehensive_profile import ComprehensiveProfileLocal
from python_sdk_remote.utilities import our_get_env
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

LANG_CODE_HE = LangCode.HEBREW.value
QUEUE_LOCAL_PYTHON_COMPONENT_ID = 245
QUEUE_LOCAL_PYTHON_COMPONENT_NAME = "profile_facebook_selenium_scraper_imp_local/src/facebook_scraper"
DEVELOPER_EMAIL = 'neomi.b@circ.zone'
DEFAULT_STARS = 0
DEFAULT_LAST_DIALOG_WORKFLOW_STATE_ID = 0
SYSTEM_ID = 1

DISABLE_HEADLESS_MODE = our_get_env("DISABLE_HEADLESS_MODE",
                                    raise_if_not_found=False)  # You can set to false locally to see the browser & debug

LOGGER_CODE_OBJECT = {
    'component_id': QUEUE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': QUEUE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

# TODO: make sure we can see the data in  importer views, data_source_instance and api_call
#   using importing/sync of contacts/people/profiles
class FacebookScraper(metaclass=MetaLogger, object=LOGGER_CODE_OBJECT):
    """Class for scraping Facebook friends' information."""

    def __init__(self, facebook_user_identifier: str = None, facebook_password: str = None) -> None:
        """Initializes the FacebookScraper class."""
        self.comprehensive_profile = ComprehensiveProfileLocal()
        # TODO: use dict instead of self, and use all
        self.name = 'name'
        self.gender = 1
        self.job_title = 'job_title'
        self.address = 'address'
        self.email = 'email'
        self.went_to = 'went_to'
        self.website = 'website'
        options = webdriver.ChromeOptions()
        if not DISABLE_HEADLESS_MODE:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)

        self.facebook_user_identifier = facebook_user_identifier
        self.facebook_password = facebook_password
        if facebook_user_identifier and facebook_password:
            self.login(facebook_user_identifier, facebook_password)

    def __del__(self) -> None:
        """Destructor for the FacebookScraper class."""
        self.driver.quit()

    def _safe_find_element(self, by: str, value: str, raise_if_not_found: bool = True, multi: bool = False) -> (
            WebElement or list[WebElement] or None):
        try:
            self.wait.until(expected_conditions.presence_of_element_located((by, value)))
            element = self.driver.find_element(by, value) if not multi else self.driver.find_elements(by, value)
        except (NoSuchElementException, TimeoutException):
            caller_function = inspect.stack()[2].function
            error_message = f"Element not found in {caller_function}"
            if raise_if_not_found:
                self.logger.exception(error_message, object={'by': by, 'value': value, 'url': self.driver.current_url})
                raise Exception(error_message)
            else:
                self.logger.warning(error_message, object={'by': by, 'value': value})
                element = None

        return element

    def _move_to_url(self, url: str = None, refresh: bool = False) -> None:
        if url and (self.driver.current_url != url or refresh):
            self.driver.get(url)

    @staticmethod
    def extract_and_cast_to_int(input_string: str) -> int:
        """Extracts and casts the first integer from the given input string."""
        for s in input_string.split():
            if s.isdigit():
                return int(s)

    def login(self, facebook_user_identifier: str = None, facebook_password: str = None) -> None:
        """Login to the account by given username and facebook_password."""
        facebook_user_identifier = facebook_user_identifier or self.facebook_user_identifier
        facebook_password = facebook_password or self.facebook_password
        if not facebook_user_identifier or not facebook_password:
            raise ValueError("Facebook user identifier and password are required.")
        self._move_to_url(url='https://www.facebook.com/')

        facebook_user_identifier_input = self._safe_find_element(By.ID, 'email')
        facebook_password_input = self._safe_find_element(By.ID, 'pass')

        facebook_user_identifier_input.send_keys(facebook_user_identifier)
        facebook_password_input.send_keys(facebook_password)
        facebook_password_input.submit()

        self.wait.until(expected_conditions.url_contains('facebook.com'))

    def get_num_friends(self) -> int or None:
        """Gets the number of friends from the Facebook friends list."""
        self._move_to_url(url='https://www.facebook.com/friends/list')
        num_friends_css_selector = 'div.xu06os2:nth-child(3) > \
            div:nth-child(1) >div:nth-child(1) > div:nth-child(1) >\
                  div:nth-child(1) > div:nth-child(1) >\
                h2:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
        num_of_friends = self._safe_find_element(By.CSS_SELECTOR, num_friends_css_selector).text
        num_of_friends = self.extract_and_cast_to_int(num_of_friends)

        return num_of_friends

    def click_friend_by_index(self, index: int) -> None:
        """Clicks on the friend with the specified index (0 based)"""
        if self.driver.current_url != 'https://www.facebook.com/friends/list':
            self._move_to_url(url='https://www.facebook.com/friends/list')
        xpath = f'//*[@aria-label="All friends"]//a[@href]'
        friend_elements = self._safe_find_element(By.XPATH, xpath, multi=True)
        friend_elements = [friend for friend in friend_elements
                           if friend.get_attribute('href') != 'https://www.facebook.com/friends/']
        if index >= len(friend_elements):
            raise ValueError(f"Index {index} is out of range. Number of friends: {len(friend_elements)}")

        if friend_elements[index].is_displayed():
            friend_elements[index].click()

    # TODO: fix
    # def get_profile_name(self, url: str = None) -> str:
    #     """Gets the name of the current friend."""
    #     self._move_to_url(url=url)
    #     friend_name_css_selector = '.x14qwyeo > h1:nth-child(1)'
    #     friend_name = self._safe_find_element(By.CSS_SELECTOR, friend_name_css_selector).text
    #
    #     return friend_name

    def click_about_profile(self, url: str = None) -> None:
        """Clicks on the 'About' section of the current profile."""
        self._move_to_url(url=url)
        profile_tabs = self._safe_find_element(By.XPATH, '//*[@data-pagelet="ProfileTabs"]//a[@href]', multi=True)
        # Posts, About, Friends, Photos, Videos
        for tab in profile_tabs:
            if tab.text == 'About':
                tab.click()
                break

    def get_about_details(self):
        about = self._safe_find_element(By.XPATH, '//*[@data-pagelet="ProfileAppSection_0"]').text
        # Example: 'About\nContact and basic info\nPage transparency\nCategories\nPolitician\nContact info\nbibi@netanyahu.org.il\nEmail\nWebsites and social links\nhttp://www.netanyahu.org.il/\nWebsite'
        for line in about.split('\n'):
            if "@" in line:
                self.email = line
            elif "http" in line:
                self.website = line

    def click_about_basic_info_friend(self, url: str = None) -> None:
        """
        Clicks on the 'About' section and then the 'Basic Info' subsection
        of the current friend's profile."""
        self._move_to_url(url=url)
        self.click_about_profile()
        basic_info_css_selector = 'div.x1e56ztr:nth-child(5)'
        basic_info = self._safe_find_element(By.CSS_SELECTOR, basic_info_css_selector)
        basic_info.click()

    def get_intro(self, url: str = None) -> None:
        """Gets the intro information of the current friend."""
        self._move_to_url(url=url)
        xpath = '//*[@data-pagelet="ProfileTilesFeed_0"]'
        intro = self._safe_find_element(By.XPATH, xpath).text
        # Example 1: Intro
        # חשבון הפייסבוק הרשמי של ראש הממשלה בנימין נתניהו
        # Page · Politician
        # bibi@netanyahu.org.il
        # netanyahu.org.il

        # Example 2: Intro
        # Owner and Founder at SnowFun • כיף בשלג
        # Project Manager, Senior at NetoFun נטופאן
        # Owner and Founder at פלאפל אקספרס - Falafel express
        # Studied at האוניברסיטה הפתוחה The Open University
        # Lives in Netanya, Israel
        intro_lines = intro.split('\n')
        for line in intro_lines:
            if "@" in line:
                self.email = line
            elif "Lives in" in line:
                self.address = line
            elif "Studied at" in line:
                self.went_to = line
            elif " at " in line:
                self.job_title = line

    # def get_gender_type(self, url: str = None) -> int or None:
    #     # TODO: use enum
    #     """Gets the gender information of the current friend."""
    #     self._move_to_url(url=url)
    #     self.click_about_basic_info_friend()
    #     gender_css_selector = '.xqmdsaz > div:nth-child(3) >\
    #           div:nth-child(1) >div:nth-child(2) > div:nth-child(1) >\
    #               div:nth-child(1) > div:nth-child(2) >div:nth-child(1) >\
    #                   div:nth-child(1) > div:nth-child(1) >\
    #                       div:nth-child(1) >div:nth-child(1) >\
    #                           span:nth-child(1)'
    #     gender = self._safe_find_element(By.CSS_SELECTOR, gender_css_selector).text
    #
    #     if gender == 'Female':
    #         gender = 1
    #         return gender
    #     if gender == 'Male':
    #         gender = 2
    #         return gender

    @staticmethod
    def convert_to_date(date_string: str) -> datetime or None:
        """Converts a date string to a datetime object."""
        default_date_format = "%B %d %Y"
        date_object = datetime.strptime(date_string, default_date_format)
        return date_object

    # TODO: test
    def get_birth_date(self, url: str = None) -> datetime or None:
        """Gets the birthdate of the current friend."""
        self._move_to_url(url=url)
        self.click_about_basic_info_friend()
        birth_date_css_selector = 'div.xat24cr:nth-child(3) >\
              div:nth-child(1) >div:nth-child(1) > div:nth-child(2) >\
                  div:nth-child(1) > div:nth-child(1) >div:nth-child(1) >\
                   div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
        birth_date = self._safe_find_element(By.CSS_SELECTOR, birth_date_css_selector).text
        birth_year_css_selector = 'div.xat24cr:nth-child(3) >\
              div:nth-child(1) >div:nth-child(1) > div:nth-child(2) >\
                div:nth-child(2) > div:nth-child(1) >div:nth-child(1) >\
                   div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'

        birth_year = self._safe_find_element(By.CSS_SELECTOR, birth_year_css_selector).text
        birth_date = birth_date + " " + birth_year
        return self.convert_to_date(birth_date)

    def scrape_friends(self) -> None:
        """
        Scrapes information about the friends
        and inserts it into the database."""
        num_of_friends = self.get_num_friends()

        for friend_index in range(num_of_friends):
            try:
                self.click_friend_by_index(index=friend_index)
                self.get_intro()
                self.click_about_profile()
                self.get_about_details()

                self.insert_to_database()
            except Exception as exception:
                self.logger.exception("Error while scraping friend", object={
                    'friend_index': friend_index, 'exception': exception})

    @staticmethod
    def generate_compatible_dict(profile_entry: dict) -> dict:
        """generate_compatible_dict."""
        profile = {
            'number': profile_entry.get('number'),
            'profile_name': profile_entry.get('name'),
            'name': profile_entry.get('name'),
            'name_approved': True,
            'lang_code': LangCode(profile_entry.get('language', LANG_CODE_HE)),
            # 'user_id': logger.user_context.get_real_user_id(),
            'person_id': profile_entry.get('person_id'),
            'is_main': profile_entry.get('is_main', 0),
            'profile_type_id': profile_entry.get('profile_type_id', 1),
            'is_approved': profile_entry.get('is_approved', 0),
            # 'is_main': profile_entry.get('is_main'),
            'preferred_lang_code': LangCode(profile_entry['language']) if 'language' in profile_entry else None,
            'is_rip': profile_entry.get('rip', 0),
            "main_phone_id": profile_entry.get('main_phone_id', 1),
            "gender_id": profile_entry.get('gender_id', 1),
            "stars": profile_entry.get('stars', 0),
            'experience_years_min': profile_entry.get('experience_years_min'),
            'last_dialog_workflow_state_id': profile_entry.get('last_dialog_workflow_state_id', 0),
            'visibility_id': profile_entry.get('visibility_id', 0),
        }
        location = {
            'coordinate': {
                'latitude': profile_entry.get('latitude', 0),
                'longitude': profile_entry.get('longitude', 0),
            },
            'address_local_language': profile_entry.get('language'),
            'address_english': profile_entry.get('street'),
            'postal_code': profile_entry.get('zip'),
            'plus_code': profile_entry.get('plus_code'),
            'neighborhood': profile_entry.get('neighborhood'),
            'county': profile_entry.get('county'),
            'region': profile_entry.get('region'),
            'state': profile_entry.get('state', 'Israel'),
            'country': profile_entry.get('country')
        }

        entry = {
            "location": location,
            "profile": profile,
        }

        return entry

    def insert_to_database(self) -> None:
        """insert."""
        profile_dict = {
            'name': self.name,
            'gender_id': self.gender,
            'lang_code': LangCode(LANG_CODE_HE),
            'visibility_id': True,
            'is_approved': False,
            'stars': DEFAULT_STARS,
            'last_dialog_workflow_state_id': DEFAULT_LAST_DIALOG_WORKFLOW_STATE_ID,
            'job_title': self.job_title,
            'address_english': self.address
        }

        profile_dict = self.generate_compatible_dict(profile_dict)
        self.comprehensive_profile.insert(profile_dict=profile_dict, lang_code=LangCode(LANG_CODE_HE))
        # access_token = os.getenv("FACEBOOK_GRAPH_IMPORT_API_ACCESS_TOKEN")
        # ExternalUser.insert_or_update_external_user_access_token(
        #     self.username, profile_id, SYSTEM_ID, access_token)
