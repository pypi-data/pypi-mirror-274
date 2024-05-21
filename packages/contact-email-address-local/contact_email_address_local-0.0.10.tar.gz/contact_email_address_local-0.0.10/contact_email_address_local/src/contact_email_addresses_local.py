from database_mysql_local.generic_mapping import GenericMapping
from email_address_local.email_address import EmailAddressesLocal
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext

from .contact_email_addresses_constants import CONTACT_EMAIL_ADDRESSES_PYTHON_PACKAGE_CODE_LOGGER_OBJECT

user_context = UserContext()

DEFAULT_SCHEMA_NAME = "contact_email_address"
DEFAULT_ENTITY_NAME1 = "contact"
DEFAULT_ENTITY_NAME2 = "email_address"
DEFAULT_ID_COLUMN_NAME = "contact_email_id"
DEFAULT_TABLE_NAME = "contact_email_address_table"
DEFAULT_VIEW_TABLE_NAME = "contact_email_address_view"


class ContactEmailAdressesLocal(GenericMapping, metaclass=MetaLogger,
                                object=CONTACT_EMAIL_ADDRESSES_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):
    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME, default_entity_name1: str = DEFAULT_ENTITY_NAME1,
                 default_entity_name2: str = DEFAULT_ENTITY_NAME2, default_column_name: str = DEFAULT_ID_COLUMN_NAME,
                 default_table_name: str = DEFAULT_TABLE_NAME, default_view_table_name: str = DEFAULT_VIEW_TABLE_NAME,
                 default_lang_code: LangCode = None, is_test_data: bool = False) -> None:

        GenericMapping.__init__(
            self, is_test_data=is_test_data,
            default_schema_name=default_schema_name, default_entity_name1=default_entity_name1,
            default_entity_name2=default_entity_name2, default_column_name=default_column_name,
            default_table_name=default_table_name, default_view_table_name=default_view_table_name)
        self.email_address_local = EmailAddressesLocal(is_test_data=is_test_data)
        self.default_lang_code = default_lang_code  # TODO: not used

    def insert_contact_and_link_to_email_address(
            self, contact_dict: dict, contact_email_address: str, contact_id: int) -> int or None:
        """
        Insert contact and link to existing or new email address
        :param contact_dict: contact_dict
        :param contact_email_address: contact_email_address
        :param contact_id: contact_id
        :return: contact_id
        """
        if not contact_email_address:
            # TODO: we can try to look if there's an email address in the database by phone number
            # when contact-phones-local is done
            return
        lang_code = LangCode.detect_lang_code_restricted(
            text=contact_email_address,
            allowed_lang_codes=[LangCode.ENGLISH.value, LangCode.HEBREW.value],
            default_lang_code=LangCode.ENGLISH
        )
        email_address_id = self.email_address_local.get_email_address_id_by_email_address(
            email_address=contact_email_address)
        if not email_address_id:
            # Create a new  email address and add it to email_address_table and email_address_ml_table
            self.logger.info("email_address_id is None, creating a new email address and adding it to"
                             " email_address_table and email_address_ml_table")
            first_name = contact_dict.get("first_name")
            last_name = contact_dict.get("last_name")
            name = f"{first_name} {last_name}"
            email_address_id = self.email_address_local.insert(email_address=contact_email_address,
                                                               lang_code=lang_code,
                                                               name=name, is_test_data=self.is_test_data)
            if not email_address_id:
                self.logger.error("email_address_id is None")
                return
            # Link contact to email address
            self.logger.info("Linking contact to email address")
            contact_email_address_id = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                           entity_name2=self.default_entity_name2,
                                                           entity_id1=contact_id, entity_id2=email_address_id,
                                                           ignore_duplicate=True)
        else:
            # check if there is link to existing email address
            self.logger.info("Linking contact to existing email address")
            mapping_tuple = self.select_multi_mapping_tuple_by_id(entity_name1=self.default_entity_name1,
                                                                  entity_name2=self.default_entity_name2,
                                                                  entity_id1=contact_id, entity_id2=email_address_id)
            if not mapping_tuple:
                # Link contact to existing email address
                self.logger.info("Linking contact to existing email address")
                contact_email_address_id = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                               entity_name2=self.default_entity_name2,
                                                               entity_id1=contact_id, entity_id2=email_address_id,
                                                               ignore_duplicate=True)
            else:
                self.logger.info("contact is already linked to email address")
                contact_email_address_id = mapping_tuple[0]
        return contact_email_address_id
