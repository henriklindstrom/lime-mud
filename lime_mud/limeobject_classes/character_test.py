import lime_config
import lime_plugins
import pytest
from unittest.mock import call, create_autospec


def test_sets_name_property(
        loaded_plugins, limeapp, tester_person):

    uow = limeapp.unit_of_work()
    tester_person.properties.lastname.value = 'Mc Testy'
    tester_idx = uow.add(tester_person)
    res = uow.commit()
    updated_person = res.get(tester_idx)

    assert updated_person.properties.name.value == 'Tester Mc Testy'


def test_sends_event_when_person_renamed(
        loaded_plugins, limeapp, tester_person):

    limeapp.publish = create_autospec(limeapp.publish)

    uow = limeapp.unit_of_work()
    tester_person.properties.lastname.value = 'Mc Testy'
    uow.add(tester_person)
    uow.commit()

    limeapp.publish.assert_has_calls([call('custom.person.renamed', {
        'old_name': 'Tester Testsson',
        'new_name': 'Tester Mc Testy'})])


@pytest.fixture
def tester_person(limeapp):
    """A person that gets added to `limeapp`"""
    uow = limeapp.unit_of_work()
    tester = limeapp.limetypes.person(firstname='Tester', lastname='Testsson')
    tester_idx = uow.add(tester)
    res = uow.commit()
    return res.get(tester_idx)


@pytest.fixture
def loaded_plugins(no_registered_limeobjects):
    return lime_plugins.load_plugins(config=lime_config.config)
