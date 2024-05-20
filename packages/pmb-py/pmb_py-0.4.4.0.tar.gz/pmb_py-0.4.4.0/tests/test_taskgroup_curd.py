import pytest
import pmb_py


def test_taskgroup_create(pmb_login_logout):
    pmb_py.api.TaskGroups.create(project_id=5, name='task_group_test_01')
    tg = pmb_py.api.TaskGroups.list(
        project_id=5, name='task_group_test_01').first()
    assert(tg.name == 'task_group_test_01')

    re = pmb_py.api.TaskGroups.remove(tg.id)
    assert(re, 'delete task group fail')

    pmb_py.api.TaskGroups.create(
        project_id=5, name='task_group_test_02', cost=0, sort_num=122)
    tg = pmb_py.api.TaskGroups.list(name='task_group_test_02').first()
    assert(tg.name == 'task_group_test_02')

    re = pmb_py.api.TaskGroups.remove(tg.id)
    assert(re, 'delete task group fail')


def test_taskgroup_list(pmb_login_logout):
    re = pmb_py.api.TaskGroups.list(project_id=5)
    tasks = re.results
    assert(len(tasks) == 4)

    re = pmb_py.api.TaskGroups.list(project_id=5, name='Shotgun Tasks')
    tasks = list(re.results)[0]
    assert(tasks.name == 'Shotgun Tasks')

    re = pmb_py.api.TaskGroups.list(project_id=5, name='Shotgun Tasks')
    tasks = re.first()
    assert(tasks.name == 'Shotgun Tasks')
