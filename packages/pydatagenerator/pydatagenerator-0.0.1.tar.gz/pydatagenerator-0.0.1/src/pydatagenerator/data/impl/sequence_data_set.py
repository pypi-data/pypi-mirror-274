from typing import Dict, List
from pydatagenerator.data.abstract import AbstractDataSet


class SequenceDataSet(AbstractDataSet):
    """SequenceDataSet
    """
    type = 'type.sequence-dataset'

    def required_fields(self) -> List[str]:
        """Returns the required fields for the current data set

        Returns:
            List[str]: List of required fields for the current data set
        """
        return ['start', 'increment']

    def optional_fields(self) -> List[str]:
        """Returns the optional fields for the current data set

        Returns:
            List[str]: List of optional fields for the current data set
        """
        return []

    def __init__(self, dataset_info: Dict[str, object]):
        super().__init__(dataset_info)
        self.__val = int(dataset_info['start']) - int(dataset_info['increment'])

    def handle(self) -> object:
        """Process the given dataset_info and returns a result out of it

        Returns:
            object: The result obtained after processing the dataset_info
        """
        self.validate_dataset_info()
        increment = int(self._dataset_info['increment'])
        self.__val += increment
        return self.__val
