from pydatagenerator.xml.impl import XmlParser


def test_xml_parser_random_numbers():
    parser = XmlParser()
    tags_str = '''
    <pydatagenerator iterations="20">
        <dataset name="age" type="type.random-number-dataset" floating="false" min="1" max="100"/>
        <dataset name="wage" type="type.random-number-dataset" floating="false" min="1000" max="100000000"/>
        <template>
            INSERT INTO Employees VALUES (#{age}, #{wage})
        </template>
    </pydatagenerator>
    '''
    values = parser.parse_xml_from_string(tags_str)
    assert isinstance(values, list)
    assert len(values) == 20

def test_xml_parser_sequence_data():
    parser = XmlParser()
    tags_str = '''
    <pydatagenerator iterations="20">
        <dataset name="id" type="type.sequence-dataset" start="0" increment="1"/>
        <dataset name="sum" type="type.sequence-dataset" start="10" increment="100"/>
        <template>
            INSERT INTO Sums VALUES (#{id}, #{sum})
        </template>
    </pydatagenerator>
    '''
    values = parser.parse_xml_from_string(tags_str)
    assert isinstance(values, list)
    assert len(values) == 20


def test_xml_parser_sequence_data_and_random_numbers():
    parser = XmlParser()
    tags_str = '''
    <pydatagenerator iterations="20">
        <dataset name="id" type="type.sequence-dataset" start="0" increment="1"/>
        <dataset name="wage" type="type.random-number-dataset" floating="false" min="1000" max="100000000"/>
        <template>
            INSERT INTO Salaries VALUES (#{id}, #{wage})
        </template>
    </pydatagenerator>
    '''
    values = parser.parse_xml_from_string(tags_str)
    assert isinstance(values, list)
    assert len(values) == 20
