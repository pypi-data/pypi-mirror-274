import csv
import sys
import os

from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
load_dotenv()
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))

from contact_email_address_local.contact_email_addresses_local import ContactEmailAdressesLocal
from contact_group_local.contact_group import ContactGroups
from contact_local.contact_local import ContactsLocal
from contact_location_local.contact_location_local import ContactLocationLocal
from contact_notes_local.contact_notes_local import ContactNotesLocal
from contact_persons_local.contact_persons_local import ContactPersonsLocal
from contact_phone_local.contact_phone_local import ContactPhoneLocal
from contact_profile_local.contact_profiles_local import ContactProfilesLocal
from contact_user_external_local.contact_user_external_local import ContactUserExternalLocal
from database_mysql_local.generic_crud import GenericCRUD
from database_mysql_local.point import Point
from importer_local.ImportersLocal import ImportersLocal
from internet_domain_local.internet_domain_local import DomainLocal
from location_local.country import Country
from location_local.location_local_constants import LocationLocalConstants
from logger_local.MetaLogger import MetaLogger
from organization_profile_local.organization_profiles_local import OrganizationProfilesLocal
from organizations_local.organizations_local import OrganizationsLocal
# import pycountry
from phonenumbers import NumberParseException
from user_context_remote.user_context import UserContext
from user_external_local.user_externals_local import UserExternalsLocal
from data_source_local.data_source import DataSources

from .contact_person_profile_csv_imp_local_constants import CSVToContactPersonProfileConstants

# from contact_local.contact_local import ContactsLocal
# from database_mysql_local.generic_crud import GenericCRUD
# from logger_local.LoggerLocal import Logger
# from text_block_local.text_block import TextBlocks
# from user_context_remote.user_context import UserContext

CLASS_NAME = "CSVToContactPersonProfile"
CONTACT_PERSON_PROFILE_CSV_SYSTEM_ID = 1
DEFAULT_LOCATION_ID = LocationLocalConstants.UNKNOWN_LOCATION_ID
DEFAULT_PROFILE_ID = 0


# Those methods should be called from the common method for this repo (contact-person-profile-csv-imp-local-python-package and google-contact-sync ...)

# TODO def process_first_name( original_first_name: str) -> str: (move to people-local-python-package)
#     normilized_first_name = the first word in original_first_name
#     GroupsLocal.add_update_group_and_link_to_contact( normilized_first_name, is_group=true, contact_id) # When checking if exists, ignore the upper-case lower-case
#     return normilized_first_name

# TODO def process_last_name( original_last_name : str) -> str: (move to people-local-python-package)
#     normilized_last_name = Remove all the digits from the last_name
#     GroupsLocal.add_update_group_and_link_to_contact( normilized_last_name, is_group=true, contact_id) # When checking if exists, ignore the upper-case lower-case

# TODO def process_phone( original_phone_number: str) -> str: (move to phone-local-python-package)
#     phone_id, normalized_phone = PhonesLocal.link_phone_to_contact( normilized_phone, contact_id) # Please use method written by @akiva and return normalized_phone_number

# TODO def process_job_title( job_title: str) -> str: (move to people-local-python-package)
#     normalized_job_title = GroupsLocal.add_update_group_and_link_to_contact( job_title, is_group=true, contact_id) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_email_address( email_address: str)
#          """ Returned email_address_id, domain_name, organization_name """
#           DomainsLocal.link_contact_to_domain( contact_id, domain_name )

# TODO def process_organization( organization_name: str, email_address: str) -> str: (move to people-local-python-package
#     if organization_name == None or empty
#          organization_name = extract_organization_from_email_address( email_address)
#     normalized_organization_name = GroupsLocal.add_update_group_and_link_to_contact( organization_name, is_organization=true) # When checking if the organization exists, remove suffix such as Ltd, Inc, בעמ... when searching ignore the uppper-case lower-case

# TODO def process_department( department_name: str) -> str: (move to people-local-python-package
#     normalized_department_name = GroupsLocal.add_update_group_and_link_to_contact( department_name, is_department=true) # When searching ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_continent( continent_name: str) -> str: (move to location-local-python-package)
#     continent_id, normalized_continent_name = GroupsLocal.add_update_group_and_link_to_contact( continent_name, is_continent=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_country( country_name: str) -> str: (move to location-local-python-package)
#     country_id, normalized_country_name = GroupsLocal.add_update_group_and_link_to_contact( country_name, is_country=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_state( state_name: str) -> str: (move to location-local-python-package)
#     state_id, normalized_state_name = GroupsLocal.add_update_group_and_link_to_contact( state_name, is_state=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_county_in_state( county_in_state_name_id: id) -> str: (move to location-local-python-package)
#     country_id, normalized_county_name = GroupsLocal.add_update_group_and_link_to_contact( county_in_state_id, is_county=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_region( region_name: str) -> str: (move to location-local-python-package)
#     region_id, normalized_region_name = GroupsLocal.add_update_group_and_link_to_contact( region_name, is_region=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_neighbourhood_in_city( neighbourhood_in_city_id: str) -> str: (move to location-local-python-package)
#     neighbourhood_id, normalized_neighbourhood_name = GroupsLocal.add_update_group_and_link_to_contact( neighbourhood_in_city_id, is_neighbourhood=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_street_in_city( street_in_city_id: int) -> str: (move to location-local-python-package)
#     street_id, normalized_street_name = GroupsLocal.add_update_group_and_link_to_contact( street_in_city_id, is_street=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_building_in_street( location_id: int) -> str: (move to location-local-python-package)
#     location_id, normalized_building_address_name = GroupsLocal.add_update_group_and_link_to_contact( location_id, is_street=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_website


class CSVToContactPersonProfile(GenericCRUD, metaclass=MetaLogger,
                                object=CSVToContactPersonProfileConstants.CSV_LOCAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        GenericCRUD.__init__(self, default_schema_name="field", default_column_name="field_id",
                             default_table_name="field_table", default_view_table_name="field_view",
                             is_test_data=is_test_data)
        self.contact_entity_type_id = self.select_one_value_by_id(
            schema_name="entity_type", view_table_name="entity_type_ml_en_view",
            select_clause_value="entity_type_id", column_name="title", column_value="Contact")
        self.user_context = UserContext()
        self.organization_profiles = OrganizationProfilesLocal(is_test_data=is_test_data)
        self.contact_persons = ContactPersonsLocal(is_test_data=is_test_data)
        self.contact_user_external = ContactUserExternalLocal(is_test_data=is_test_data)
        self.contact_profiles = ContactProfilesLocal(is_test_data=is_test_data)
        self.contact_groups = ContactGroups(is_test_data=is_test_data)
        self.contact_email_addresses = ContactEmailAdressesLocal(is_test_data=is_test_data)
        self.contact_phone = ContactPhoneLocal(is_test_data=is_test_data)
        self.contact_location = ContactLocationLocal(is_test_data=is_test_data)
        self.contacts_local = ContactsLocal(is_test_data=is_test_data)
        self.user_externals_local = UserExternalsLocal(is_test_data=is_test_data)
        self.organizations_local = OrganizationsLocal(is_test_data=is_test_data)
        self.domain_local = DomainLocal(is_test_data=is_test_data)
        self.importers_local = ImportersLocal()
        self.data_sources = DataSources()

    # # TODO Does this function should be here on in https://github.com/circles-zone/variable-local-python-package/tree/dev/variable_local_python_package/variable_local/src "field/field.py"?
    # def __get_field_name(self, field_id: int, data_source_type_id: int) -> str:
    #     """
    #     Get the field name from the database
    #     :param field_id: The field ID
    #     :param data_source_type_id: The data source ID
    #     :return: The field name
    #     """
    #     
    #                  'data_source_type_id': data_source_type_id})

    #     self.set_schema(schema_name="data_source_field")
    #     data_source_field_tuples = self.select_multi_tuple_by_where(view_table_name="data_source_field_view",  
    #                                             select_clause_value="external_field_name",  
    #                                             where="data_source_type_id = %s AND field_id = %s",  
    #                                             params=(data_source_type_id, field_id))  

    #     if data_source_field_tuples:
    #         
    #         return data_source_field_tuples[0][0]
    #     return

    # TODO what are the diff between csv_path and directory_name?
    # ans: csv_path is the full path to the csv file, directory_name is the directory where the csv file is located 

    # TODO I think file name should be after directory_name and csv_path
    # ans: it cannot be after directory_name and csv_path because it is a required parameter 

    # TODO: break this function into smaller functions
    def insert_update_contact_from_csv(
            self, *, data_source_type_id: int, file_name: str = None, user_external_username: str,
            # TODO Add support to criteria_set_id
            directory_name: str = None, csv_path: str = None, start_index: int = 0, end_index: int = None) -> dict:
        """
        Insert contacts from CSV file to the database
        :param data_source_type_id: The data source ID
        :param file_name: The CSV file name
        :param user_external_username: The user external username
        :param directory_name: The CSV file directory name if it wasn't given it will search for the file in the same directory
        :param csv_path: The CSV file path if it wasn't given it will search for the file in the same directory
        :param start_index: The start index
        :param end_index: The end index
        :return: 
        """

        # TODO Please explain
        # if csv_path is provided then we will use the full path
        # if csv_path is not provided then we will use the directory_name and file_name to create the full path 
        # if directory_name is not provided the assumption is that the file is in the same directory as the script and not in a folder 
        if csv_path is not None:
            csv_file_path = csv_path
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_file_path = os.path.join(script_dir, directory_name or '', file_name)
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"File {csv_file_path} not found")

        contact_fields_to_keep = (
            'name_prefix', 'additional_name', 'name_suffix', 'nickname', 'full_name', 'title', 'department', 'notes',
            'first_name', 'last_name', 'phone1', 'phone2', 'phone3', 'birthday', 'email1', 'email2', 'email3',
            'hashtag',
            'website1', 'handle', 'address1_street', 'address1_city', 'address1_state', 'address1_postal_code',
            'address1_country', 'address2_street', 'address2_city', 'address2_state', 'address2_postal_code',
            'address2_country', 'job_title', 'organization', 'display_as')

        user_external_id = self.__get_user_external_id(user_external_username)
        # We create a new data_source_instance_id everytime we import a new csv file
        data_source_instance_id = self.__get_data_source_instance_id(
            data_source_type_id=data_source_type_id, csv_file_path=csv_file_path,
            user_external_id=user_external_id, file_name=file_name, 
            user_external_username=user_external_username,
            start_index=start_index, end_index=end_index
        )
        fields_dictonary = self.data_sources.get_fields_name_from_csv(data_source_type_id)
        keys = list(fields_dictonary.keys())
        contact_data_by_contact_id_dict = {}
        # TODO: break this into smaller functions
        with (open(csv_file_path, 'r', encoding='utf-8') as csv_file):
            for row_index, row in enumerate(csv.DictReader(csv_file)):
                if end_index is not None and not start_index <= row_index <= end_index:
                    continue
                csv_keys = list(row.keys())
                contact_data = {}
                '''
                # Old version
                for fields in keys:
                    if fields_dictonary[fields] not in csv_keys:
                        continue
                    if fields_dictonary[fields] is not None and isinstance(fields_dictonary[fields], str):
                        contact_data[fields] = row[fields_dictonary[fields]]
                    else:
                        contact_data[fields] = None
                '''
                splitter = ' ::: '
                for field in keys:
                    field_value = fields_dictonary.get(field)
                    if field_value not in csv_keys:
                        continue

                    if field_value is not None and isinstance(field_value, str):
                        if splitter in row[field_value]:
                            values_list = row[field_value].split(splitter)
                            for index, value in enumerate(values_list):
                                current_field = field.replace('1', str(index + 1))
                                if not contact_data.get(current_field):
                                    contact_data[current_field] = value
                        elif not contact_data.get(field):
                            contact_data[field] = row[field_value]
                    else:
                        contact_data[field] = None

                contact_data = {key: contact_data.get(key) or None for key in contact_fields_to_keep}
                if (not contact_data.get('first_name')
                    and not contact_data.get('last_name')
                    and not contact_data.get('organization')):
                    continue
                contact_data['is_test_data'] = self.is_test_data

                # TODO Please call get_display_name(first_name, last_name, organization) if display_as is empty

                # for phone in ['phone1', 'phone2', 'phone3']:
                #     if contact_data[phone] is None:
                #         continue
                #     phone_data = process_phone(original_phone_number=contact_data[phone])
                #     if phone_data is None:
                #         continue
                #     else:
                #         contact_data[phone] = phone_data['normalized_phone_number']

                # contact_data['first_name'] = process_first_name(
                #     original_first_name=contact_data['first_name'])
                # contact_data['last_name'] = process_last_name(
                #     original_last_name=contact_data['last_name'])

                # TODO This should be executed also by Google Contact Sync (please make sure it is in people-local-python-package
                #   i.e. get_display_name(first_name, last_name, organization) -> str
                if contact_data.get('display_as') is None:
                    contact_data['display_as'] = contact_data.get('first_name') or ""  # prevent None
                    if (contact_data.get('last_name')
                            and not contact_data.get('last_name').isdigit()):
                        contact_data['display_as'] += " " + contact_data['last_name']
                    if not contact_data['display_as'] and contact_data.get('organization'):
                        contact_data['display_as'] += " " + contact_data['organization']

                    # TODO if contact_data['display_as'] still empty raise?

                # TODO process_notes( contact_data[notes] )

                # TODO We should take care of situation which the contact already exists and we need to update it
                contact_data["data_source_instance_id"] = data_source_instance_id
                contact_data["source"] = "Import"
                contact_id = self.contacts_local.upsert_contact_dict(contact_dict=contact_data)
                if contact_id:
                    self.__insert_contact_details_to_db(
                        contact_id=contact_id, contact_dict=contact_data, user_external_id=user_external_id,
                        data_source_instance_id=data_source_instance_id,
                        data_source_type_id=data_source_type_id)
                    contact_data_by_contact_id_dict[contact_id] = contact_data
                # groups_linked_by_job_title = process_job_title(contact_id=contact_id, job_title=contact_data['job_title'])
                # if groups_linked_by_job_title is None:
                #     logger.info("No groups linked by job title to contact " + str(contact_id))


        return contact_data_by_contact_id_dict


    # TODO def insert_update_contact_groups_from_contact_notes( contact_notes: str) -> int:
    # TODO Add contact_group with seq, attribute, is_sure using group-local-python-package

    # TODO def process_people_url( people_url ) -> str:
    # TODO Use regex to extract the data from the URL
    # TODO add to user_external using user-external-python-package
    @staticmethod
    def process_url(original_url: str) -> str:
        prefixes = ['http://', 'https://']
        for prefix in prefixes:
            if original_url.startswith(prefix):
                original_url = original_url[len(prefix):]
                break
        if original_url.endswith('/'):
            original_url = original_url[:-1]

        return original_url

    # TODO: add a method to add notes to text_block process them to retrieve the groups and create and link the groups to the user 

    def process_notes(self, contact_note: str) -> None:
        # TODO number_of_system_recommednded_groups_identified_in_contact_notes = get_system_recommended_groups_from_contact_notes( contact_notes: str)

        # TODO loop on all contact URLs/websites
        # TODO process_people_url( process_url( people_url ) )

        # TODO Process emails in the contact notes
        # Add or update the emails as a separate contact if they do not exist in contact_table

        # TODO Process contact notes using text-block-local-python-package

        # TODO Process the date in the contact notes and insert/update the person_milestones_table

        # TODO Process actions items after "---" and insert into action_items_table

        pass

    def get_location_type_id_by_name(self, location_type_name: str) -> int or None:
        """
        Get the location type ID by its name
        :param location_type_name: The location type name
        :return: The location type ID    
        """
        location_type_id = self.select_one_value_by_id(
            schema_name="location", view_table_name="location_type_ml_view",
            select_clause_value="location_type_id", column_name="title", column_value=location_type_name)
        return location_type_id

    def __insert_contact_details_to_db(self, contact_id: int, contact_dict: dict, user_external_id: int,
                                       data_source_instance_id: int, data_source_type_id: int) -> int:
        
        location_id = DEFAULT_LOCATION_ID
        # insert organization
        organization_id = self.__insert_organization(contact_dict=contact_dict)

        # insert link contact_location
        # The location is in contact_dict
        location_results = self.__insert_link_contact_location(
            contact_dict=contact_dict, contact_id=contact_id)
        if location_results:
            location_id = location_results[0].get(
                "location_id") or DEFAULT_LOCATION_ID

        # insert link contact_group
        self.__insert_link_contact_groups(
            contact_dict=contact_dict, contact_id=contact_id)

        # insert link contact_persons
        self.__insert_link_contact_persons(
            contact_dict=contact_dict, contact_id=contact_id)

        # insert link contact_profiles
        contact_profile_info = (
            self.__insert_contact_profiles(
                contact_dict=contact_dict, contact_id=contact_id)
        )
        if contact_profile_info is not None:
            profile_id = contact_profile_info.get(
                "profile_id") or DEFAULT_PROFILE_ID
        else:
            profile_id = DEFAULT_PROFILE_ID

        # insert organization-profile
        self.__insert_organization_profile(
            organization_id=organization_id, profile_id=profile_id)

        # insert link contact_email_addresses
        self.__insert_link_contact_email_addresses(
            contact_dict=contact_dict, contact_id=contact_id)

        # insert link contact_notes
        self.__insert_link_contact_notes_and_text_blocks(contact_dict=contact_dict,
                                                         contact_id=contact_id,
                                                         profile_id=profile_id)

        # insert link contact_phones
        self.__insert_link_contact_phones(
            contact_dict=contact_dict, contact_id=contact_id)

        # inset link contact_user_externals
        self.__insert_link_contact_user_external(
            contact_dict=contact_dict, contact_id=contact_id)

        # insert link contact_internet_domains
        self.__insert_link_contact_domains(
            contact_dict=contact_dict, contact_id=contact_id)

        importer_id = self.__insert_importer(
            contact_id=contact_id, location_id=location_id,
            user_external_id=user_external_id,
            google_people_api_resource_name=contact_dict.get("resource_name"),
            data_source_instance_id=data_source_instance_id,
            data_source_type_id=data_source_type_id
        )
        return importer_id
        
    def __insert_organization(self, contact_dict: dict) -> int or None:
        
        if not contact_dict.get("organization"):
            return
        organization_dict = self.__create_organization_dict(
            organization_name=contact_dict.get("organization"))
        organization_upsert_result = self.organizations_local.upsert_organization(
            organization_dict=organization_dict)
        organization_id = organization_upsert_result.get("organization_id")
        organization_ml_ids_list = organization_upsert_result.get("organization_ml_ids_list")  # noqa
        
        return organization_id

    def __create_organization_dict(self, organization_name: str) -> dict:
        
        organization_dict = {
            "is_approved": 0,
            "is_main": 1,
            "point": Point(0, 0),  # TODO: how are we supposed to get the point?
            "location_id": LocationLocalConstants.UNKNOWN_LOCATION_ID,
            # TODO: how are we supposed to get the location_id?
            "profile_id": 0,  # TODO: how are we supposed to get the profile_id?
            "parent_organization_id": 1,
            "non_members_visibility_scope_id": 0,
            "members_visibility_scope_id": 0,
            "Non_members_visibility_profile_id": 0,
            "created_user_id": self.user_context.get_effective_user_id(),
            "created_real_user_id": self.user_context.get_real_user_id(),
            "created_effective_user_id": self.user_context.get_effective_user_id(),
            "created_effective_profile_id": self.user_context.get_effective_profile_id(),
            "updated_user_id": self.user_context.get_effective_user_id(),
            "updated_real_user_id": self.user_context.get_real_user_id(),
            "updated_effective_user_id": self.user_context.get_effective_user_id(),
            "updated_effective_profile_id": self.user_context.get_effective_profile_id(),
            "main_group_id": 1,
            "lang_code": self.user_context.get_effective_profile_preferred_lang_code_string(),  # TODO: is this correct?
            "name": organization_name,
            "title": organization_name,
            "is_name_approved": 0,
            "is_description_approved": 0
        }
        
        return organization_dict

    def __insert_organization_profile(self, organization_id: int, profile_id: int) -> int or None:
        
        if not organization_id or not profile_id:
            
            return

        organization_profile_id = self.organization_profiles.insert_mapping_if_not_exists(
            organization_id=organization_id, profile_id=profile_id)
        
        return organization_profile_id

    def __insert_link_contact_groups(self, contact_dict: dict, contact_id: int) -> list:
        
        groups = []
        groups_linked = None
        if contact_dict.get("organization"):
            groups.append(contact_dict.get("organization"))
        if contact_dict.get("job_title"):
            groups.append(contact_dict.get("job_title"))
        if len(groups) > 0:
            groups_linked = self.contact_groups.insert_link_contact_group_with_group_local(
                contact_id=contact_id, groups=groups)
        
        return groups_linked

    def __insert_link_contact_persons(self, contact_dict: dict, contact_id: int) -> int:
        
        contact_person_results_dict = self.contact_persons.insert_contact_and_link_to_existing_or_new_person(
            contact_dict=contact_dict,
            contact_email_address=contact_dict["email1"],
            contact_id=contact_id
        )
        contact_person_id = contact_person_results_dict.get("contact_person_id")
        
        return contact_person_id

    def __insert_link_contact_email_addresses(self, contact_dict, contact_id) -> list[int]:
        
        email_addresses = self.contacts_local.get_contact_email_addresses_from_contact_dict(
            contact_dict=contact_dict)
        contact_email_addresses = self.contact_email_addresses
        contact_email_address_ids = []
        for email_address in email_addresses:
            contact_email_address_id = contact_email_addresses.insert_contact_and_link_to_email_address(
                contact_dict=contact_dict,
                contact_email_address_str=email_address,
                contact_id=contact_id
            )
            contact_email_address_ids.append(contact_email_address_id)
        
        return contact_email_address_ids

    @staticmethod
    def __insert_link_contact_notes_and_text_blocks(
            *, contact_dict: dict, contact_id: int, profile_id: int) -> int or None:
        if not contact_dict.get("notes"):
            return
        # TODO: I think we should change ContactNotesLocal - send the args to the method and not the class
        contact_notes = ContactNotesLocal(contact_dict=contact_dict, contact_id=contact_id, profile_id=profile_id)
        insert_information = contact_notes.insert_contact_notes_text_block()
        contact_note_id = insert_information.get("contact_note_id")
        return contact_note_id

    def __insert_link_contact_phones(self, contact_dict: dict, contact_id: int) -> list[int]:
        
        phone_numbers = self.contacts_local.get_contact_phone_numbers_from_contact_dict(contact_dict=contact_dict)
        contact_phone_ids = []
        for phone_number in phone_numbers:
            contact_phone_id = self.contact_phone.insert_contact_and_link_to_existing_or_new_phone(
                contact_dict=contact_dict,
                phone_number=phone_number,
                contact_id=contact_id
            )
            contact_phone_ids.append(contact_phone_id)
        
        return contact_phone_ids

    def __insert_link_contact_user_external(self, contact_dict: dict, contact_id: int) -> int:
        
        contact_user_external_id = self.contact_user_external.insert_contact_and_link_to_existing_or_new_user_external(
            contact_dict=contact_dict,
            contact_email_address=contact_dict["email1"],
            contact_id=contact_id,
            user_external_dict={"username": contact_dict["email1"]}
        )
        
        return contact_user_external_id

    def __insert_contact_profiles(self, contact_dict: dict, contact_id: int) -> dict:
        
        insert_information = self.contact_profiles.insert_and_link_contact_profile(
            contact_dict=contact_dict,
            contact_id=contact_id
        )
        
        return insert_information

    def __insert_link_contact_domains(self, contact_dict: dict, contact_id: int) -> list[dict]:
        
        website_count = 1
        website_url = contact_dict.get("website" + str(website_count))
        domain_insert_information_list = []
        while website_url:
            domain_insert_information = self.domain_local.link_contact_to_domain(
                contact_id=contact_id, url=website_url)
            domain_insert_information_list.append(domain_insert_information)
            website_count += 1
            website_url = contact_dict.get("website" + str(website_count))
        
        return domain_insert_information_list

    def __insert_link_contact_location(self, contact_dict: dict, contact_id: int) -> list[dict] or None:
        
        location_dicts = self.__procces_location_of_contact(contact_dict)
        if not location_dicts:
            return
        location_results = [self.contact_location.insert_contact_and_link_to_location(
            location_dict=location_dict, contact_id=contact_id)
            for location_dict in location_dicts]

        return location_results

    def __insert_importer(self, contact_id: int, location_id: int, user_external_id: int,
                          google_people_api_resource_name: str, data_source_type_id: int,
                          data_source_instance_id: int) -> int:
        # TODO: Shall we consider the url of csv's as the following? Use Sql2Code. Use const enum
        if data_source_type_id == 16:
            url = "www.google.com"
        elif data_source_type_id == 17:
            url = "www.outlook.com"
        elif data_source_type_id == 18:
            url = "www.linkedin.com"
        else:
            raise ValueError("data_source_type_id is not valid")
        importer_id = self.importers_local.insert(
            data_source_type_id=data_source_type_id,
            data_source_instance_id=data_source_instance_id,
            location_id=location_id,
            entity_type_id=self.contact_entity_type_id,
            entity_id=contact_id, url=url,
            user_external_id=user_external_id,
            google_people_api_resource_name=google_people_api_resource_name
        )
        
        return importer_id

    def __procces_location_of_contact(self, contact_dict: dict) -> dict or None:
        """
        Process location of Google contact
        :param contact_dict: location_dict
        :return: location_dict
        """
        
        address_street1 = contact_dict.get("address1_street")
        address_city1 = contact_dict.get("address1_city")
        address_state1 = contact_dict.get("address1_state")
        address_postal_code1 = contact_dict.get("address1_postal_code")
        address_country1 = contact_dict.get("address1_country")
        address_street2 = contact_dict.get("address2_street")
        address_city2 = contact_dict.get("address2_city")
        address_state2 = contact_dict.get("address2_state")
        address_postal_code2 = contact_dict.get("address2_postal_code")
        address_country2 = contact_dict.get("address2_country")
        is_contact_location1 = (address_street1 or address_city1 or address_state1
                                or address_postal_code1 or address_country1)
        is_contact_location2 = (address_street2 or address_city2 or address_state2
                                or address_postal_code2 or address_country2)

        phone_numbers_list = self.__get_phone_numbers_list(contact_dict)
        email_addresses_list = self.__get_email_addresses_list(contact_dict)
        if (not is_contact_location1 
                and not is_contact_location2
                and not phone_numbers_list 
                and not email_addresses_list):
            return
        # TODO: How can we add location type?
        proccessed_location_dicts = []
        if is_contact_location1:
            location_dict = self.__create_location_dict(
                address_street=address_street1,
                address_city=address_city1,
                address_postal_code=address_postal_code1,
                address_country=address_country1,
                address_state=address_state1
            )
            proccessed_location_dicts.append(location_dict)
        if is_contact_location2:
            location_dict = self.__create_location_dict(
                address_street=address_street2,
                address_city=address_city2,
                address_postal_code=address_postal_code2,
                address_country=address_country2,
                address_state=address_state2
            )
            proccessed_location_dicts.append(location_dict)
        for phone_number in phone_numbers_list:
            try:
                country = Country.get_country_name_by_phone_number(phone_number)
            except NumberParseException as number_parse_exception:
                self.logger.error("Error while parsing phone number",
                                 object={"number_parse_exception": number_parse_exception})
                continue
            except Exception as exception:
                self.logger.error("Error while getting country name by phone number",
                                 object=exception)
                continue
            currect_location_dict = {
                "address_local_language": None,
                "city": None,
                "postal_code": None,
                "country": country,
                "coordinate": LocationLocalConstants.DEFAULT_COORDINATE,
                "neighborhood": LocationLocalConstants.DEFAULT_NEGIHBORHOOD_NAME,
                "county": LocationLocalConstants.DEFAULT_COUNTY_NAME,
                "state": LocationLocalConstants.DEFAULT_STATE_NAME,
                "region": LocationLocalConstants.DEFAULT_REGION_NAME,
            }
            proccessed_location_dicts.append(currect_location_dict)
        for email_address in email_addresses_list:
            country = Country.get_country_name_by_email_address(email_address)
            currect_location_dict = {
                "address_local_language": None,
                "city": None,
                "postal_code": None,
                "country": country,
                "coordinate": Point(0, 0),
                "neighborhood": LocationLocalConstants.DEFAULT_NEGIHBORHOOD_NAME,
                "county": LocationLocalConstants.DEFAULT_COUNTY_NAME,
                "state": LocationLocalConstants.DEFAULT_STATE_NAME,
                "region": LocationLocalConstants.DEFAULT_REGION_NAME,
            }
            proccessed_location_dicts.append(currect_location_dict)
        
        return proccessed_location_dicts

    @staticmethod
    def __create_location_dict(*, address_street: str, address_city: str, address_postal_code: str,
                               address_country: str, address_state: str) -> dict:
        location_dict = {
            "address_local_language": address_street,
            "city": address_city,
            "postal_code": address_postal_code,
            "country": address_country,
            "coordinate": Point(0, 0),
            "neighborhood": LocationLocalConstants.DEFAULT_NEGIHBORHOOD_NAME,
            "county": LocationLocalConstants.DEFAULT_COUNTY_NAME,
            "state": address_state or LocationLocalConstants.DEFAULT_STATE_NAME,
            "region": LocationLocalConstants.DEFAULT_REGION_NAME,
        }
        
        return location_dict

    @staticmethod
    def __get_phone_numbers_list(contact_dict: dict) -> list:
        phones_list = [contact_dict.get(f"phone{i}") for i in range(1, 4) if contact_dict.get(f"phone{i}")]
        return phones_list

    @staticmethod
    def __get_email_addresses_list(contact_dict: dict) -> list:
        emails_list = [contact_dict.get(f"email{i}") for i in range(1, 4) if contact_dict.get(f"email{i}")]
        # TODO use enum const for "email1" ....
        return emails_list

    def __get_user_external_id(self, user_external_username: str) -> int or None:
        
        user_external_id = self.user_externals_local.select_one_value_by_id(
            select_clause_value="user_external_id", column_name="username",
            column_value=user_external_username, order_by="user_external_id DESC")
        if user_external_id is None:
            self.user_externals_local.insert_or_update_user_external_access_token(
                username=user_external_username,
                profile_id=self.user_context.get_effective_profile_id(),
                system_id=CONTACT_PERSON_PROFILE_CSV_SYSTEM_ID,
                access_token=""
            )
            user_external_id = self.user_externals_local.select_one_value_by_id(
                select_clause_value="user_external_id", column_name="username",
                column_value=user_external_username, order_by="user_external_id DESC")

        return user_external_id

    def __get_data_source_instance_id(self, data_source_type_id: int, csv_file_path: str, user_external_id: int, file_name: str,
                                      user_external_username: str, start_index: int, end_index: int) -> int:
        name = datetime.now(ZoneInfo("UTC")).strftime("%y%m%d %H%M%S") + " " + \
            user_external_username + " 'Google Contact- Google Contact CSV'"
        data_source_instance_id = self.insert(
            schema_name="data_source_instance",
            table_name="data_source_instance_table",
            data_dict={
                "name": name,
                "data_source_type_id": data_source_type_id,
                "file_or_api": "file",
                "path": csv_file_path,
                "filename": file_name,
                "computer_name": None,
                "user_external_id": user_external_id,
                "start_index": start_index,
                "end_index": end_index,
            }
        )
        return data_source_instance_id
