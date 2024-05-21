from datetime import datetime
from functools import lru_cache
from typing import Dict

from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from person_local.persons_local import PersonsLocal

from .constants_profile_local import PROFILE_LOCAL_PYTHON_LOGGER_CODE, DEFAULT_LANG_CODE


# TODO Where do we use 'object'? Can we call it 'logger_init_object' instead of 'object' everywhere?
class ProfilesLocal(GenericCRUD, metaclass=MetaLogger, object=PROFILE_LOCAL_PYTHON_LOGGER_CODE):
    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name="profile", default_table_name="profile_table",
                         default_view_table_name="profile_view", default_column_name="profile_id",
                         is_test_data=is_test_data)

    # TODO Shall we give insert() the person_id or shell insert() UPSERT person?
    def insert(self, *, profile_dict: Dict[str, any], person_id: int) -> int:  # noqa
        """Returns the new profile_id"""
        if "person_id" not in profile_dict:
            profile_dict["person_id"] = person_id
        if not isinstance(profile_dict.get('preferred_lang_code'), str):
            profile_dict["preferred_lang_code"] = profile_dict.get('preferred_lang_code', DEFAULT_LANG_CODE).value

        valid_columns = ['profile_id', 'number', 'identifier', 'name', 'title', 'title_approved', 'user_id', 'person_id', 'is_main',
                         'visibility_id', 'is_approved', 'profile_type_id', 'preferred_lang_code',
                         'experience_years_min', 'main_phone_id', 'profile_main_email', 'is_rip', 'gender_id', 'stars',
                         'last_dialog_workflow_state_id', 'is_system', 'internal_description', 'is_test_data',
                         'is_business_profile']
        profile_dict = {k: v for k, v in profile_dict.items() if k in valid_columns}
        profile_dict_ml = profile_dict.copy()
        if 'name' not in profile_dict:
            profile_dict['name'] = profile_dict_ml.get('title')
        if 'title' not in profile_dict_ml:
            profile_dict_ml['title'] = profile_dict.get('name')
        profile_dict.pop('title', None)
        profile_dict.pop('title_approved', None)
        super().insert(data_dict=profile_dict)

        profile_id = self.cursor.lastrowid()
        profile_ml_table_dict = {
            "profile_id": profile_id,
            "lang_code": profile_dict_ml.get('lang_code', DEFAULT_LANG_CODE).value,
            "title": profile_dict_ml['title'],  # Cannot be None
            "title_approved": profile_dict_ml.get('title_approved'),
            "about": profile_dict_ml.get('about')
        }
        super().insert(table_name="profile_ml_table", data_dict=profile_ml_table_dict)

        return profile_id

    def update(self, profile_dict: Dict[str, any]) -> None:
        profile_id = profile_dict['profile_id']
        profile_dict = {
            "person_id": profile_dict.get('person_id'),
            "name": profile_dict.get('name'),
            "user_id": profile_dict.get('user_id'),
            "is_main": profile_dict.get('is_main'),
            "visibility_id": profile_dict.get('visibility_id'),
            "is_approved": profile_dict.get('is_approved'),
            "profile_type_id": profile_dict.get('profile_type_id'),
            "preferred_lang_code": profile_dict.get('preferred_lang_code', DEFAULT_LANG_CODE).value,
            "experience_years_min": profile_dict.get('experience_years_min'),
            "main_phone_id": profile_dict.get('main_phone_id'),
            "is_rip": profile_dict.get('is_rip'),
            "gender_id": profile_dict.get('gender_id'),
            "stars": profile_dict.get('stars'),
            "last_dialog_workflow_state_id": profile_dict.get('last_dialog_workflow_state_id')
        }
        self.update_by_column_and_value(column_value=profile_id, data_dict=profile_dict)

        profile_ml_table_dict = {
            "profile_id": profile_id,
            "lang_code": profile_dict.get('lang_code', DEFAULT_LANG_CODE).value,
            "title": profile_dict['name'],
            "title_approved": profile_dict.get('title_approved'),
            "about": profile_dict.get('about')
        }
        self.update_by_column_and_value(table_name="profile_ml_table",
                          column_value=profile_id, data_dict=profile_ml_table_dict)

    # TODO develop get_profile_object_by_profile_id( self, profile_id: int ) -> Profile[]:
    # TODO I think it is more accurate to call it get_profile_dict_by_profile_id(...), as _dict can be str in a format of a JSON
    @lru_cache
    def get_profile_dict_by_profile_id(self, profile_id: int) -> Dict[str, any]:
        profile_ml_dict = self.select_one_dict_by_column_and_value(
            view_table_name="profile_ml_view", column_value=profile_id)
        profile_dict = self.select_one_dict_by_column_and_value(column_value=profile_id)

        if not profile_ml_dict or not profile_dict:
            return {}
        return {**profile_ml_dict, **profile_dict}

    @lru_cache
    def get_profile_id_by_email_address(self, email_address: str) -> int:
        return self.select_one_dict_by_column_and_value(column_name="main_email_address",
                                          column_value=email_address,
                                          select_clause_value="profile_id").get('profile_id')

    def delete_by_profile_id(self, profile_id: int):
        self.delete_by_column_and_value(column_value=profile_id)

    @lru_cache  # TODO: preferred_lang_code can change over time
    def get_preferred_lang_code_by_profile_id(self, profile_id: int) -> LangCode:
        preferred_lang_code = self.select_one_dict_by_column_and_value(column_value=profile_id).get('preferred_lang_code')
        return LangCode(preferred_lang_code)

    def get_test_profile_id(self) -> int:
        person_id = PersonsLocal().get_test_person_id()
        test_name = f"Test Profile {datetime.now().strftime('%Y/%m/%d-%H:%M:%S')}"
        return self.get_test_entity_id(entity_name="profile",
                                       insert_function=self.insert,
                                       insert_kwargs={"profile_dict": {"name": test_name},
                                                      "person_id": person_id})

    def insert_profile_type(self, is_test_data: bool = False) -> int:
        profile_type_table_dict = {"is_test_data": is_test_data or self.is_test_data}
        profile_type_id = super().insert(table_name="profile_type_table", data_dict=profile_type_table_dict)
        return profile_type_id

    @lru_cache
    def get_test_profile_type_id(self) -> int:
        return self.get_test_entity_id(entity_name="profile_type",
                                       insert_function=self.insert_profile_type)
