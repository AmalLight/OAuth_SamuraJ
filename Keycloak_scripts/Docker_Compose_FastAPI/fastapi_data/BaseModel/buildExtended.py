import json , os , sys

def buildit ( JSON_content ) :
    json_data = json.loads ( JSON_content )
    
    with open ( 'extended.py' , 'w' ) as f :
         f.write ( 'from pydantic import BaseModel    ' + '\n' )

         # ---------------------------------------------------------------

         f.write ( 'class access_token ( BaseModel ) :' + '\n' )
         f.write ( '  access_token : str              ' + '\n' )

         # ---------------------------------------------------------------

         f.write ( 'class userpassword ( BaseModel ) :' + '\n' )
         f.write ( '  user     : str                  ' + '\n' )
         f.write ( '  password : str                  ' + '\n' )

         # ---------------------------------------------------------------

         f.write ( 'class formfromweb  ( BaseModel ) :' + '\n' )

         if 'Name' in json_data.keys () : f.write ( '  Name : str ' + '\n' )

         for action in json_data [ 'Actions' ].keys () :

             f.write ( '  ' + action + ' : str ' + '\n' )
         f.write     (   '  access_token : str ' + '\n' )

         # ---------------------------------------------------------------

         f.write ( 'class machines_pass_and_access_token ( BaseModel ) :' + '\n' )

         for name in json_data [ 'Name' ].keys () : 
         
             if ( name != 'None' ) and ( name.startswith ( 'Machine' ) ) :

                f.write ( '  ' + name + ' : str ' + '\n' )
         f.write        ( '  access_token : str ' + '\n' )

         # ---------------------------------------------------------------

         f.write ( 'class undo_ssh_copy ( BaseModel ) :' + '\n' )
         
         for name in json_data [ 'Name' ].keys () : 
         
             if ( name != 'None' ) and ( name.startswith ( 'Machine' ) ) :

                f.write ( '  ' + name + ' : bool ' + '\n' )
         f.write        ( '  access_token : str  '        )
