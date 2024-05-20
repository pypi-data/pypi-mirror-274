from .jobs_local_constants import JobsLocalConstants

from database_mysql_local.generic_crud import GenericCRUD
from database_mysql_local.generic_mapping import GenericMapping
from logger_local.LoggerLocal import Logger
from group_local.group_local import GroupLocal
from group_remote.group_remote import GroupsRemote
from language_remote.lang_code import LangCode

logger = Logger.create_logger(object=JobsLocalConstants.JOBS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)


DEFAULT_SCHEMA_NAME = "job_title"
DEFAULT_TABLE_NAME = "job_title_table"
DEFAULT_ML_TABLE_NAME = "job_title_ml_table"
DEFAULT_VIEW_TABLE_NAME = "job_title_view"
DEFAULT_ID_COLUMN_NAME = "job_title_id"
DEFAULT_ML_ID_COLUMN_NAME = "job_title_ml_id"


class JobsLocal(GenericCRUD):

    def __init__(self, is_test_data: bool = False):
        GenericCRUD.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME, default_table_name=DEFAULT_TABLE_NAME,
                             default_id_column_name=DEFAULT_ID_COLUMN_NAME,
                             is_test_data=is_test_data)

    def process_job_title(contact_id: int, job_title: str) -> list[tuple[int, str]]:
        """
        Process the job title for a contact by checking if related groups exist and linking them.

        Args:
        - contact_id (int): The ID of the contact.
        - job_title (str): The job title associated with the contact.

        Returns:
        - List[Tuple[int, str]]: A list of tuples containing linked group IDs and titles.
        """
        if job_title is None:
            return []
        # Creating an instance of GenericMapping
        generec_mapping = GenericMapping(
            default_entity_name1='contact', default_entity_name2='group', default_schema_name='contact_group')

        # Retrieving all group names
        groups_names = GroupLocal().get_all_groups_names()

        # Initializing lists to store groups to link and groups that are successfully linked
        groups_to_link = []
        groups_linked = []

        # Iterating through group names to find matching groups based on job_title
        for group in groups_names:
            if group is None:
                continue
            if job_title in group:
                groups_to_link.append(group)

        # If no matching groups found based on job_title
        if len(groups_to_link) == 0:
            # Creating a new group with the job_title
            title = job_title
            lang_code = LangCode.detect_lang_code_str_restricted(text=title, default_lang_code='en')
            # TODO Why do we need the 1st parameter?
            group_id = GroupsRemote().create_group(
                title_lang_code=lang_code,
                is_interest=True, title=title)
            # Inserting mapping between contact and the newly created group
            generec_mapping.insert_mapping(entity_name1='contact', entity_name2='group',
                                           entity_id1=contact_id, entity_id2=group_id)
            groups_linked.append((group_id, title))
        else:
            # Linking contact with existing groups found based on job_title
            for group in groups_to_link:
                group_id = GroupsRemote().get_group_response_by_group_name(
                    group_name=group).json()['data'][0]['id']
                generec_mapping.insert_mapping(entity_name1='contact', entity_name2='group',
                                               entity_id1=contact_id, entity_id2=group_id)
                groups_linked.append((group_id, group))

        # Logging the success of processing job title and returning linked group IDs and titles

        # TODO Please add a suffix to all relevant variables i.e. groups_linked
        return groups_linked
