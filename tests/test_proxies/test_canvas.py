import pytest

import snakeskin.lib.mockingbird as mockingbird
import snakeskin.proxies.canvas as canvas


@pytest.fixture
def ucb_canvas(fixture_tenants):
    return fixture_tenants[0]


class TestCanvasGetUserForSisId:
    '''Canvas API query (user for SIS ID)'''

    def test_user_for_sis_id(self, ucb_canvas):
        '''returns fixture data'''
        oliver_response = canvas.get_user_for_sis_id(ucb_canvas, 2040)
        assert oliver_response.status_code == 200
        assert oliver_response.json()['sortable_name'] == 'Heyer, Oliver'
        assert oliver_response.json()['avatar_url'] == 'https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Donald_Duck.svg/618px-Donald_Duck.svg.png'

        paul_response = canvas.get_user_for_sis_id(ucb_canvas, 242881)
        assert paul_response.status_code == 200
        assert paul_response.json()['sortable_name'] == 'Kerschen, Paul'
        assert paul_response.json()['avatar_url'] == 'https://en.wikipedia.org/wiki/Daffy_Duck#/media/File:Daffy_Duck.svg'

    def test_user_not_found(self, ucb_canvas, caplog):
        '''logs 404 for unknown user and returns empty response'''
        response = canvas.get_user_for_sis_id(ucb_canvas, 9999999)
        assert 'HTTP/1.1" 404' in caplog.text
        assert not response

    def test_server_error(self, ucb_canvas, caplog):
        '''logs unexpected server errors and returns empty response'''
        with mockingbird.register(canvas.get_user_for_sis_id, 500, {}, '{"message": "Internal server error."}'):
            response = canvas.get_user_for_sis_id(ucb_canvas, 2040)
            assert 'HTTP/1.1" 500' in caplog.text
            assert not response
