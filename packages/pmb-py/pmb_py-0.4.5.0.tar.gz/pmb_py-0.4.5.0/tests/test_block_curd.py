import datetime
import pytest
import pmb_py


def test_block_list(pmb_login_logout):
    blcoks = pmb_py.api.Blocks.list(project_id=2).results
    assert(len(blcoks)==33)

    # with pytest.raises(pmb_py.PmbError) as execinfo :
    #     pmb_py.api.Blocks.list(project_id=[3,4], task_id=2)


def test_block_list2(pmb_login_logout):
    re = pmb_py.api.Blocks.list(task_id=3)
    blocks = re.results
    assert(len(blocks) == 17)


def test_block_list3(pmb_login_logout):
    re = pmb_py.api.Blocks.list(project_id=937)
    # 937 是 智崴_一帶一路2020，有 4207 個 block
    for block in re.results:
        assert(block.project_id == 937)
        assert(type(block.date)==datetime.date)
    # assert(re.total_count == 4207)
    assert(re.next_start() == 1001)


def test_block_list4(pmb_login_logout):
    re = pmb_py.api.Blocks.list(project_id=5, member_id=22)
    assert(len(re.results) == 2)


def test_block_list5(pmb_login_logout):
    re = pmb_py.api.Blocks.list(project_id=1288, group_id=5013)
    for item in re.results:
        assert(item.project_id==1288)
        assert(item.group_id==5013)


def test_block_list6(pmb_login_logout):
    '''測試 session, 在同一次 test 呼叫二次'''
    blcoks = pmb_py.api.Blocks.list(project_id=2).results
    assert(len(blcoks)==33)

    re = pmb_py.api.Blocks.list(project_id=1288, group_id=5013)
    for item in re.results:
        assert(item.project_id==1288)
        assert(item.group_id==5013)