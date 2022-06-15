
export ACCESS_TOKEN=$( \
\
curl -X POST https://keycloak/auth/realms/master/protocol/openid-connect/token --insecure \
             \
            -H 'content-type: application/x-www-form-urlencoded' \
            -d 'username=admin' \
            -d "password=$1" \
            -d 'grant_type=password' \
            -d 'client_id=admin-cli' | jq --raw-output '.access_token' )
echo ''
echo $ACCESS_TOKEN
echo ''

sleep 2

curl -X  GET https://keycloak/auth/admin/realms/myrealm/users/?briefRepresentation=false --insecure \
             \
             -H "Accept: application/json" \
             -H "Authorization: Bearer ${ACCESS_TOKEN}" \
             
# https://www.keycloak.org/docs-api/11.0/rest-api/
