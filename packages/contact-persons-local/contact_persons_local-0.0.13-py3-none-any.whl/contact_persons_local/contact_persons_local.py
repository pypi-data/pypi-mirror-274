from .contact_persons_local_constants import CONTACT_PERSONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT
from logger_local.LoggerLocal import Logger
from database_mysql_local.generic_mapping import GenericMapping
from person_local.persons_local import PersonsLocal
from person_local.person import Person
from contact_local.contact_local import ContactsLocal      # noqa: E402

logger = Logger.create_logger(object=CONTACT_PERSONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

DEFAULT_SCHEMA_NAME = 'contact_person'
DEFAULT_ENTITY_NAME1 = 'contact'
DEFAULT_ENTITY_NAME2 = 'person'
DEFAULT_ID_COLUMN_NAME = 'contact_person_id'
DEFAULT_TABLE_NAME = 'contact_person_table'
DEFAULT_VIEW_TABLE_NAME = 'contact_person_view'

GENDER_ID = 8  # = Prefer not to respond


class ContactPersonsLocal(GenericMapping):
    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME, default_entity_name1: str = DEFAULT_ENTITY_NAME1,
                 default_entity_name2: str = DEFAULT_ENTITY_NAME2, default_id_column_name: str = DEFAULT_ID_COLUMN_NAME,
                 default_table_name: str = DEFAULT_TABLE_NAME, default_view_table_name: str = DEFAULT_VIEW_TABLE_NAME,
                 is_test_data: bool = False):

        GenericMapping.__init__(self, default_schema_name=default_schema_name, default_entity_name1=default_entity_name1,
                                default_entity_name2=default_entity_name2, default_id_column_name=default_id_column_name,
                                default_table_name=default_table_name, default_view_table_name=default_view_table_name,
                                is_test_data=is_test_data)
        self.persons_local = PersonsLocal()
        self.contacts_local = ContactsLocal()

    def insert_contact_and_link_to_existing_or_new_person(self, contact_dict: dict, contact_email_address: str,
                                                          contact_id: int) -> dict:
        """
        Insert contact and link to existing or new person
        :param contact_dict: contact dict
        :param contact_id: contact id
        :param is_test_data: is test data
        :return: contact_person_id
        """
        logger.start(object={"contact_dict": contact_dict, "contact_email_address": contact_email_address,
                             "contact_id": contact_id})
        result_dict = {}
        # TODO: also check if contact_person_id by phone number
        person_id = self.select_one_value_by_id(select_clause_value="person_id",
                                                id_column_name="contact_id",
                                                id_column_value=contact_id)
        if contact_email_address and person_id is None:
            # TODO: use upsert with both email_addresses and phone_numbers
            '''
            # old code
            person_id = self.persons_local.get_person_id_by_email_address(email_address=contact_email_address)
            '''
            person_id = self.persons_local.get_people_id(people_entity_name="person", ids_dict={"contact_id": contact_id})
        if person_id is None:
            # create new person and add it to person_table
            logger.info(log_message="person_id is None, creating new person")
            person_object = self._proccess_contact_dict_to_person_class(contact_dict=contact_dict,
                                                                        contact_email_address=contact_email_address)
            result = self.persons_local.insert_if_not_exists(person=person_object)
            if result:
                person_id = result[0]
            contact_person_id = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                    entity_name2=self.default_entity_name2,
                                                    entity_id1=contact_id, entity_id2=person_id,
                                                    ignore_duplicate=True)
            person_phone_ids = self.__insert_person_phones_mapping(person_id=person_id, contact_dict=contact_dict)
            email_address_person_ids = self.__insert_email_address_person_mapping(
                person_id=person_id, contact_dict=contact_dict)
            result_dict["person_phone_ids"] = person_phone_ids
            result_dict["email_address_person_ids"] = email_address_person_ids
        else:
            # link to existing person
            logger.info(log_message="person_id is not None, linking to existing person")
            mapping_tuple = self.select_multi_mapping_tuple_by_id(entity_name1=self.default_entity_name1,
                                                                  entity_name2=self.default_entity_name2,
                                                                  entity_id1=contact_id, entity_id2=person_id)
            if not mapping_tuple:
                logger.info(log_message="mapping_tuple is None, creating new mapping")
                contact_person_id = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                        entity_name2=self.default_entity_name2,
                                                        entity_id1=contact_id, entity_id2=person_id,
                                                        ignore_duplicate=True)
            else:
                # TODO: update person when persons-local will have a more generic update method
                logger.info(log_message="mapping_tuple is not None")
                contact_person_id = mapping_tuple[0][0]
        result_dict["person_id"] = person_id
        result_dict["contact_person_id"] = contact_person_id
        logger.end(object={"result_dict": result_dict})
        return result_dict

    def get_person_ids_by_contact_id(self, contact_id: int, limit: int = 1, order_by: str = "contact_person_id DESC") -> list:
        """
        Get person id by contact id
        :param contact_id: contact id
        :param limit: limit
        :param order_by: order by
        :return: person id
        """
        logger.start(object={"contact_id": contact_id})
        person_ids_tuple_list = self.select_multi_tuple_by_id(select_clause_value="person_id",
                                                              id_column_name="contact_id",
                                                              id_column_value=contact_id,
                                                              limit=limit,
                                                              order_by=order_by)
        person_ids = [person_id_tuple[0] for person_id_tuple in person_ids_tuple_list]
        logger.end(object={"person_ids": person_ids})
        return person_ids

    def _proccess_contact_dict_to_person_class(self, contact_dict: dict, contact_email_address: str) -> Person:
        """
        Process contact dict to person dict
        :param contact_dict: contact dict
        :return: person dict
        """
        logger.start(object={"contact_dict": contact_dict})
        person_object = Person(gender_id=GENDER_ID,
                               birthday_date=contact_dict['birthday'],
                               first_name=contact_dict['first_name'],
                               last_name=contact_dict['last_name'],
                               main_email_address=contact_email_address,
                               is_test_data=self.is_test_data)
        return person_object

    def __insert_person_phones_mapping(self, person_id: int, contact_dict: dict) -> list[int]:
        """
        Insert person phones mapping
        :param person_id: person id
        :param contact_dict: contact dict
        :return: person phone ids
        """
        logger.start(object={"person_id": person_id, "contact_dict": contact_dict})
        phone_numbers_ids = self.contacts_local.get_contact_phone_numbers_from_contact_dict(contact_dict=contact_dict)
        person_phone_ids = []
        for phone_number_id in phone_numbers_ids:
            person_phone_id = self.insert_mapping(
                schema_name="person_phone",
                entity_name1="person",
                entity_name2="phone",
                entity_id1=person_id,
                entity_id2=phone_number_id,
                ignore_duplicate=True
            )
            person_phone_ids.append(person_phone_id)
        logger.end(object={"person_phone_ids": person_phone_ids})
        return person_phone_ids

    def __insert_email_address_person_mapping(self, person_id: int, contact_dict: dict) -> list[int]:
        """
        Insert person emails mapping
        :param person_id: person id
        :param contact_dict: contact dict
        :return: person email ids
        """
        logger.start(object={"person_id": person_id, "contact_dict": contact_dict})
        email_addresses_ids = self.contacts_local.get_contact_email_addresses_from_contact_dict(contact_dict=contact_dict)
        emails_address_person_ids = []
        for email_address_id in email_addresses_ids:
            email_address_person_id = self.insert_mapping(
                schema_name="email_address_person",
                entity_name1="email_address",
                entity_name2="person",
                entity_id1=email_address_id,
                entity_id2=person_id,
                ignore_duplicate=True
            )
            emails_address_person_ids.append(email_address_person_id)
        logger.end(object={"emails_address_person_ids": emails_address_person_ids})
        return emails_address_person_ids
