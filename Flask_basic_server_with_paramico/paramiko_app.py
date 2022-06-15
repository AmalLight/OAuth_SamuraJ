from flask import Flask, url_for , request , g , send_from_directory
import paramiko_shell , random

# --------------------------------------------------------

app = Flask ( __name__ , static_folder=None )

@app.route ( '/static/<path:filename>' )
def assets (                filename   ) : return send_from_directory ( 'static' , filename )

# --------------------------------------------------------

@app.before_request
def callme_before_every_request ():
    g.id = str ( random.randint ( 0 , 9 ) )
    for i in range ( 8 ): g.id += str ( random.randint ( 0 , 9 ) )
    request_detail = """
    
    
    ******************************************
    Before Request id: {g_id}
    Before URL:        {url}
    Before Methods:    {methods}
    Before Headers:    {headers} """
                        
    app.logger.debug( request_detail.format ( g_id = g.id , url = request.url , methods = request.method , headers = str ( request.headers ) [:-4] ) )

@app.after_request
def callme_after_every_response ( response ) :
    request_response = """
    ******************************************
    After request id:  {g_id}
    Response:          {response} """
    
    app.logger.debug( request_response.format ( g_id = g.id , response = str ( response ) ) )
    return                    response

# --------------------------------------------------------

@app.route ( '/' , methods=['GET'] )
def basic  (                       ) : return '<br>switch to a.<br><br>' + paramiko_shell.doc ()

@app.route ( '/paramiko' , methods=['POST'] )
def route_paramiko ():
    da_ritorno = 'switch to paramiko.'

    port , pssw = None , 'None'
    ipto , user = None ,  None
 
    data = request.form

    if ( 'port' in data ) and data [ 'port' ]: port = data [ 'port' ]
    if ( 'pssw' in data ) and data [ 'pssw' ]: pssw = data [ 'pssw' ]

    if not port: port=22

    if ( 'cmd' in data ) and ( 'ipto' in data ) and ( 'user' in data ):

        if data [ 'ipto' ] and data [ 'user' ]:

            ipto , user , cmd = data [ 'ipto' ] , data [ 'user' ] , data [ 'cmd' ]

            da_ritorno += '<br>ip   {} done.'.format ( ipto )
            da_ritorno += '<br>user {} done.'.format ( user )
            da_ritorno += '<br>port {} done.'.format ( port )
            da_ritorno += '<br>pssw {} done.'.format ( pssw )
            da_ritorno += '<br>cmd  {} done.'.format (  cmd )

            da_ritorno += '<br>------------------------------'
            da_ritorno += '<br>is Working...'

            da_ritorno += str ( paramiko_shell.connect ( ipto , user , port , pssw , cmd ) )

            da_ritorno += '<br>Working done.'
            da_ritorno += '<br>------------------------------'
            da_ritorno += '<br>END.'

    return da_ritorno

@app.route ( '/<path:default>/' , methods=['GET' , 'POST'] )
def regex_impact ( default ):
    return 'switch to default.'

# --------------------------------------------------------

if __name__ == "__main__": app.run( '0.0.0.0' , port=8066 , debug=True )
