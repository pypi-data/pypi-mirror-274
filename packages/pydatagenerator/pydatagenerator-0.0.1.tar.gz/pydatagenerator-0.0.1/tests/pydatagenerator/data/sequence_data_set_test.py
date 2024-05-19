from pydatagenerator.data.impl.dataset_handler_factory import DatasetHandlerFactory


def test_generate_sequence_data():
    handler = DatasetHandlerFactory().get_dataset_handler({
        'type': 'type.sequence-dataset',
        'name': 'count',
        'start': 0,
        'increment': 5
    })

    value = handler.handle()
    assert value is not None
    assert value == 0

    value = handler.handle()
    assert value is not None
    assert value == 5
