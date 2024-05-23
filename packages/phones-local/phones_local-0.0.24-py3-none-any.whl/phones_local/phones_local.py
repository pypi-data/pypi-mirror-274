from database_mysql_local.generic_mapping import GenericMapping
from logger_local.LoggerLocal import Logger
from phonenumbers import (NumberParseException, PhoneNumberFormat,
                          format_number, parse)
from user_context_remote.user_context import UserContext

from .phone_local_constans import code_object_init

logger = Logger.create_logger(object=code_object_init)
user_context = UserContext()


class PhonesLocal(GenericMapping):
    def __init__(self) -> None:
        super().__init__(default_schema_name="phone",
                         default_table_name="phone_table",
                         default_view_table_name="phone_view",
                         default_column_name="phone_id")

    def get_normalized_phone_number_by_phone_id(self, phone_id: int) -> int:
        logger.start(object={"phone_id": phone_id})
        data = self.select_one_dict_by_column_and_value(select_clause_value="local_number_normalized",
                                          column_value=phone_id)
        if not data:
            logger.end("No phone number found for phone_id " +
                       str(phone_id))
        else:
            phone_number = int(data["local_number_normalized"])
            logger.end("Return Phone Number of a specific phone id",
                       object={'phone_number': phone_number})
            return phone_number  # TODO: should we add area_code?

    def verify_phone_number(self, phone_number: int) -> None:
        logger.start(object={"phone_number": phone_number})
        self.update_by_column_and_value(column_value=phone_number,
                          data_dict={"is_verified": 1})
        logger.end()

    def is_verified(self, phone_number: int) -> bool:
        logger.start(object={"phone_number": phone_number})
        data = self.select_one_dict_by_column_and_value(select_clause_value="is_verified",
                                          column_value=phone_number)
        if not data:
            logger.end("No phone number found for phone_number " +
                       str(phone_number))
            return False
        is_verified = data["is_verified"]
        logger.end("Return is_verified of a specific phone id",
                   object={'is_verified': is_verified})
        return is_verified

    @staticmethod
    def normalize_phone_number(original_number: str, region: str) -> dict:
        """
        Normalize phone number to international format.
        :param original_number: Original phone number.
        :param region: Region of the phone number.
        :return: Dictionary with the normalized phone number and the international code.

        Example:
        original_number = "0549338666"
        region = "IL"
        result = {
            "international_code": 972,
            "full_number_normalized": "+972549338666"
        }
        """
        try:
            parsed_number = parse(original_number, region)
            international_code = parsed_number.country_code
            full_number_normalized = format_number(parsed_number, PhoneNumberFormat.E164)
            # parsed_number example: original_number='0687473298' -> PhoneNumber(country_code=972, national_number=687473298, extension=None, italian_leading_zero=None, number_of_leading_zeros=None, country_code_source=0, preferred_domestic_carrier_code=None)
            number_info = {
                "international_code": international_code,
                "full_number_normalized": full_number_normalized,
                "extension": parsed_number.extension,
            }
            return number_info
        except NumberParseException as e:
            logger.exception(f"Invalid phone number: {original_number}.", object=e)
            raise e

    def get_country_iso_code(self) -> str:
        contact_id = None  # user_context.get_effective_contact_id()
        profile_id = user_context.get_effective_profile_id()
        location_id = None  # user_context.get_effective_location_id()
        country_id = None  # user_context.get_effective_country_id()

        if not country_id:  # get country_id from location_id
            if not location_id:  # get location_id from contact_id or profile_id
                if contact_id and not profile_id:  # get profile_id from contact_id
                    profile_id = self.select_one_value_by_column_and_value(
                        schema_name="contact_profile",
                        view_table_name='contact_profile_view', select_clause_value='profile_id',
                        column_name='contact_id', column_value=contact_id)
                assert profile_id, "profile_id is required for getting location_id"
                location_id = self.select_one_value_by_column_and_value(
                    schema_name="location_profile",
                    view_table_name='location_profile_view', select_clause_value='location_id',
                    column_name='profile_id', column_value=profile_id)

            assert location_id, "location_id is required for getting country_id"
            country_id = self.select_one_value_by_column_and_value(
                schema_name="location", view_table_name='location_view', select_clause_value='country_id',
                column_name='location_id', column_value=location_id)

        country_iso_code = self.select_one_value_by_column_and_value(
            schema_name="country", view_table_name='country_ml_view', select_clause_value='iso',
            column_name='country_id', column_value=country_id)
        return country_iso_code

    # TODO: Is it really necessary to access the database for location?
    # I think it's possible to get the normalized phone number and the international code
    # from original_phone_number
    def process_phone(self, original_phone_number: str, country_iso_code: str = None, contact_id: int = None) -> dict:
        """
        Process phone number and return normalized phone number.
        :param original_phone_number: Original phone number.
        :param country_iso_code: Country ISO code.
        :param contact_id: Contact id.
        :return: Dictionary with the normalized phone number and the international code.
        """
        logger.start(object={'original_phone_number': original_phone_number})
        country_iso_code = country_iso_code or self.get_country_iso_code()
        normalized_phone_number = self.normalize_phone_number(
            original_number=original_phone_number, region=country_iso_code)
        phone_data = {
            'number_original': original_phone_number,
            'international_code': normalized_phone_number['international_code'],
            'full_number_normalized': normalized_phone_number['full_number_normalized'],
            'local_number_normalized': int(str(normalized_phone_number['full_number_normalized'])
                                           .replace(str(normalized_phone_number['international_code']), '')),
            'created_user_id': logger.user_context.get_effective_user_id(),
        }
        phone_id = self.insert(data_dict=phone_data)

        # link phone to profile
        profile_id = user_context.get_effective_profile_id()
        if profile_id:
            phone_profile_id = self.insert_mapping(
                schema_name='phone_profile',
                entity_name1='phone', entity_name2='profile', entity_id1=phone_id, entity_id2=profile_id)
        else:
            phone_profile_id = None

        # link phone to contact
        if contact_id:
            contact_phone_id = self.insert_mapping(
                schema_name='contact_phone', entity_name1='contact', entity_name2='phone',
                entity_id1=contact_id, entity_id2=phone_id)
        else:
            contact_phone_id = None

        result = {
            'phone_profile_id': phone_profile_id,
            'phone_id': phone_id,
            'normalized_phone_number': normalized_phone_number,
            'original_phone_number': original_phone_number,
            'contact_phone_id': contact_phone_id,
        }
        logger.end("success processing phone number", object=result)
        return result

    def insert_phone(self, phone_data: dict) -> int:
        """
        Insert phone data into the phone table.
        :param phone_data: Dictionary with the phone data.
        :return: Phone id.
        """
        logger.start(object={'phone_data': phone_data})
        phone_id = self.insert(data_dict=phone_data)
        logger.end("success inserting phone", object={'phone_id': phone_id})
        return phone_id

    def get_test_phone_id(self, number_original: str, international_code: int = 972) -> int:
        phone_data = {
            'number_original': number_original,
            'local_number_normalized': int(number_original[3:]),  # must be unique
            'full_number_normalized': f'+{international_code}{number_original[1:]}',
            'international_code': international_code,
            'area_code': int(number_original[1:3]),
            'extension': number_original[3],
        }
        return self.insert_phone(phone_data=phone_data)
