.DEFAULT_GOAL:=all

REPOSITORY?=telekom-digioss
IMAGE?=kong-plugin-jwt-keycloak
KONG_VERSION?=3.6.1
FULL_IMAGE_NAME:=${REPOSITORY}/${IMAGE}:${KONG_VERSION}

PLUGIN_VERSION?=1.5.0-1

# Tests version separated with spaces
TEST_VERSIONS?=2.8.1 3.0.0 3.1.0 3.2.2 3.3.0 3.5.0

DC:=KONG_VERSION=${KONG_VERSION} PLUGIN_VERSION=${PLUGIN_VERSION} docker compose

### Docker ###

all: run
	

run:
	$(DC) up -d --build kong

stop:
	$(DC) down

### LuaRocks ###

upload:
	luarocks upload kong-plugin-jwt-keycloak-${PLUGIN_VERSION}.rockspec --api-key=${API_KEY}

### Testing ###

test-unit:
	@echo ======================================================================
	@echo "Running unit tests with kong version ${KONG_VERSION}"
	@echo

	$(DC) up --build --abort-on-container-failure test-unit

	@echo
	@echo "Unit tests passed with kong version ${KONG_VERSION}"
	@echo ======================================================================

test-integration:
	@echo ======================================================================
	@echo "Testing kong version ${KONG_VERSION} with ${KONG_DATABASE}"
	@echo

	$(DC) up --build --abort-on-container-failure test-integration

	@echo
	@echo "Testing kong version ${KONG_VERSION} with ${KONG_DATABASE} was successful"
	@echo ======================================================================

test: test-unit test-integration

sleep:
	@sleep 5
