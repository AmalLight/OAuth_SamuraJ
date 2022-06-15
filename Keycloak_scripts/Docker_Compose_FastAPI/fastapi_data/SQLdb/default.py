from SQLdb.database import engine
from SQLdb.tables   import Base
from sqlalchemy     import text

from client_safe_submit import recusive_option

def create () :

    with engine.connect () as connection :

         Base.metadata.create_all ( bind = engine )

         connection.execute ( text ( " DROP TABLE groups  " ) )
         connection.execute ( text ( " DROP TABLE actions " ) )
        
         Base.metadata.create_all ( bind = engine )

def clean () :

    with engine.connect () as connection :
    
         connection.execute ( text ( " DELETE FROM groups  * " ) )
         connection.execute ( text ( " DELETE FROM actions * " ) )
    
def reset ( Actions_dict , Groups_dict ) :

    for action_name in Actions_dict.keys () :
    
        action_cmd     = Actions_dict [ action_name ][ 0 ]
        action_enable  = Actions_dict [ action_name ][ 1 ]
        action_disable = Actions_dict [ action_name ][ 2 ]
        action_id      = Actions_dict [ action_name ][ 3 ]

        action_enable  = ( '' if action_enable  == '.' else action_enable  )
        action_disable = ( '' if action_disable == '.' else action_disable )

        action_enable  = [ str ( number ) for number in recusive_option ( action_enable , ''  , '.' , [] , [] ) ]
        action_disable = [ str ( number ) for number in recusive_option ( '' , action_disable , '.' , [] , [] ) ]
        
        action_enable  = ' '.join ( action_enable  )
        action_disable = ' '.join ( action_disable )

        with engine.connect () as connection :
            
             connection.execute ( text ( " INSERT INTO actions VALUES ( {} , '{}' , '{}' , '{}' , '{}' ) ".
             format ( action_id , action_name , action_enable , action_disable , action_cmd ) ) )

    # -------------------------------------------------

    for group_name in Groups_dict.keys () :

        group_id  = Groups_dict [ group_name ][ 0 ]
        group_can = Groups_dict [ group_name ][ 1 ]

        group_can = ( '' if group_can == '.' else group_can )

        group_can = [ str ( number ) for number in recusive_option ( group_can , ''  , '.' , [] , [] ) ]
        
        group_can  = ' '.join ( group_can  )

        with engine.connect () as connection :
            
             connection.execute ( text ( " INSERT INTO groups VALUES ( {} , '{}' , '{}' ) ".
             format ( group_id , group_name , group_can ) ) )
