import json , os , sys

from os.path import exists

from flask       import Flask , request , render_template , Response , send_from_directory
from flask_cors  import CORS  , cross_origin

import myjwt_for_keycloak , JSON.HTMLfromJSON , client_safe_submit

# -------------------------------------------------------------------------------------------------------

app = Flask ( __name__ , static_url_path='' )

commands = JSON.HTMLfromJSON.saveHTMLasShell ( './JSON/template.json' )

data_copy_dict = client_safe_submit.data_copy_dict ( commands , './JSON/template_dict.txt' )

index_html_text = ''
with open ( './static/pages/index.html' , 'r' ) as f : index_html_text += f.read ()

# -------------------------------------------------------------------------------------------------------

csp  = ' default-src     * \'self\' data: \'unsafe-inline\' \'unsafe-eval\' ;'
csp += ' media-src       * \'self\' data: \'unsafe-inline\' \'unsafe-eval\' ;'
csp += ' script-src      * \'self\' data: \'unsafe-inline\' \'unsafe-eval\' ;'

headers                                        = { }
headers [ 'Accept-Ranges'                    ] = '*'
headers [ "Access-Control-Allow-Origin"      ] = "*"
headers [ "Access-Control-Allow-Credentials" ] = "false" # Credential is not supported if the CORS header 'Access-Control-Allow-Origin' is '*'
headers [ "Access-Control-Allow-Methods"     ] = "*"     # like to put: ', '.join ( array_methods )
headers [ "Access-Control-Allow-Headers"     ] = "*"     # Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization
headers [ "Content-Security-Policy"          ] = csp     # these were set for the redirect ( from keycloak )

# -------------------------------------------------------------------------------------------------------

@app.route ( '/' , methods=[ 'GET' ] )
def home () :
    global headers  , index_html_text
    return Response ( index_html_text , 200 , headers )

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

@app.route ( '/static/<path:path>' , methods=[ 'GET' ] )
def send_static_files ( path ) :

    if exists ( './static/{}'.format ( path ) ) : return send_from_directory ( 'static' , path )
    else :                                        return '' ;

@app.route ( '/favicon.ico' , methods=[ 'GET' ] )
def send_favicon () :
    return send_from_directory ( '' , 'orbz_death.ico' )
    
@app.route ( '/manage' , methods=[ 'POST' ] )
def manage () :
    global Admin_token

    if not request.content_type.startswith ( 'application/json' ) : return 'Request is not an application/json: {}'.format ( request.content_type )
    
    else :
    
        data = request.get_json ()
    
        if   not 'access_token' in data : return 'Access_token key is not present in json data: {}'.format ( str ( data.keys () ) )
    
        elif not myjwt_for_keycloak.tokentest ( data , 'admin' ) : return 'The token is not like the Server required.'
        
        return send_from_directory ( 'iframe' , 'manage.html' )

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

@app.route ( '/paramiko' , methods=[ 'POST' ] )
def paramiko () :

    if not request.content_type.startswith ( 'application/json' ) : return 'Request is not an application/json: {}'.format ( request.content_type )

    data = request.get_json ()
    
    testToken = myjwt_for_keycloak.tokentest ( data )

    testSelect = ( client_safe_submit.optionstest ( data , commands , data_copy_dict ) if testToken else False )
    
    return ( str ( testToken ) + '; ' + str ( testSelect ) )

