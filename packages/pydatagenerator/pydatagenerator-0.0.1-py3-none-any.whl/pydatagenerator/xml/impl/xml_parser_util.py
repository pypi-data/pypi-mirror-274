import lxml
from typing import Dict

class XmlParserUtil(object):
    def collect_attributes(node: lxml.etree._Element) -> Dict[str, object]:
        """Collect lxml node attributes

        Args:
            node (lxml.etree._Element): The lxml to extract the node attributes from

        Returns:
            Dict[str, object]: The attributes dictionary collected from the node attributes
        """
        res = {}
        for item in node.attrib.items():
            key, res[key] = item
        return res