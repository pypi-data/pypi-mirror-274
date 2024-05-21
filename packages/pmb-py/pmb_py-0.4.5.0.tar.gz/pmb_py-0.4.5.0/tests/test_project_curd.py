import pytest
import pmb_py


def test_project_list(pmb_login_logout):
    projects = pmb_py.api.Projects.list()
    print(projects)
    assert(projects)


def test_project_get(pmb_login_logout):
    projects = pmb_py.api.Projects.get(2)
    assert(projects)
    with pytest.raises(pmb_py.PmbError) as execinfo:
        pmb_py.api.Projects.get(500000)


def test_project_update(pmb_login_logout):
    project = pmb_py.api.Projects.get(2)
    old_shotgun_id = project.sg_project_id
    project = pmb_py.api.Projects.update(2, sg_project_id=97)
    assert project.sg_project_id == 97
    project = pmb_py.api.Projects.update(2, sg_project_id=old_shotgun_id)
    assert project.sg_project_id == old_shotgun_id
