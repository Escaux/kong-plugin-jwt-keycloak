import requests

# This way how to import is really a hacky bad way, but i hat not found a way
# to have the variables really as global variable available in all modules
# I am not python developer ... it think this is now visible without any doubt ...
# Help how to rework it .... in the good way ... really would be welcome
import tests.config
from tests.config import *

from requests_toolbelt.utils import dump

# helper functions
def logging_hook(logtext, *args, **kwargs):
    data = dump.dump_all(logtext)
    print(data.decode('utf-8'))

def keyclock_adjust_accessTokenLifespan(seconds):
    # Set token-setting to issue tokens with different valid time periods
    r = requests.put(KC_HOST + "/admin/realms/master", 
                 headers={'authorization': 'Bearer ' + KC_ADMIN_TOKEN, 'content-type': "application/json"}, 
                 json={'accessTokenLifespan': str(seconds)})
    assert r.status_code == 204

def get_kc_admin_token():
    r = requests.post(KC_REALM + "/protocol/openid-connect/token", data={
        'grant_type': 'password',
        'client_id': 'admin-cli',
        'username': KC_USER,
        'password': KC_PASS
    })
    assert r.status_code == 200
    return r.json()['access_token']

############################################################################
# Now initialize the required testdata
#
# Set token-setting to issue tokens for only 1 second valid for user-tokens to be able to request
# at the beginning a token which is issued by current keycloak  instance .. but directly will be expired
# when it is used in test-cases
if not setup_done:
    # Request directly token with these settings
    if KC_ADMIN_TOKEN is None:
        # Get the token so we can change the lifespan
        KC_ADMIN_TOKEN = get_kc_admin_token()
        # ... Then change the lifespan to 1h because the default is 60 seconds and on slow machines
        # the tests fail because of this!!
        # You don't have any idea how CRAZY I became trying to debug semi-random 401 errors.
        keyclock_adjust_accessTokenLifespan(3600)
        KC_ADMIN_TOKEN = get_kc_admin_token()
    else:
        print("-------------- already existing KC_ADMIN_TOKEN -------------------")

    # Not set keycloak to issue only 1 second valid tokens
    keyclock_adjust_accessTokenLifespan(1)
    r = requests.post(KC_REALM + "/protocol/openid-connect/token", data={
        'grant_type': 'password',
        'client_id': 'admin-cli',
        'username': KC_USER,
        'password': KC_PASS
    })
    if TD_TOKEN_EXPIRED is None:
        TD_TOKEN_EXPIRED = r.json()['access_token']
    else:
        print("-------------- already existing TD_TOKEN_EXPIRED -------------------")
    setup_done = True

# Change keycloak back to issue tokens 20 minutes valid
if setup_done:
    keyclock_adjust_accessTokenLifespan(1200)

# And now ask Keycloak about the running version information
r = requests.get(KC_HOST + '/admin/serverinfo', headers={'Authorization': 'Bearer ' + KC_ADMIN_TOKEN})
assert r.status_code == 200
KC_VERSION = r.json()['systemInfo']['version']
