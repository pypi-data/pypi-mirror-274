import abc
import sys
from typing import Dict, List


class DataSetConstants:
    """DataSetConstants
    """
    DEFAULT_REQUIRED_FIELDS = ['name', 'type']


class AbstractDataSet(abc.ABC):
    """AbstractDataSet
    """
    type = 'type.abstract-dataset'

    def __init__(self, dataset_info: Dict[str, object]):
        """Creates a new data set
        """
        self._dataset_info = dataset_info

    @property
    def dataset_info(self) -> Dict[str, object]:
        """Dataset info getter

        Returns:
            Dict[str, object]: The dataset_info value
        """
        return self._dataset_info

    @dataset_info.setter
    def dataset_info(self, value: Dict[str, object]):
        """Dataset info setter

        Args:
            value (Dict[str, object]): The dataset_info value
        """
        self._dataset_info = value

    @dataset_info.deleter
    def dataset_info(self) -> None:
        """Dataset info deleter
        """
        del self._dataset_info

    def validate_default_required_fields(self) -> None:
        """Validates the default required fields (name and type)
        """
        fields = list(self._dataset_info.keys())
        fields_set = set(fields)

        for field in DataSetConstants.DEFAULT_REQUIRED_FIELDS:
            if field not in fields_set:
                sys.stderr.write(f'Error: Missing required property {field}')
                sys.exit(-1)

    def validate_required_fields(self) -> None:
        """Validates the required fields
        """
        fields = list(self._dataset_info.keys())
        fields_set = set(fields)
        req_fields = self.required_fields()
        for field in req_fields:
            if field not in fields_set:
                sys.stderr.write(f'Error: Missing property {field} \n')
                sys.exit(-1)

    def validate_optional_fields(self) -> None:
        """Validates the optional fields
        """
        fields = list(self._dataset_info.keys())
        req_fields = set(DataSetConstants.DEFAULT_REQUIRED_FIELDS + self.required_fields())
        fields_set = set([field for field in fields if field not in req_fields])
        optional_fields = set(self.optional_fields())

        diff = fields_set - optional_fields

        if len(diff) > 0:
            sys.stderr.write(f'Error: Unknown properties {diff} \n')
            sys.exit(-1)

    def validate_dataset_info(self) -> None:
        """Validates the dataset info
        """
        self.validate_default_required_fields()
        if self.type == self._dataset_info['type']:
            self.validate_required_fields()
            self.validate_optional_fields()

    @abc.abstractmethod
    def required_fields(self) -> List[str]:
        """Returns the required fields for the current data set

        Returns:
            List[str]: List of required fields for the current data set
        """
        return []

    @abc.abstractmethod
    def optional_fields(self) -> List[str]:
        """Returns the optional fields for the current data set

        Returns:
            List[str]: List of optional fields for the current data set
        """
        return []

    @abc.abstractmethod
    def handle(self) -> object:
        """Process the given dataset_info and returns a result out of it

        Returns:
            object: The result obtained after processing the dataset_info
        """
        return
