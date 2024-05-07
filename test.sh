#!/bin/bash
set -eo pipefail

export ARTIFACTORY_URL=registry.gitlab.com/telepo/smg/artifactory
export HTTPBIN_IMAGE="$ARTIFACTORY_URL/mirror-httpbin:latest"
export PGADMIN_IMAGE="$ARTIFACTORY_URL/mirror-pgadmin4:7.5"
export POSTGRES_IMAGE="$ARTIFACTORY_URL/mirror-postgres:15.3-bookworm"
export KEYCLOAK_IMAGE="$ARTIFACTORY_URL/mirror-keycloak:15.0.2"

make stop
make SHELL='sh -x' default keycloak-start start
make SHELL='sh -x' helpers-start
make SHELL='sh -x' test-integration || ( rc=$?; docker logs --details kong; docker logs --details kong_test_keycloak; docker exec kong cat '/proxy_error.log'; docker logs --details kong_test_httpbin; exit $rc)
