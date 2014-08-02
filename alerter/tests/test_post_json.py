import json
import os
import unittest
import mock

from os.path import dirname, join as pjoin

from nose.tools import assert_equal

from ..alerter import APP


class AlerterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = APP.test_client()
        self.post_url = '/cloudmailin/'

        with open(pjoin(dirname(__file__), 'sample_post.json')) as f:
            self.sample_json = f.read()

    def test_status_endpoint_returns_http_200_ok(self):
        response = self.app.get('/_status/')
        assert_equal(200, response.status_code)
        assert_equal(
            {'message': 'All systems go.'},
            json.loads(response.data))

    def test_post_json_no_match(self):
        os.environ['SEARCH_KEYWORDS'] = 'not-a-matching-keyword'
        response = self.app.post(
            self.post_url,
            data=self.sample_json,
            content_type='application/json')
        assert_equal(200, response.status_code)
        assert_equal(
            {'message': 'OK, email did not match search.'},
            json.loads(response.data))

    def test_post_json_with_match(self):
        os.environ['SEARCH_KEYWORDS'] = 'Test'
        with mock.patch('alerter.alerter.send_text_alert') as send_text_alert:
            response = self.app.post(
                self.post_url,
                data=self.sample_json,
                content_type='application/json')
            assert_equal(200, response.status_code)
            assert_equal(
                {'message': 'SMS sent'},
                json.loads(response.data))
            send_text_alert.assert_called_once_with('Test', 'Test Subject')

    def test_bad_json_returns_400(self):
        response = self.app.post(
            self.post_url,
            data='malformed json',
            content_type='application/json')
        assert_equal(400, response.status_code)
