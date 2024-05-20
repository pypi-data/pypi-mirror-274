import pytest
import pmb_py


def test_task_list(pmb_login_logout):
    tasks = pmb_py.api.Tasks.list(project_id=2)
    assert(len(tasks.results) == 3)

    # with pytest.raises(pmb_py.PmbError) as execinfo :
    #     pmb_py.api.Tasks.list(project_id=[3,4], task_id=2)
    pmb_py.api.Tasks.list(project_id=[3, 4], task_id=2)
    print('test')


def test_task_list_2(pmb_login_logout):
    task = pmb_py.api.Tasks.list(member_id=60, gantt_item_id=1936).first()
    assert(task)


def test_task_create_update_remove(pmb_login_logout):
    task = pmb_py.api.Tasks.create(
        name='task_create_1', project_id=5, task_group_id=5343)
    assert(task)

    task = pmb_py.api.Tasks.update(
        task.id, name='task_updated', member_id=20, gantt_item_id=1)
    assert(task.name == "task_updated")


def test_gantt_task(pmb_login_logout):
    re = pmb_py.api.GanttTasks.list(project_id=2)
    assert(len(re.results) == 3)

    gtask = pmb_py.api.GanttTasks.list(id=4).first()
    assert(gtask.id == 4)
