from allabolag.liquidated_companies import iter_liquidated_companies
from datetime import datetime, timedelta

def test_iter_liquidated_companies():
    since = datetime.now() - timedelta(days=5)
    companies = [x for x in iter_liquidated_companies(since)]
    assert len(companies) > 0