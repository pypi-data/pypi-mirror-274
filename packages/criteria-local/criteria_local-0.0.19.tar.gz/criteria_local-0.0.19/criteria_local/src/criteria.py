from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .constants import LOGGER_CRITERIA_CODE_OBJECT, PEOPLE_ENTITY_TYPE_ID


class Criterion:
    """Criterion class"""

    def __init__(self, *, entity_type_id: int = None, name: str = None, min_age: float = None,
                 max_age: float = None, group_list_id: int = None, min_number_of_kids: int = None,
                 max_number_of_kids: int = None, min_kids_age: float = None, max_kids_age: float = None,
                 gender_list_id: int = None, min_height: int = None, max_height: int = None,
                 partner_experience_level: int = None, number_of_partners: int = None,
                 location_id: int = None, location_list_id: int = None, coordinate: str = None,
                 radius: int = None, radius_measure: str = None, radius_km: int = None,
                 job_group_list_id: int = None, job_location_list_id: int = None,
                 vacancy_list_id: int = None, workplace_profile_list_id: int = None,
                 start_date_type_id: int = None, job_types_id: int = None, visibility_id: int = None, where_sql: str = None,
                 is_test_data: bool = None, internet_domain_id: int = None,
                 internet_domain_list_id: int = None, organization_name: str = None, group_id: int = None,
                 profile_list_id: int = None, international_code: int = None, **kwargs) -> None:
        """Initialize a Criterion object."""
        for key, value in locals().items():
            if key not in ["self", "kwargs", "__class__"]:
                setattr(self, key, value)

        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> dict:
        """Convert the Criterion object to a dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __eq__(self, other: 'Criterion') -> bool:
        """Check if two Criterion objects are equal."""
        return self.to_dict() == other.to_dict()


class CriteriaLocal(GenericCRUD, metaclass=MetaLogger, object=LOGGER_CRITERIA_CODE_OBJECT):
    """CriteriaLocal class"""

    def __init__(self) -> None:
        """
        Initialize the CriteriaLocal object.

        This class inherits from GenericCRUD.

        :rtype: None
        """
        super().__init__(default_schema_name="criteria",
                         default_table_name="criteria_table",
                         default_view_table_name="criteria_view",
                         default_column_name="criteria_id")

    def insert(self, criterion: Criterion) -> int:
        """
        Insert a criterion into the database.
        criterion.entity_type_id is required.

        :param criterion: The criterion to insert.
        :type criterion: Criterion
        :rtype: None
        """
        criteria_dict = criterion.to_dict()
        criterion_id =  super().insert(data_dict=criteria_dict)
        return criterion_id

    def update(self, criteria_id: int, new_criterion: Criterion) -> None:
        """
        Update a criterion in the database.

        :param criteria_id: The ID of the criterion to update.
        :param new_criterion: The new criterion.
        :type criteria_id: int
        :type new_criterion: Criterion
        :rtype: None
        """
        criteria_dict = new_criterion.to_dict()
        super().update_by_column_and_value(column_value=criteria_id, data_dict=criteria_dict)

    def select_criterion_object(self, criteria_id: int) -> Criterion:
        """
        Select a criterion from the database.

        :param criteria_id: The ID of the criterion to select.
        :type criteria_id: int
        :rtype: Criterion
        """
        criterion = self.select_criterion_dict(criteria_id=criteria_id)
        criterion_object = Criterion(**criterion)
        return criterion_object

    def select_criterion_dict(self, criteria_id: int) -> dict:
        """
        Select a criterion from the database.

        :param criteria_id: The ID of the criterion to select.
        :type criteria_id: int
        :rtype: dict
        """
        criterion_dict=super().select_one_dict_by_column_and_value(column_value=criteria_id)
        return criterion_dict

    def delete(self, criteria_id: int) -> None:
        """
        Delete a criterion from the database.

        :param criteria_id: The ID of the criterion to delete.
        :type criteria_id: int
        :rtype: None
        """
        self.delete_by_column_and_value(column_value=criteria_id)

    def get_test_criteria_id(self, criterion: Criterion = None, **kwargs) -> int:
        if not criterion:
            criterion = Criterion(entity_type_id=PEOPLE_ENTITY_TYPE_ID, is_test_data=True, **kwargs)
        return super().get_test_entity_id(entity_name="criteria",
                                          insert_function=self.insert,
                                          insert_kwargs={"criterion": criterion})

    def get_entities_by_criterion(self, criterion: Criterion) -> list[dict]:
        where_sql = criterion.where_sql
        entity_id = criterion.entity_type_id
        # TODO: get the following dinamically using the entity_id
        if entity_id == PEOPLE_ENTITY_TYPE_ID:
            schema_name = "person"
            view_table_name = "person_view"
        else:
            self.logger.critical(f"entity_type_id {entity_id} is not supported")
            return []
        entities = self.select_multi_dict_by_where(schema_name=schema_name,
                                                   view_table_name=view_table_name,
                                                   where=where_sql)
        return entities

    def get_criterias_from_criteria_set_id(self, criteria_set_id: int) -> list[dict]:
        """Given parent_criteria_set_id, find its child_criteria_set_id which now becomes parent_criteria_set_id,
            and continue recursively until all child_criteria_set_id not found in parent_criteria_set_id.
            For each such leaf, return its critiria_id and entity_type_id"""
        select_clause_value = "parent_criteria_set_id, child_criteria_set_id, criteria_id, entity_type_id"
        all_rows = self.select_multi_dict_by_where(view_table_name="criteria_set_general_view",
                                                   select_clause_value=select_clause_value, where="TRUE")
        grouped_by_parent = {}
        for row in all_rows:
            parent_criteria_set_id = row["parent_criteria_set_id"]
            row.pop("parent_criteria_set_id")
            if parent_criteria_set_id not in grouped_by_parent:
                grouped_by_parent[parent_criteria_set_id] = []
            grouped_by_parent[parent_criteria_set_id].append(row)

        criteria_list = []
        def recursive_find_criteria_set(parent_criteria_set_id: int):
            for row in grouped_by_parent[parent_criteria_set_id]:
                if row["child_criteria_set_id"] in grouped_by_parent:
                    recursive_find_criteria_set(row["child_criteria_set_id"])
                else:  # leaf
                    criteria_list.append({"criteria_id": row["criteria_id"], "entity_type_id": row["entity_type_id"]})

        recursive_find_criteria_set(criteria_set_id)
        return criteria_list
