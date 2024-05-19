import re
import sys
from lxml import etree
from pydatagenerator.data.impl import DatasetHandlerFactory
from pydatagenerator.xml.abstract import AbstractXmlParser
from pydatagenerator.xml.impl.xml_parser_util import XmlParserUtil
from typing import Dict, List


class XmlParser(AbstractXmlParser):
    """XML Parser Implementation
    """

    @staticmethod
    def parse_template(template_content: str, data_info: Dict[str, object], iterations: int) -> List[str]:
        """Parse template

        Args:
            template_content (str): The template tag's content
            data_info (Dict[str, object]): The data info containing the actual values for the template_content's variables
            iterations (int): The number of iterations

        Returns:
            List[str]: List of values after replacing the template_content's variables with the data_info values for each iteration
        """
        regex = re.compile(r'(?:^|(?<=[^#]))#{\w+}')
        iterators = {k: iter(v) for k, v in data_info.items()}

        def subst(match_obj):
            key = match_obj.group(0)
            # Remove unnecessary characters from key
            for c in ['{', '#', '}']:
                key = key.replace(c, '')
            return str(next(iterators[key]))

        return [regex.sub(subst, template_content) for _ in range(iterations)]

    def parse_xml_from_string(self, xml_str: str) -> List[str]:
        """Parse xml from string

        Args:
            xml_str (str): The xml specification for generating data

        Returns:
            List[str]: List of resulted values after processing the xml_str
        """
        root = etree.fromstring(xml_str)
        generator = root.xpath('//pydatagenerator')[0]
        datasets = generator.xpath('//dataset')
        iterations = generator.get('iterations')
        handler_factory = DatasetHandlerFactory()
        data_info = {}

        if not iterations:
            sys.stderr.write('Error: No iterations property found for pydatagenerator tag')
            sys.exit(-1)
        else:
            iterations = int(iterations)

        for _ in range(iterations):
            for dataset in datasets:
                dataset_info = XmlParserUtil.collect_attributes(dataset)
                dataset_handler = handler_factory.get_dataset_handler(dataset_info)
                name = dataset_info['name']
                if name in data_info:
                    data_info[name].append(dataset_handler.handle())
                else:
                    data_info[name] = [dataset_handler.handle()]

        templates = generator.xpath('//template')
        template = templates[0] if templates else None

        if template is None:
            sys.stderr.write('Error: No <template> found')
            sys.exit(-1)

        template_content = ''.join(template.itertext()).strip()

        return XmlParser.parse_template(template_content, data_info, iterations)

    def parse_xml_from_file(self, xml_file: str) -> List[str]:
        """Parse xml from file

        Args:
            xml_file (str): The path to the xml file containing the xml specification for generating data

        Returns:
            List[str]: List of resulted values after processing the xml_str
        """
        with open(xml_file) as f:
            xml = f.read()
            return self.parse_xml_from_string(xml)
