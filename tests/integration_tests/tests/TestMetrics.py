from tests.utils import *


class TestMetrics(unittest.TestCase):

    @call_api(endpoint=KONG_METRICS + '/metrics', parse_json=False)
    def test_metrics(self, status, body):
        self.assertEqual(OK, status)
        self.assertTrue('kong_plugin_jwt_keycloak_duration_seconds' in body)
        self.assertTrue('kong_plugin_jwt_keycloak_requests' in body)

        metrics = {}
        for l in body.split('\n'):
            l = l.strip()
            if l.startswith('#') or not l:
                continue
            [k, v] = l.split()
            metrics[k] = v
        access_count = metrics['kong_plugin_jwt_keycloak_duration_seconds_count{method="access"}']
        auth_count = metrics['kong_plugin_jwt_keycloak_duration_seconds_count{method="do_authentication"}']

        # Ensure that we didn't under-count the number of requests
        self.assertGreaterEqual(access_count, auth_count)
