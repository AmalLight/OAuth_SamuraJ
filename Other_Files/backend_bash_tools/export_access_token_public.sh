
user=$1
pass=$2

export access_token=$( \
\
curl -X POST https://keycloak/auth/realms/myrealm/protocol/openid-connect/token --insecure \
             \
            -H 'content-type: application/x-www-form-urlencoded' \
            -d "username=$user" \
            -d "password=$pass" \
            -d 'grant_type=password' \
            -d 'client_id=oauth-playground' | jq --raw-output '.access_token' )
echo ''
echo $access_token
echo ''
