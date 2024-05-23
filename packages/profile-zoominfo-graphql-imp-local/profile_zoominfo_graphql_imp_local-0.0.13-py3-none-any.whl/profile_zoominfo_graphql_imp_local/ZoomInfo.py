import json

from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from profile_local.comprehensive_profile import ComprehensiveProfileLocal
from python_sdk_remote.utilities import our_get_env
from zoomus import ZoomClient

from .constants_zoominfo import OBJECT_FOR_LOGGER_CODE

ZOOMINFO_APPLICATION_CLIENT_ID = our_get_env("ZOOMINFO_APPLICATION_CLIENT_ID")
ZOOMINFO_APPLICATION_CLIENT_SECRET = our_get_env("ZOOMINFO_APPLICATION_CLIENT_SECRET")
ZOOMINFO_APPLICATION_ACCOUNT_ID = our_get_env("ZOOMINFO_APPLICATION_ACCOUNT_ID")

DEFAULT_LANG_CODE = LangCode.ENGLISH  # TODO: remove and use real language code per user


class ZoomInfo(ZoomClient, metaclass=MetaLogger, object=OBJECT_FOR_LOGGER_CODE):
    def __init__(self, client_id: str = ZOOMINFO_APPLICATION_CLIENT_ID,
                 client_secret: str = ZOOMINFO_APPLICATION_CLIENT_SECRET,
                 account_id: str = ZOOMINFO_APPLICATION_ACCOUNT_ID) -> None:
        """
        Sets the ZoomInfo client with the given credentials.

        Args:
            client_id (str): The client ID.
            client_secret (str): The client secret.
            account_id (str): The account ID.

        Returns:
            ZoomClient: The configured ZoomClient instance.
        """
        super().__init__(client_id=client_id, client_secret=client_secret, api_account_id=account_id)
        self.comprehensive_profile_local = ComprehensiveProfileLocal()

    def get_user_by_email(self, email_address: str) -> dict or None:
        """
        Gets a ZoomInfo user by their email address.

        Args:
            email_address (str): The email address to search for.

        Returns:
            dict: The user dict if found, else None.
        """

        users = self.get_all_users()
        for user in users['users']:
            if user['email'] == email_address:
                user = self.get_user_by_id(user['id'])
                compatible_dict = self.generate_compatible_dict(user)
                self.comprehensive_profile_local.insert(profile_dict=compatible_dict,
                                                        lang_code=DEFAULT_LANG_CODE)

                return user
        return None

    def _get_next_page(self, next_page_token: str) -> dict:
        """
        Internal method to get the next page of results.

        Args:
            next_page_token (str): The next page token.

        Returns:
            dict: The next page of results.
        """
        response = self.user.list(page_token=next_page_token)
        if response.status_code != 200:
            raise Exception(f"Failed to get all users. Status code: {response.status_code}, "
                            f"response.json(): {response.json()}")
        users_list = response.json()
        return users_list

    def get_all_users(self) -> dict:
        """
        Gets all ZoomInfo users.

        Returns:
            dict: The response containing users.
        """

        response = self.user.list()

        if response.status_code != 200:
            raise Exception(f"Failed to get all users. Status code: {response.status_code}, "
                            f"response.json(): {response.json()}")
        users_list = response.json()

        while users_list['page_number'] <= users_list['page_count']:
            for user in users_list['users']:
                user = self.get_user_by_id(user['id'])
                compatible_dict = self.generate_compatible_dict(user)
                self.comprehensive_profile_local.insert(profile_dict=compatible_dict, lang_code=DEFAULT_LANG_CODE)
            if users_list['next_page_token'] == "":
                break
            users_list = self._get_next_page(users_list['next_page_token'])

        return users_list

    def get_all_users_emails(self) -> list:
        """
        Gets all ZoomInfo users emails.

        Returns:
            list: The list of emails.
        """

        users = self.get_all_users()
        emails = []
        for user in users['users']:
            emails.append(user['email'])

        return emails

    def get_user_by_phone_number(self, phone_number: str) -> dict or None:
        """
        Gets a ZoomInfo user by their phone number.

        Args:
            phone_number (str): The phone number to search for.

        Returns:
            dict: The user dict if found, else None.
        """

        users = self.get_all_users()

        while users['page_number'] <= users['page_count']:
            for user in users['users']:
                user = self.get_user_by_id(user['id'])
                if phone_number in user['phone_number']:
                    compatible_dict = self.generate_compatible_dict(user)
                    self.comprehensive_profile_local.insert(profile_dict=compatible_dict, lang_code=DEFAULT_LANG_CODE)

                    return user
            if users['next_page_token'] == "":
                break
            users = self._get_next_page(users['next_page_token'])

        return None

    def get_user_by_first_and_last_name(self, first_name: str, last_name: str) -> dict or None:
        """
        Gets a ZoomInfo user by their name.

        Args:
            first_name (str): The first name to search for.
            last_name (str): The last name to search for.

        Returns:
            dict: The user dict if found, else None.
        """

        users = self.get_all_users()

        users_by_name = []
        while users['page_number'] <= users['page_count']:
            for user in users['users']:
                if user['first_name'] == first_name and user['last_name'] == last_name:
                    user = self.get_user_by_id(user['id'])
                    compatible_dict = self.generate_compatible_dict(user)
                    self.comprehensive_profile_local.insert(profile_dict=compatible_dict, lang_code=DEFAULT_LANG_CODE)

                    users_by_name.append(user)
            if users['next_page_token'] == "":
                return users_by_name
            users = self._get_next_page(users['next_page_token'])

        return None

    def get_user_by_id(self, user_id: str) -> dict or None:
        """
        Gets a ZoomInfo user by their ID.

        Args:
            user_id (str): The user ID to search for.

        Returns:
            dict: The user dict if found, else None.
        """

        user_response = self.user.get(id=user_id)
        if user_response.status_code != 200:
            raise Exception(f"Failed to get user by ID. Status code: {user_response.status_code}, "
                            f"user_response.json(): {user_response.json()}")
        user_dict = user_response.json()
        print(json.dumps(user_dict, indent=4, sort_keys=True))
        compatible_dict = self.generate_compatible_dict(user_dict)
        self.comprehensive_profile_local.insert(profile_dict=compatible_dict, lang_code=DEFAULT_LANG_CODE)

        return user_dict

    def get_all_users_by_location(self, location: str) -> list:
        """
        Gets all ZoomInfo users by their location.

        Args:
            location (str): The location to search for.

        Returns:
            list: The list of users.
        """

        users = self.get_all_users()
        users_by_location = []
        while users['page_number'] <= users['page_count']:
            for user in users['users']:
                user = self.get_user_by_id(user['id'])
                if str(user['location']).lower() == location.lower():
                    # TODO Shall we add importer package in comprehensive_profile.insert() so we can see what was imported using 'SELECT * FROM importer.importer_entity_types_imported_group_by_date_source_view;'
                    # TODO Shall we call storage package in comprehensive_profile.insert()?
                    compatible_dict = self.generate_compatible_dict(user)
                    self.comprehensive_profile_local.insert(profile_dict=compatible_dict, lang_code=DEFAULT_LANG_CODE)
                    users_by_location.append(user)
            if users['next_page_token'] == "":
                break
            users = self._get_next_page(users['next_page_token'])

        return users_by_location

    def get_all_zoominfo_user_by_job_title(self, job_title: str) -> list:
        """
        Gets all ZoomInfo users by their job title.

        Args:
            job_title (str): The job title to search for.

        Returns:
            list: The list of users.
        """

        users = self.get_all_users()
        users_by_job_title = []

        while users['page_number'] <= users['page_count']:
            for user in users['users']:
                user = self.get_user_by_id(user['id'])
                if str(user['job_title']).lower() == job_title.lower():
                    compatible_dict = self.generate_compatible_dict(user)
                    self.comprehensive_profile_local.insert(profile_dict=compatible_dict, lang_code=DEFAULT_LANG_CODE)
                    users_by_job_title.append(user)
            if not users['next_page_token']:
                break
            users = self._get_next_page(users['next_page_token'])

        return users_by_job_title

    @staticmethod
    def generate_compatible_dict(user_info: dict) -> dict:
        plan_type_dict = {
            1: "Basic",
            2: "Licensed",
            99: "None (can only be set with ssoCreate)"
        }

        # TODO Please add _dict suffix to all those objects
        person = {}

        profile = {
            'name': user_info['display_name'],
            'title_approved': True,
            'lang_code': user_info['language'],
            'user_id': user_info['id'],
            'is_approved': True,
            'profile_type_id': plan_type_dict[user_info['type']],
            'preferred_lang_code': user_info['language'],
            'main_phone_id': user_info['phone_number'],
        }

        location = {
            'address_local_language': user_info['language'],
            'coordinate': {},
            'phone_number': user_info['phone_number'],
            'country': user_info['location']
        }

        # TODO Please use the storage package
        storage = {
            'path': user_info.get('pic_url'),  # TODO: pic_url is not in user_info
            'url': user_info.get('pic_url'),
            'file_extension': 'jpg',
            'file_type': 'Profile Image'
        }

        entry = {
            "person": person,
            "location": location,
            "profile": profile,
            "storage": storage,
        }

        return entry
