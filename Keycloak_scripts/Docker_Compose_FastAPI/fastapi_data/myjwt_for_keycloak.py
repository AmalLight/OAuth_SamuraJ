import jwt , base64 , json

public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs/uorMzhqwvcq59NoWfVOeuGyQ186E1EZRp8lWdaM+uMOP6PXMvrAjBqRExC1PjR8h+GVh8VoYJmPAp+Lk8vgdE4VZFAVP0cUZgg+rhBtaX7HIOSPA7+9vt3MPD/ObHQkP/rZU+zYP4BY3QzLbRgwZJ03RCf+67pF4bbvEkLlu73v58qCXdkhtTDXdODwcTuZpKo4HbsQnvpGSG4V3P6fmTl0MFy1w6sSSuwANPPlHkp9GOWkcUvEiM5h1juV3iWlcDLcX3V2LtDQb4cMwfAW/kCMkLMoMwSJMxbyIpSMHvniKOODK5AinlpTw1GJxOJDF+Jbh/Pu123h5JuvlatwwIDAQAB"

public_key = "-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----".format ( public_key )

# https://www.janua.fr/keycloak-access-token-verification-example/
# https://jwt.io/
# https://pypi.org/project/jwt/
# https://pypi.org/project/PyJWT/

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------

def base64UrlDecode ( data ) :
    while data.count ( '-' ) : data = data.replace ( '-' , '+' ) ;
    while data.count ( '_' ) : data = data.replace ( '_' , '/' ) ;

    pad = len ( data ) % 4 ;

    if ( pad ) and ( pad == 1 ) : return False # 'Invalid Length for base64'

    elif pad : data += ( '=' * ( 5-pad-1 ) ) ;

    return base64.b64decode ( data ) ;

def tokentest ( data , username = None ) :

    access_token = None
    da_ritorno = 'Empty'

    # Access_token key is not present in json data: {}'.format ( str ( data.keys () ) )
    if not 'access_token' in data : return False , False

    access_token       = data    [ 'access_token' ] ;
    access_token_split = access_token.split ( '.' ) ;
    
    # "Invalid Length for access_token split"
    if len ( access_token.split ( '.' ) ) != 3 : return False , False

    headers_encode = access_token_split [ 0 ] ;
    body_encode    = access_token_split [ 1 ] ;
    signature      = access_token_split [ 2 ] ;

    headers_decode   = base64UrlDecode ( headers_encode ).decode () ; # to string type
    body_decode      = base64UrlDecode ( body_encode    ).decode () ; # to string type

    if False in [ headers_decode , body_decode ] : return False , False

    # The JSON.parse method parses a JSON string, constructing the JavaScript value or object described by the string == json.loads
    headers_decode_json = json.loads ( headers_decode ) ;
    body_decode_json    = json.loads ( body_decode    ) ;

    access_token_again_json , access_token_again_str = None , None
    try:
            access_token_again_json = jwt.decode ( access_token , public_key , algorithms = [ 'RS256' ] , audience = 'oauth-playground' )
    except: access_token_again_str  ,              access_token_again_json = 'NULL' , None

    return body_decode_json , ( ( access_token_again_json != None ) and ( body_decode_json [ 'preferred_username' ] == username if username else True ) )
