
function Array_remove ( A1 , A2 )
{
    if      (   A1.length ==  0 ) return [] ;
    else if (   A2.length ==  0 ) return A1 ;
    else if ( [ A2 ]      == A1 ) return [] ;
    else
    {
        var lista = [] ;

        var  A1_Index_A2 = A1.indexOf ( A2 ) ;
        if ( A1_Index_A2 > -1 ) {

            for ( var i = 0 ; i < A1.length ; i++ )

                if ( i != A1_Index_A2 ) lista.push ( A1 [ i ] ) ;

            return lista ;
        }
    }
    
    return A1 ;
}

function StringSymbol ( stringa , index_symbol )
{
    if      ( ( index_symbol = stringa.indexOf ( '!' ) ) > -1 ) return [ index_symbol , '!' ] ;
    else if ( ( index_symbol = stringa.indexOf ( 'U' ) ) > -1 ) return [ index_symbol , 'U' ] ;
    else if ( ( index_symbol = stringa.indexOf ( '&' ) ) > -1 ) return [ index_symbol , '&' ] ;
    else                                                        return [ -1           , '.' ] ;
}

function recusive_option ( string_left , string_right , symbol , list_left , list_right )
{
    string_left  = string_left .toString () ; // fixing JavaScript bug ( using json )
    string_right = string_right.toString () ; // fixing JavaScript bug ( using json )
    
    // alert ( 'string left: ' + string_left + ' string right: ' + string_right + ' symbol: ' + symbol ) ;
    // ---------------------------------------------------------------------------------------------------

    if ( ( symbol == '!' ) || ( symbol == 'U' ) || ( symbol == '&' ) )
    {
        list_left  = recusive_option ( string_left ,  '' , '.' , [] , [] ) ;
        list_right = recusive_option ( '' , string_right , '.' , [] , [] ) ;

        if ( symbol == '!' )
    
            for ( var right of list_right ) list_left = Array_remove ( list_left , right ) ;

        else if ( ( symbol == 'U' ) || ( symbol == '&' ) )
        {
            if  ( ( symbol == 'U' ) && ( list_left.length > 0 ) && ( list_right.length > 0 ) )
            {
                var last  = list_left  [ list_left.length - 1 ] ;
                var first = list_right [ 0                    ] ;

                while ( ( last < first ) && ( ( ++ last ) < first ) ) list_left.push ( last ) ;
            }
            
            return list_left.concat ( list_right ) ;
        }
    }
    
    // -----------------------------------------------------------------------------

    else if ( symbol == '.' )
    {
        var  string_to_search   =                string_left         ;
        var  Array_StringSymbol = StringSymbol ( string_left  , -1 ) ;

        if ( Array_StringSymbol [ 0 ] == -1 ) {
             string_to_search   =                string_right        ;
             Array_StringSymbol = StringSymbol ( string_right , -1 ) ;
        }

        var index_symbol = Array_StringSymbol [ 0 ] ;
        var local_symbol = Array_StringSymbol [ 1 ] ;
        
        if      ( ( index_symbol <  0 ) && ( string_right.length == 0 ) ) return [ parseInt ( string_left  ) ] ;
        else if ( ( index_symbol <  0 ) && ( string_left. length == 0 ) ) return [ parseInt ( string_right ) ] ;
        else if (   index_symbol > -1 )

            return recusive_option ( string_to_search.substring ( 0 , index_symbol     ) ,
                                     string_to_search.substring (     index_symbol + 1 ) , local_symbol , [] , [] ) ;
    }

    // -------------------------------------------------------
    // alert ( 'list: ' + list_left + ' symbol: ' + symbol ) ;

    return list_left ;
}

