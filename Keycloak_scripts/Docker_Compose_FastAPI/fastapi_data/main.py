import myjwt_for_keycloak , JSON.HTMLfromJSON , client_safe_submit , paramiko_cmd

import json , os , sys , importlib , extended , requests

from os.path           import exists
from fastapi           import FastAPI , Request
from fastapi.responses import HTMLResponse , RedirectResponse , FileResponse

from starlette.staticfiles import StaticFiles

# -------------------------------------------------------------------------------------------------------

app = FastAPI ()

app.mount ( "/static" , StaticFiles ( directory = "static" ) , name = "static" )

index_html_text = ''
with open ( './static/pages/index.html' , 'r' ) as f : index_html_text += f.read ()

see_your_token_headers = { 'content-type': 'application/x-www-form-urlencoded' }

# -------------------------------------------------------------------------------------------------------

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware (

    CORSMiddleware ,
    allow_origins = [ "*" ]  ,
    allow_credentials = True ,
    allow_methods = [ "*" ]  ,
    allow_headers = [ "*" ]  )

# -------------------------------------------------------------------------------------------------------

@app.get ( "/" , response_class = HTMLResponse )
async def home_page ( ) :
      global headers  , index_html_text
      return HTMLResponse ( content = index_html_text , status_code = 200 )

@app.get ( '/favicon.ico' )
async def   send_favicon () : return FileResponse ( './orbz_death.ico' )

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

def verify_Token_and_run (

    base_data , req : Request , test_user : str = None ,

    reload_json : bool = False , test_group : bool = False , executed_CMD : bool = False ) :

    if not req.headers [ 'Content-Type' ].count ( 'application/json' ) :

       return 'Request is not an application/json: {}'.format ( req.headers [ 'Content-Type' ] )

    data , return_value = base_data.dict () , ''

    # data for selected options
    # body_decode_json for group
    body_decode_json , testToken = myjwt_for_keycloak.tokentest ( data , test_user )
    return_value  = ( 'Token:' + str ( testToken ) )

    if reload_json : reload_json = JSON.HTMLfromJSON.saveHTMLasShell ( 'JSON/template.json' ) if testToken else False
    return_value += ( '; reloadJSON:' + str ( reload_json ) )

    if test_group  : test_group = client_safe_submit.optionstest ( body_decode_json , data ) if ( testToken and not reload_json ) else False
    return_value += ( '; Group:' + str ( test_group ) )

    if executed_CMD : executed_CMD = paramiko_cmd.run_commands ( data ) if test_group == True else False
    return_value += ( '; Paramiko:' + str ( executed_CMD ) )

    if ( test_user ) and ( not reload_json ) and ( not test_group ) and ( not executed_CMD ) : return testToken
    else :                                                                                     return return_value

@app.post ( '/paramiko' )
async def paramiko ( formfromweb : extended.formfromweb , req : Request ) :
      return verify_Token_and_run ( formfromweb , req , None ,  False , True , True )

@app.post ( '/see_your_access_token' )
async def see_your_access_token ( userpassword : extended.userpassword ) :

      data = { 'username' : userpassword.dict () [ 'user'     ] ,
               'password' : userpassword.dict () [ 'password' ] ,
               'grant_type' : 'password' , 'client_id' : 'oauth-playground' }

      response = requests.post ( 'https://keycloak:8443/auth/realms/myrealm/protocol/openid-connect/token' ,
                 headers = see_your_token_headers , verify = False , data = data )

      try_toCatch = None
      try :    try_toCatch = json.loads ( response.content ) [ 'access_token' ]
      except : try_toCatch = None
      return   try_toCatch

@app.post ( '/reloadJSON' )
# we need to keep alive: --reload-include extended.py --reload for docs
async def reloadJSON ( access_token : extended.access_token , req : Request ) :
      return verify_Token_and_run ( access_token , req , 'admin' , True , False , False )

@app.post ( '/init_all_machines' )
async def     init_all_machines  (

      machines_pass_and_access_token : extended.machines_pass_and_access_token , req : Request ) :

      if verify_Token_and_run ( machines_pass_and_access_token , req , 'admin' , False , False , False ) :

         return paramiko_cmd.init_all_machines ( machines_pass_and_access_token.dict () )

      return False

@app.post ( '/reload_with_init' )
async def reload_with_init ( 

      machines_pass_and_access_token : extended.machines_pass_and_access_token , req : Request ) :

      if verify_Token_and_run ( machines_pass_and_access_token , req , 'admin' , False , False , False ) :
      
         return ( verify_Token_and_run ( machines_pass_and_access_token , req , 'admin' , True , False , False ) ,

         paramiko_cmd.init_all_machines ( machines_pass_and_access_token.dict () ) )

      return False

@app.post ( '/undo_ssh_copy' )
def undo_ssh_copy ( machine_names_and_access_token : extended.undo_ssh_copy , req : Request ) :

    if verify_Token_and_run ( machine_names_and_access_token , req , 'admin' , False , False , False ) :
    
       return paramiko_cmd.undo_ssh_copy ( machine_names_and_access_token.dict () )

    return False
