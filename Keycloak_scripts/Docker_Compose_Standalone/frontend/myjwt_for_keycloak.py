import jwt , base64 , json

public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlqOIc4M3dijPGDGjktaV+wUNVodFEfJXfYE2kgApJYtQNSQUEZ26lKiYIyObZHpUN63SVjXp+dLvPkvK9r3b3Vndchxwjhpi7e1wgGxSHiJc1ZlFjL4YHhqzjk+ar4CRN5Vn6sQG9jnmBgPiF49A/MIO08vbh6Pov/vS2R4iQWDxdJHrI2qxsREs4v+O1AekGd2ZVZJ9kDbh18dx+mitWMJPfaO1NAGqF7pCHgCuMF1V8MHZ+B4JLpz3FmolKMpF2RNNKKCij56b2Hds3EXDIAq3OsjMcyRNxiluj04DQ2WK/jHs9TJMe9yeB7Lt2j4MW4lfefu1OBb6n/o80ahYeQIDAQAB"

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

def tokentest ( data , username=None ) :

    access_token = None
    da_ritorno = 'Empty'

    # Access_token key is not present in json data: {}'.format ( str ( data.keys () ) )
    if not 'access_token' in data : return False

    access_token       = data    [ 'access_token' ] ;
    access_token_split = access_token.split ( '.' ) ;
    
    # "Invalid Length for access_token split"
    if len ( access_token.split ( '.' ) ) != 3 : return False

    headers_encode = access_token_split [ 0 ] ;
    body_encode    = access_token_split [ 1 ] ;
    signature      = access_token_split [ 2 ] ;

    headers_decode   = base64UrlDecode ( headers_encode ).decode () ; # to string type
    body_decode      = base64UrlDecode ( body_encode    ).decode () ; # to string type

    if False in [ headers_decode , body_decode ] : return False

    # The JSON.parse method parses a JSON string, constructing the JavaScript value or object described by the string == json.loads
    headers_decode_json = json.loads ( headers_decode ) ;
    body_decode_json    = json.loads ( body_decode    ) ;

    access_token_again_json , access_token_again_str = None , None
    try:
            access_token_again_json = jwt.decode ( access_token , public_key , algorithms=['RS256'] , audience='oauth-playground' )

    except: access_token_again_str  ,              access_token_again_json = 'NULL' , None

    """ FOR DEBUG

    if access_token_again_str :

       while access_token_again_str.count ( "'" ) or body_decode.count ( "'" ) :

             access_token_again_str = access_token_again_str.replace ( "'"  , '"' )
             body_decode            =            body_decode.replace ( "'"  , '"' )

       while access_token_again_str.count ( ' ' ) or body_decode.count ( ' ' ) :
         
             access_token_again_str = access_token_again_str.replace ( ' ' , '' )
             body_decode            =            body_decode.replace ( ' ' , '' )

       while access_token_again_str.count ( '\n' ) or body_decode.count ( '\n' ) :

             access_token_again_str = access_token_again_str.replace ( '\n' , ''  )
             body_decode            =            body_decode.replace ( '\n' , ''  )

       while access_token_again_str.count ( 'true'  ) or body_decode.count ( 'true'  ) :

             access_token_again_str = access_token_again_str.replace ( 'true'  , 'True' )
             body_decode            =            body_decode.replace ( 'true'  , 'True' )

       while access_token_again_str.count ( 'false' ) or body_decode.count ( 'false' ) :

             access_token_again_str = access_token_again_str.replace ( 'false' , 'False' )
             body_decode            =            body_decode.replace ( 'false' , 'False' )

    first_response = ( ( 'not ' if not ( access_token_again_str == body_decode ) else '' ) + 'Verified' ) if access_token_again_json else 'Failed'
    
    second_response = 'access token is not vaild for decoding ( maybe it\'s expired )' if ( first_response == 'Failed' ) else ( 'Credential was ' + first_response )

    """

    return ( ( access_token_again_json != None ) and ( body_decode_json [ 'preferred_username' ] == username if username else True ) )
