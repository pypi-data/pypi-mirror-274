import sys
from pydatagenerator.data.abstract import AbstractDataSet, AbstractDataSetHandler
from typing import Dict


class DatasetHandlerFactory(AbstractDataSetHandler):
    """Dataset handler factory
    """

    def get_dataset_handler(self, dataset_info: Dict[str, object]) -> AbstractDataSet:
        """Get dataset handler

        Args:
            dataset_info (Dict[str, object]): The dataset info to construct the dataset handler for

        Returns:
            AbstractDataSet: The data set handler constructed from the dataset_info
        """
        type = dataset_info.get('type')
        if not type:
            sys.stderr.write('Error: No value provided for type')
            sys.exit(-1)
        handler = self.__classes.get(dataset_info['type'])
        if not handler:
            sys.stderr.write(f'Error: Unknown type {dataset_info['type']}')
            sys.exit(-1)
        return handler(dataset_info)

    def __init__(self):
        self.__classes = {c.type: c for c in AbstractDataSet.__subclasses__()}
