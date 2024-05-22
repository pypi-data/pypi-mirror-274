from dotenv import load_dotenv
from datetime import datetime
from logger_local.Logger import Logger
from .organization_profile_constants import ORGANIZATION_PROFILE_PYTHON_PACKAGE_CODE_LOGGER_OBJECT
from database_mysql_local.generic_mapping import GenericMapping
load_dotenv()

logger = Logger(object=ORGANIZATION_PROFILE_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

DEFAULT_SCHEMA_NAME = "organization_profile"
DEFAULT_TABLE_NAME = "organization_profile_table"
DEFAULT_VIEW_NAME = "organization_profile_view"
DEFAULT_ID_COLUMN_NAME = "organization_profile_id"
DEFAULT_ENTITY_NAME1 = "organization"
DEFAULT_ENTITY_NAME2 = "profile"


class OrganizationProfilesLocal(GenericMapping):
    def __init__(self, is_test_data: bool = False):
        GenericMapping.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME,
                                default_table_name=DEFAULT_TABLE_NAME,
                                default_view_table_name=DEFAULT_VIEW_NAME,
                                default_id_column_name=DEFAULT_ID_COLUMN_NAME,
                                default_entity_name1=DEFAULT_ENTITY_NAME1,
                                default_entity_name2=DEFAULT_ENTITY_NAME2,
                                is_test_data=is_test_data)

    def insert_mapping(self, organization_id: int, profile_id: int, ignore_duplicate: bool = False) -> int:
        logger.start(object={"organization_id": organization_id, "profile_id": profile_id,
                             "ignore_duplicate": ignore_duplicate})
        organization_profile_id = GenericMapping.insert_mapping(self, entity_id1=organization_id, entity_id2=profile_id,
                                                                ignore_duplicate=ignore_duplicate)
        logger.end(object={"organization_profile_id": organization_profile_id})
        return organization_profile_id

    def insert_mapping_if_not_exists(self, organization_id: int, profile_id: int) -> int:
        logger.start(object={"organization_id": organization_id, "profile_id": profile_id})
        organization_profile_id = self.get_organization_profile_id(organization_id=organization_id, profile_id=profile_id)
        if organization_profile_id:
            logger.info(log_message="The link already exists",
                        object={"organization_id": organization_id, "profile_id": profile_id})
            logger.end(object={"organization_profile_id": organization_profile_id})
            return organization_profile_id
        organization_profile_id = self.insert_mapping(organization_id=organization_id, profile_id=profile_id)
        logger.end(object={"organization_profile_id": organization_profile_id})
        return organization_profile_id

    def get_profile_id_and_organization_id(self, organization_profile_id: int) -> dict[str, int]:
        logger.start(object={"organization_profile_id": organization_profile_id})
        result = self.select_one_dict_by_id(
            select_clause_value="organization_id, profile_id",
            id_column_name=DEFAULT_ID_COLUMN_NAME,
            id_column_value=organization_profile_id
        )
        logger.end(object={"result": result})
        return result

    def get_linked_profile_ids(self, organization_id: int) -> list[int]:
        logger.start(object={"organization_id": organization_id})
        profile_ids_tuple_list = self.select_multi_tuple_by_where(
            select_clause_value="profile_id",
            where="organization_id = %s",
            params=(organization_id,)
        )
        profile_ids_list = [profile_id for (profile_id,) in profile_ids_tuple_list]
        logger.end(object={"profile_ids_list": profile_ids_list})
        return profile_ids_list

    def get_linked_organization_ids(self, profile_id: int) -> list[int]:
        logger.start(object={"profile_id": profile_id})
        organization_ids_tuple_list = self.select_multi_tuple_by_where(
            select_clause_value="organization_id",
            where="profile_id = %s",
            params=(profile_id,)
        )
        organization_ids_list = [organization_id for (organization_id,) in organization_ids_tuple_list]
        logger.end(object={"organization_ids_list": organization_ids_list})
        return organization_ids_list

    # get organization ids linked to a profile id with updated_timestamp greater than remote_last_modified_timestamp
    def get_linked_organization_ids_with_updated_timestamp(self, profile_id: int,
                                                           remote_last_modified_timestamp: datetime) -> list[int]:
        logger.start(object={"profile_id": profile_id, "remote_last_modified_timestamp": remote_last_modified_timestamp})
        organization_ids_tuple_list = self.select_multi_tuple_by_where(
            select_clause_value="organization_id",
            where="profile_id = %s AND updated_timestamp > %s",
            params=(profile_id, remote_last_modified_timestamp)
        )
        organization_ids_list = [organization_id for (organization_id,) in organization_ids_tuple_list]
        logger.end(object={"organization_ids_list": organization_ids_list})
        return organization_ids_list

    def get_organization_profile_id(self, organization_id: int, profile_id: int) -> int | None:
        logger.start(object={"organization_id": organization_id, "profile_id": profile_id})
        organization_profile_id_dict = self.select_one_dict_by_where(
            select_clause_value="organization_profile_id",
            where="organization_id = %s AND profile_id = %s",
            params=(organization_id, profile_id)
        )
        organization_profile_id = organization_profile_id_dict.get("organization_profile_id", None)
        logger.end(object={"organization_profile_id": organization_profile_id})
        return organization_profile_id
