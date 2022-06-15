
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

                for i in range ( last , first ) : list_left += [ i ]

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

def data_copy_dict ( commands , input_file ) :

    da_ritorno , i = {} , 1
    
    for key  in commands [ 'Name'    ] : da_ritorno [ key ] , i = i , i+1
    for key1 in commands [ 'Actions' ] :

        for key2 in commands [ 'Actions' ] [ key1 ] : da_ritorno [ key2 ] , i = i , i+1

    da_ritorno_str = str ( da_ritorno )
    while da_ritorno_str.count ( ',' ) : da_ritorno_str = da_ritorno_str.replace ( ',' , '\n' )

    file_shell = open ( input_file , 'w' )
    file_shell.write ( da_ritorno_str )
    file_shell.close ()

    return da_ritorno

# -----------------------------------------------------------------------------

def optionstest ( data , commands , data_copy_dict ) :

    data_copy = data.copy ()
    del data_copy [ 'access_token' ]

    enable_list = [*range ( 1 , 100 )]

    for key in data_copy :

        try :   commands_key = commands [ key ] if 'Name' == key else commands [ 'Actions' ][ key ]
        except: return False
        
        key_name     = data_copy      [ key      ] # form_key
        key_name_int = data_copy_dict [ key_name ] # form_value
        
        if ( key_name == 'None' ) or ( key_name_int in enable_list ) :

            enable_list_key  = commands_key [ key_name ][ 1 ]
            disable_list_key = commands_key [ key_name ][ 2 ]

            if not disable_list_key.count ( '.' ) :
                   disable_list_key = recusive_option ( '' , disable_list_key , '.' , [] , [] )

                   enable_list  = [ e for e in enable_list if not e in disable_list_key ]

            if not enable_list_key.count ( '.' ) :
                   enable_list_key = recusive_option ( enable_list_key , ''  , '.' , [] , [] )

                   enable_list += [ e for e in enable_list_key if not e in enable_list ]

        else : return False
    return True

