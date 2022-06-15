<script type='text/javascript' >

    function disable ()
    {
        var option_list = document.getElementsByTagName ( 'option' ) ;

        var option_list_len = option_list.length ;
        
        var global_list_toDisable = [] ;
        
        for ( var i1 = 0 ; i1 < option_list_len ; i1 ++ ) option_list [ i1 ].className = 'd-block' ;
        for ( var i2 = 0 ; i2 < option_list_len ; i2 ++ )
        {
            var option = option_list [ i2 ] ;
            
            // NOT make actions for disabled value
            var selected = ( global_list_toDisable.indexOf ( i2 + 1 ) == -1 ) ;

            if ( selected && ( ! ( selected = false ) ) && ( option.value != 'None' ) )
            
                for ( var select of document.getElementsByTagName ( 'select' ) )

                    if ( selected = ( select.value == option.value ) ) break ;

            if ( selected )
            {
                var option_id = option.id ;
            
                var  enable_list = option.id.split ( '_' ) [ 0 ] ;
                var disable_list = option.id.split ( '_' ) [ 1 ] ;

                if ( ! disable_list.includes ( '.' ) )
                {
                    var list_toDisable = recusive_option ( '' , disable_list , '.' , [] , [] ) ;
                
                    for ( var disable of list_toDisable )

                        if ( disable <= option_list_len )

                            if ( option_list [ disable - 1 ].value    != 'None'   ) {
                                 option_list [ disable - 1 ].className = 'd-none' ;

                                 // NOT disable selected now, i can't disable myself
                                 if ( option_list [ disable - 1 ].value != option.value )

                                     global_list_toDisable = global_list_toDisable.concat ( disable ) ;
                            }
                }
                
                if ( ! enable_list.includes ( '.' ) )
                {
                    var list_toEnable = recusive_option ( enable_list , '' , '.' , [] , [] ) ;

                    for ( var enable of list_toEnable )

                        if ( ( enable <= option_list_len ) && // NOT enable selected now, i can't enable myself
                             ( option_list [ enable - 1 ].value != option.value ) )
                        {
                            option_list [ enable - 1 ].className = 'd-block' ;
                         
                            var  index_toDisable = global_list_toDisable.indexOf ( enable ) ;
                            if ( index_toDisable > -1 )

                                global_list_toDisable.splice ( index_toDisable , 1 ) ;
                        }
                }
            }
        }
        
        for ( var disable of global_list_toDisable )

            if ( disable <= option_list_len )
                        
                for ( var select of document.getElementsByTagName ( 'select' ) )

                    if ( ( option_list [ disable - 1 ].value == select.value ) ) select.value = 'None' ;

        CANT ( option_list , option_list_len ) ;
    }
    
    function CANT ( option_list , option_list_len ) {
    
        if ( global_functions.getParam ( 'CANT' ) !== null )

            for ( var disable of global_functions.getParam ( 'CANT' ) )
            
                if ( ( disable > 0 ) && ( disable <= option_list_len ) )
                
                    option_list [ disable - 1 ].className = 'd-none' ;
    }

    function submitParamiko ()
    {
        var req = new XMLHttpRequest () ;

        req.onreadystatechange = function ()
        {
            if ( req.readyState === 4 )
            {
                alert ( "Response status: " + req.status ) ;

                if ( req.status === 0 ) { alert ( "Backend's Error or Client's Connection error, unreachable" ) ; }
                else                    { alert ( "Backend's Response: " +  req.responseText                  ) ; }
            }
        }

        req.open ( "POST" , "/paramiko" ) ;

        req.setRequestHeader ( "Content-Type" , "application/json;charset=UTF-8" ) ;

        var data_to_send = { 'access_token' : global_functions.getParam ( 'access_token' ) } ;

        var select_list = document.getElementsByTagName ( 'select' ) ;
        
        var select_list_len = select_list.length ;
        
        for ( var i3 = 0 ; i3 < select_list_len ; i3 ++ )
        {
              var select = select_list [ i3 ] ;

              data_to_send [ select.id ] = select.value ;
        }

        req.send ( JSON.stringify ( data_to_send ) ) ;
    }

</script>
