import pytest
from pydatagenerator.data.impl.dataset_handler_factory import DatasetHandlerFactory


def test_generate_random_integer_number():
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-number-dataset',
        'name': 'random_data_set',
        'min': '10',
        'max': '20',
        'floating': 'false'
    })

    value = handler.handle()
    assert value is not None
    assert 10 <= value <= 20


def test_generate_random_floating_number():
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-number-dataset',
        'name': 'random_data_set',
        'min': '10',
        'max': '20',
        'floating': 'true'
    })

    value = handler.handle()

    assert value is not None
    assert 10.0 <= value <= 20.0


def test_validate_dataset_info_missing_default_required_properties():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        handler = DatasetHandlerFactory().get_dataset_handler({
            'name': 'random_data_set',
            'min': '10',
            'max': '20',
            'floating': 'true'
        })
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == -1

    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-number-dataset',
        'min': '10',
        'max': '20',
        'floating': 'true'
    })

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        value = handler.handle()
        assert value is None
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == -1


def test_validate_dataset_info_missing_random_number_required_property():
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-number-dataset',
        'name': 'random_data_set',
        'max': '20',
        'floating': 'true'
    })

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        value = handler.handle()
        assert value is None
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == -1

    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-number-dataset',
        'name': 'random_data_set',
        'min': '10',
        'floating': 'true'
    })

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        value = handler.handle()
        assert value is None
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == -1


def test_not_matching_dataset_type():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        handler = DatasetHandlerFactory().get_dataset_handler({
            'type': 'type.not-existing-type',
            'name': 'not-existing-type'
        })
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == -1



def test_unknown_random_number_property():
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.random-number-dataset',
        'name': 'random_data_set',
        'random': '10',
        'floating': 'true'
    })

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        value = handler.handle()
        assert value is None
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == -1
