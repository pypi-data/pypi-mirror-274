import pytest
import pmb_py
from pmb_py.domain.model import ProjectType, ProjectStatus


def test_project_type_list(pmb_login_logout):
    items = pmb_py.api.ProjectType.list().results
    assert(items)
    for item in items:
        assert(type(item) == ProjectType)


def test_project_status_list(pmb_login_logout):
    items = pmb_py.api.ProjectStatus.list().results
    assert(items)
    for item in items:
        assert(type(item) == ProjectStatus)
