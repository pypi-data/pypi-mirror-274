import pmb_py


def test_member_list(pmb_login_logout):
    re = pmb_py.api.Members.list()
    for member in re.results:
        assert(member.id is not None)
        assert(member.emp_id is not None)
        assert(member.name is not None)


def test_member_list_first(pmb_login_logout):
    re = pmb_py.api.Members.list(eid=20150907).first()
    assert(re.emp_id == '20150907')
