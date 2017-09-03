import pytest
from snakeskin.models.tenant import Tenant

@pytest.fixture
def fixture_tenants(app, db_session):

    ucb = Tenant(name='UC Berkeley', scheme='https', domain='bcourses.berkeley.edu', token='secret')
    ucoe = Tenant(name='UC Online Education', scheme='https', domain='cole2.uconline.edu', token='secret')

    db_session.add(ucb)
    db_session.add(ucoe)
    db_session.commit()

    return [ucb, ucoe]
