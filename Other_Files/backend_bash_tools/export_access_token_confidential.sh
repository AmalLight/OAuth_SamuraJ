export access_token=$( \
\
curl -X POST https://keycloak/auth/realms/myrealm/protocol/openid-connect/token --insecure \
             \
           --user mybackend:'d3286e79-0aef-49be-a7a1-70b3bf4c15c1' \
            -H   'content-type: application/x-www-form-urlencoded' \
            -d   'username=kaumi&password=123&grant_type=password' \
             | jq --raw-output '.access_token' )
echo ''
echo $access_token
echo ''
