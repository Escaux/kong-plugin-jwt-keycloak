import os

# global variables for all the test cases
setup_done = False

TD_TOKEN_EXPIRED = None
KC_ADMIN_TOKEN = None

CLIENT_ID = os.environ.get("CLIENT_ID", "test")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "c0bc799c-4dfc-4841-af01-0f1a00171c32")

KONG_API = os.environ.get("KONG_API", "http://kong:8000")
KONG_ADMIN = os.environ.get("KONG_ADMIN", "http://kong:8001")
KONG_METRICS = os.environ.get("KONG_METRICS", "http://kong:8002")

KC_USER = os.environ.get("KC_USER", "admin")
KC_PASS = os.environ.get("KC_PASS", "admin")
KC_HOST = os.environ.get("KC_HOST", "http://keycloak:8080/auth")
KC_REALM = KC_HOST + "/realms/master"
