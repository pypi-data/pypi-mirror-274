import pytest
import pmb_py


def test_gantt_item_create_update_delete(pmb_login_logout):
    obj = pmb_py.api.GanttItems.create(name='test1')
    assert type(obj) == pmb_py.domain.model.GanttItem
    # create

    the_gantt_item = pmb_py.api.GanttItems.get(obj.id)
    the_gantt_item = pmb_py.api.GanttItems.update(
        the_gantt_item.id, legend='test update')
    assert the_gantt_item.legend == 'test update'
    assert obj.id == the_gantt_item.id
    # update

    pmb_py.api.GanttItems.remove(obj.id)
    gantt_items = pmb_py.api.GanttItems.list(id=obj.id).first()
    assert gantt_items is None
    with pytest.raises(pmb_py.PmbError) as execinfo:
        # should raise error because get nothing
        pmb_py.api.GanttItems.get(obj.id)
    # delete


def test_gantt_item_list(pmb_login_logout):
    gantt_items = pmb_py.api.GanttItems.list(project_id=1005).results
    assert(gantt_items)
    for gitem in gantt_items:
        assert(gitem.project_id == 1005)
