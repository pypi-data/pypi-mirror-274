import abc
from typing import List

class AbstractXmlParser(abc.ABC):
    """XML parser contract
    """

    @abc.abstractmethod
    def parse_xml_from_string(self, xml_str: str) -> List[str]:
        """Parse xml from string

        Args:
            xml_str (str): The xml specification for generating data

        Returns:
            List[str]: List of resulted values after processing the xml_str
        """
        return

    @abc.abstractmethod
    def parse_xml_from_file(self, xml_file: str) -> List[str]:
        """Parse xml from file

        Args:
            xml_file (str): The path to the xml file containing the xml specification for generating data

        Returns:
            List[str]: List of resulted values after processing the xml_str
        """
        return