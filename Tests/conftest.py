import os
import pytest
import glob
from Library.store import Store


@pytest.fixture(autouse=True)
def before_each():
    print('*-* Before each INITIALIZATION')
    try:
        yield
        # After each test case taking screen shots form the available drivers
    except Exception as e:
        print(e)
    print('*-* After each END')


@pytest.fixture(scope='module', autouse=True)
def before_module():
    print('*-* Before module INITIALIZATION')
    yield
    # after each module ensuring the browsers are closed
    print('*-* After module END')


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    print("*-* pytest_configure" + config)
    # Configuring the selpy with data path location
    Store.global_data_path = os.path.dirname(
        os.path.abspath(__file__)).replace("/Tests", "") + '/Data/GlobalData/global_data.yml'
    Store.static_data_path = os.path.dirname(os.path.abspath(__file__)).replace("/Tests", "") + '/Data/TestData/'
    Store.dynamic_data_path = os.path.dirname(os.path.abspath(__file__)).replace("/Tests", "") + '/Data/DynamicData/'
    root_dir = os.path.dirname(os.path.abspath(__file__)).replace("/Tests", "")
    # Clearing the old screenshots from the location.
    config_path = root_dir + '/reports/images/*.png'
    for CleanUp in glob.glob(config_path):
        print(CleanUp)
        os.remove(CleanUp)


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    print("*-* pytest_sessionstart" + session)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    print("*-* pytest_sessionfinish" + session + exitstatus)


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    print("*-* pytest_unconfigure" + config)
