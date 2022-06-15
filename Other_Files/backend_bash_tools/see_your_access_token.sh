echo    ''
echo $( \
\
curl -X POST https://keycloak/auth/realms/myrealm/protocol/openid-connect/token --insecure \
             \
            -H 'content-type: application/x-www-form-urlencoded' \
            -d "username=$1" \
            -d "password=$2" \
            -d 'grant_type=password' \
            -d 'client_id=oauth-playground' | jq .access_token )
echo ''
