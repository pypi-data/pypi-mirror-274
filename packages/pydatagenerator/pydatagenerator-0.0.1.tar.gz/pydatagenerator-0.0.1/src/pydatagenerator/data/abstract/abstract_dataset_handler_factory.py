import abc
from pydatagenerator.data.abstract import AbstractDataSet
from typing import Dict


class AbstractDataSetHandler(abc.ABC):
    """Dataset handler contract
    """

    @abc.abstractmethod
    def get_dataset_handler(self, dataset_info: Dict[str, object]) -> AbstractDataSet:
        """Get dataset handler

        Args:
            dataset_info (Dict[str, object]): The dataset info to construct the dataset handler for

        Returns:
            AbstractDataSet: The data set handler constructed from the dataset_info
        """
        return
