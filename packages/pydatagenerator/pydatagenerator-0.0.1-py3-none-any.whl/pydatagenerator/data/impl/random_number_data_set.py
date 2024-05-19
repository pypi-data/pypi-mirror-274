import random
from pydatagenerator.data.abstract import AbstractDataSet


class RandomNumberDataSet(AbstractDataSet):
    """RandomNumberDataSet
    """
    type = 'type.random-number-dataset'

    def required_fields(self):
        """Returns the required fields for the current data set

        Returns:
            List[str]: List of required fields for the current data set
        """
        return ['min', 'max']

    def optional_fields(self):
        """Returns the optional fields for the current data set

        Returns:
            List[str]: List of optional fields for the current data set
        """
        return ['floating']

    def handle(self) -> object:
        """Process the given dataset_info and returns a result out of it

        Returns:
            object: The result obtained after processing the dataset_info
        """
        self.validate_dataset_info()
        is_floating = self._dataset_info['floating'] and self._dataset_info['floating'].lower() == 'true'
        func = random.uniform if is_floating else random.randint
        return func(int(self._dataset_info['min']), int(self._dataset_info['max']))
