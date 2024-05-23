from tests.utils import *


# Tokendetails: "iss": "http://keycloak:8080/auth/realms/master", "alg": "RS256" --> Already expired !!
# curl --connect-to keycloak:8080:localhost:8080 -X POST http://keycloak:8080/auth/realms/master/protocol/openid-connect/token --data-urlencode grant_type=client_credentials --data-urlencode client_id=<client id> --data-urlencode client_secret=<client secret>
STANDARD_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJVeXZ6LXZTRzN3SU9hLWFick50RFVtd0c1SElpY0lsMjJxMG4tSTRQQk13In0.eyJleHAiOjE3MTU3MDAxNTMsImlhdCI6MTcxNTY5ODk1MywianRpIjoiZGFlMjI3MTEtNGFhZi00MWY1LThhZjMtMzAxZDhmNDdlMzAzIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrOjgwODAvYXV0aC9yZWFsbXMvbWFzdGVyIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjAwMTA3Njg2LWI2NTEtNDg3YS04ZmE0LTQ2NWY2NzI2MWUxOCIsInR5cCI6IkJlYXJlciIsImF6cCI6IjAzZmRkMTQwLTU0ZGEtNGY1Ny05NTY5LWJlMjE5MmM2YTJkMiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1tYXN0ZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJlbWFpbCBwcm9maWxlIiwiY2xpZW50SG9zdCI6IjE3Mi4yMi4wLjEiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImNsaWVudElkIjoiMDNmZGQxNDAtNTRkYS00ZjU3LTk1NjktYmUyMTkyYzZhMmQyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LTAzZmRkMTQwLTU0ZGEtNGY1Ny05NTY5LWJlMjE5MmM2YTJkMiIsImNsaWVudEFkZHJlc3MiOiIxNzIuMjIuMC4xIn0.hKSg6WH3z9QA_QCyLThL8wymqAeDuzdp8Ss8gvfvhG30Ts4nvfkuIxxN0Gz3AGxhGTyDiXYoi8Gxo5tZ-PwyYEU2sVNPxXKsG2wbltZxGEg-VsMLfSErOIgOsryccGHDj8ZOlDRP4Qp1yOG52ukks9BUpX8RawEgii1xDwI_f0opOjOKYoyr125zhNhkaJyflLUh2lBIIs7-RFn27I4OlhcL8MmcrBLBuN50K68JIonucBpwVH4krf2YvVPLqsnmuqVihfnWhVIukeTMVpqQNBkm7lxViP-VUYN8Oz5D72aOrkGlRaz_xdKZoyOAamfGOa2Acmu3JqW17e4_FxKp4A'
# Tokendetails: "iss": "http://keycloak:8080/auth/realms/master", "alg": "RS256",
# override realm -> tokens "SSO Session max" and "Access Token lifespan" to 3650 Days
# curl --connect-to keycloak:8080:localhost:8080 -X POST http://keycloak:8080/auth/realms/master/protocol/openid-connect/token --data-urlencode grant_type=client_credentials --data-urlencode client_id=<client id> --data-urlencode client_secret=<client secret>
# last char replaced with '!' to make the base64 encoding invalid
BAD_SIGNATURE = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJxQ181TWtuRzVPZXFtQTdJMXU2Qk9uT2ZieUNtcVotX3JWQUJ4RFRBaFZJIn0.eyJleHAiOjE3MTY0ODMzOTQsImlhdCI6MTcxNjQ4MjE5NCwianRpIjoiZTY1YTY5YTctYzZhMC00NzYzLWJjZjQtYjAzMTI3NzM2Y2Q5IiwiaXNzIjoiaHR0cDovL2tleWNsb2FrOjgwODAvYXV0aC9yZWFsbXMvbWFzdGVyIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjNmMmQzYzk3LTNhYmUtNDBiZS1hOWNjLTM3ZGJiYTMxOGQ2ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6IjAwMDEyNzM3LTY3OTYtNDIxYy04OWY5LWNlZmVjN2RmNjBkNCIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1tYXN0ZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJlbWFpbCBwcm9maWxlIiwiY2xpZW50SWQiOiIwMDAxMjczNy02Nzk2LTQyMWMtODlmOS1jZWZlYzdkZjYwZDQiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImNsaWVudEhvc3QiOiIxNzIuMjYuMC4xIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LTAwMDEyNzM3LTY3OTYtNDIxYy04OWY5LWNlZmVjN2RmNjBkNCIsImNsaWVudEFkZHJlc3MiOiIxNzIuMjYuMC4xIn0.SA8xD2SzwzMAA60kpvw-0eU-3BvrxgL_cHDLgCGeGCNvaefUMRloATbDhdtBfZr-8aIDIFPRt5oG1c-_4ilbaaDpnpNo_m36ySV8Xb3uRjwyMGep9N27TSWuN00IdVkSxTOG3w3Wzekv8FTn2cbbvPx7Q2yD1i9pO9KMHksMxc8hTeN_2ygfqgXm80s38Npi1rFhEcTr-QlhZHKUDbdazLJtZTpgUeqHWqywsueDFyWs3dcBv3mhCbhdW9GqNkZpY5M8Zc4-xVKd_iz0adMtwS9jYFtYEgyc5kG9k736wyuoBrODo8ZuFWpKXkCFIOEHFTMHCEGcaYR0rds4z4eWu!'

class TestBasics(unittest.TestCase):

    ############################################################################
    # Test if plugin denies requests if completely no token is send to the 
    # kong instance .. it needs to fail
    @create_api({
        'allowed_iss': ['http://keycloak:8080/auth/realms/master']
    })
    @call_api()
    def test_no_auth(self, status, body):
        self.assertEqual(UNAUTHORIZED, status)
        self.assertEqual('Unauthorized', body.get('message'))

    ############################################################################
    # Test if plugin allows preflight access without token when configured 
    # ... request is without any authentication contained
    @create_api({
        'run_on_preflight': False,
        'allowed_iss': ['http://keycloak:8080/auth/realms/master']
    })
    @call_api(method='options')
    def test_preflight_success(self, status, body):
        self.assertEqual(OK, status)

    ############################################################################
    # Test if plugin denies by default preflight requests in a unauthenticated
    # way ... It needs to fail
    @create_api({
        'allowed_iss': ['http://keycloak:8080/auth/realms/master']
    })
    @call_api()
    def test_preflight_failure(self, status, body):
        self.assertEqual(UNAUTHORIZED, status)
        self.assertEqual('Unauthorized', body.get('message'))

    ############################################################################
    # Test if plugin denies a request param "jwt" which contains no valid token
    # --> It needs to be denied
    @create_api({
        'allowed_iss': ['http://keycloak:8080/auth/realms/master']
    })
    @call_api(params={"jwt": "SomeNonSenseJwtTokenValue.1234"})
    def test_bad_token_as_param(self, status, body):
        self.assertEqual(UNAUTHORIZED, status)

    ############################################################################
    # Test if plugin accepts a request param "jwt" a valid token
    # --> It needs to be allowed
    @create_api({
        'allowed_iss': ['http://keycloak:8080/auth/realms/master']
    })
    @authenticate() # Get current requested token
    @call_api(authentication_type={"queryparam":"jwt"})
    def test_good_token_as_param(self, status, body):
        self.assertEqual(OK, status)

    ############################################################################
    # Test if plugin denies requests if token contains a different algorithm
    # as it is configured for the plugin.
    # Test-Token "STANDARD_JWT" contains 'algorithm': 'RS256'
    @create_api({
        'algorithm': 'HS256',
        'allowed_iss': ['http://keycloak:8080/auth/realms/master']
    })
    @call_api(token=STANDARD_JWT)
    def test_invalid_algorithm(self, status, body):
        self.assertEqual(FORBIDDEN, status)
        self.assertEqual('Invalid algorithm', body.get('message'))


    ############################################################################
    # Test if plugin denies requests if token is issued by a different "iss"
    # Token is only valid for "master" realm
    @create_api({
        'allowed_iss': ['http://keycloak:8080/auth/realms/somethingElseThenMaster']
    })
    @authenticate() # Use current requested token
    @call_api()
    def test_invalid_iss(self, status, body):
        self.assertEqual(UNAUTHORIZED, status)
        self.assertEqual('Token issuer not allowed', body.get('message'))


    ############################################################################
    # Test if plugin denies requests if token is more then 10 minutes valid
    # (in this setup here all fresh requested tokens are 20 minutes valid)
    @create_api({
        'allowed_iss': ['http://keycloak:8080/auth/realms/master'],
        'maximum_expiration': 600
    })
    @authenticate() # Use current requested token
    @call_api()
    def test_max_exp(self, status, body):
        self.assertEqual(FORBIDDEN, status)
        self.assertEqual('Token claims invalid: ["exp"]="exceeds maximum allowed expiration"', body.get('message'))

    ############################################################################
    # Test if plugin denies requests if token contains a bad signature
    @create_api({
        'allowed_iss': ['http://keycloak:8080/auth/realms/master']
    })
    @call_api(token=BAD_SIGNATURE)
    def test_bad_signature(self, status, body):
        self.assertEqual(UNAUTHORIZED, status)
        self.assertEqual('Bad token; invalid signature', body.get('message'))

    ############################################################################
    # Test if plugin denies requests if token is already expired
    #
    # !! Execute this as last test .. it uses a short living token which
    #    was at the beginning of this test cases requested.
    @create_api({
        'allowed_iss': ['http://keycloak:8080/auth/realms/master']
    })
    @call_api(token=TD_TOKEN_EXPIRED)
    def test_invalid_exp(self, status, body):
        self.assertEqual(UNAUTHORIZED, status)
        self.assertEqual('Token claims invalid: ["exp"]="token expired"', body.get('message'))
