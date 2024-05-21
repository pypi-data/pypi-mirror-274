from datetime import date, datetime
from pmb_py.spec import TIME_FORMAT1, PmbGantt


# def test_blocks_between_date(pmb_login_logout):
#     start_date=datetime.strptime('2021-05-01', TIME_FORMAT1)
#     end_date=datetime.strptime('2021-11-01', TIME_FORMAT1)
#     pagenation_re = PmbGantt.blcoks_between_date(start_date.date(), end_date.date())
#     params = pagenation_re.query_params()
#     for block in pagenation_re.results:
#         assert block.date.year == 2021
#         assert block.date.month in [5,6,7,8,9,10,11]

