
def StringSymbol ( stringa , index_symbol ) :

    if    stringa.count ( '!' ) : return [ stringa.index ( '!' ) , '!' ]
    elif  stringa.count ( 'U' ) : return [ stringa.index ( 'U' ) , 'U' ]
    elif  stringa.count ( '&' ) : return [ stringa.index ( '&' ) , '&' ]
    else :                        return [                 -1    , '.' ]

# -----------------------------------------------------------------------------

def recusive_option ( string_left , string_right , symbol , list_left , list_right ) :

    if ( symbol == '!' ) or ( symbol == 'U' ) or ( symbol == '&' ) :

        list_left  = recusive_option ( string_left  , '' , '.' , [] , [] )
        list_right = recusive_option ( '' , string_right , '.' , [] , [] )

        if     ( symbol == '!' ) : list_left , list_right = [ left for left in list_left if not left in list_right ] , []
        elif   ( symbol == 'U' ) or ( symbol == '&' ) :

            if ( symbol == 'U' ) and len ( list_left ) and len ( list_right ) :

                last , first = list_left [ -1 ] , list_right [ 0 ]

                for i in range ( last + 1 , first ) : list_left += [ i ]

    # -----------------------------------------------------------------------------

    elif ( symbol == '.' ) :

        if   ( len ( string_left  ) in [ 1 , 2 ] ) : return [ int ( string_left  ) ]
        elif ( len ( string_right ) in [ 1 , 2 ] ) : return [ int ( string_right ) ]
        elif ( len ( string_left  ) or                        len ( string_right ) ) :

            string_to_search = ""

            if   len ( string_left  ) : string_to_search = string_left
            elif len ( string_right ) : string_to_search = string_right
        
            Array_StringSymbol = StringSymbol ( string_to_search , 0 )

            index_symbol , local_symbol = Array_StringSymbol [ 0 ] , Array_StringSymbol [ 1 ]

            if ( index_symbol > -1 ) :

                return recusive_option ( string_to_search [ : index_symbol ] , string_to_search [ index_symbol + 1 : ] , local_symbol , [] , [] )

    return list_left + list_right

# -----------------------------------------------------------------------------

from SQLdb.database import engine
from sqlalchemy     import text

def optionstest ( body_decode_json , data ) :
    user_groups = body_decode_json [ 'group' ]

    user_can = []
    user_group_can = []

    data_copy = data.copy ()
    del data_copy [ 'access_token' ]

    list_actions_name = []
    list_actions_id   = []

    for key  in data_copy :
        name  = data_copy [ key ]

        if name == 'None' : continue
        else : list_actions_name += [ name ]

    # -----------------------------------------------------------------------------

    with engine.connect () as connection :

        for i1 , name in enumerate ( list_actions_name ) :

            results = connection.execute ( text ( " SELECT id , action_enable , action_disable FROM actions WHERE action_name = '{}' ".format ( name ) ) )

            for result in results :
                action_id      = str ( result [ 0 ] )
                action_enable  = str ( result [ 1 ] ).split ( ' ' )
                action_disable = str ( result [ 2 ] ).split ( ' ' )

                if ( i1 == 0 ) :
                   user_can = [ action_id ]
                   for i2 in range ( 1 , 100 ) :
                       if ( not str ( i2 ) in user_can       ) and \
                          ( not str ( i2 ) in action_disable ) : user_can += [ str ( i2 ) ]

                if ( not action_id in user_can ) : return False
                list_actions_id += [ action_id ]

                for action_on in action_enable :
                    if ( not action_on  in user_can ) and \
                       ( not action_on == action_id ) : user_can += [ action_on ]

                for action_off in action_disable :
                    if (     action_off in user_can  ) and \
                       ( not action_off == action_id ) :

                         i = user_can.index ( action_off )
                         user_can = user_can [ : i ] + user_can [ i+1 : ]

        for user_group in user_groups :
            results = connection.execute ( text ( " SELECT action_list FROM groups WHERE group_name = '{}' ".format ( user_group ) ) )
            for result in results :
                for can in str ( result [ 0 ] ).split ( ' ' ) :

                    if not can in user_group_can : user_group_can += [ can ]

    # -----------------------------------------------------------------------------

    for    action_id in list_actions_id :
        if action_id in user_group_can  : continue

        else : return False

    return True
