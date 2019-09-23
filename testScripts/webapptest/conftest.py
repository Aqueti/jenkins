import os
import pytest


def pytest_sessionstart(session):
    session.results = dict()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result

def pytest_addoption(parser):
    parser.addoption("--project", action="store", default="acos")
    parser.addoption("--branch", action="store", default="dev")
    parser.addoption("--build", action="store", default="1")

#def pytest_generate_tests(metafunc):
#    option_value = metafunc.config.option.project
#    if 'project' in metafunc.fixturenames and option_value is not None:
#        metafunc.parametrize("project", [option_value])
