<script type='text/javascript' >

    function disable ()
    {
        var option_list     = document.getElementsByTagName ( 'option' ) ;
        var option_list_len = option_list.length ;
        
        var global_list_toDisable = [] ;

        // -------------------------------------------------------------------------------------------------
        
        for ( var i1 = 0 ; i1 < option_list_len ; i1 ++ ) option_list [ i1 ].className = 'd-block' ;
        for ( var i2 = 0 ; i2 < option_list_len ; i2 ++ )
        {
            var option = option_list [ i2 ] ;
            
            // NO make actions for disabled values
            var disabled = ( global_list_toDisable.indexOf ( i2 ) >= 0 ) ;
            var selected = false ;

            if ( ( option.value != 'None' ) && ( ! disabled ) )
            
                for ( var select of document.getElementsByTagName ( 'select' ) )

                    if ( select.value == option.value ) { selected = true ; break ; }

            if ( selected )
            {
                var option_id = option.id ;
            
                var  enable_list = option.id.split ( '_' ) [ 0 ] ;
                var disable_list = option.id.split ( '_' ) [ 1 ] ;

                if ( ! disable_list.includes ( '.' ) )
                {
                    var list_toDisable = recusive_option ( '' , disable_list , '.' , [] , [] ) ;
                
                    for ( var disable of list_toDisable )

                        if ( ( disable <= option_list_len                        ) && // I can't disable myself
                             ( option_list [ disable - 1 ].value != 'None'       ) &&
                             ( option_list [ disable - 1 ].value != option.value ) )

                               global_list_toDisable = global_list_toDisable.concat ( disable - 1 ) ;
                }
 
                var index_toDisable = -1 ;
                
                if ( ! enable_list.includes ( '.' ) )
                {
                    var list_toEnable = recusive_option ( enable_list , '' , '.' , [] , [] ) ;

                    for ( var enable of list_toEnable )

                        if ( ( enable <= option_list_len                        ) && // I can't enable myself
                             ( option_list [ enable - 1 ].value != 'None'       ) &&
                             ( option_list [ enable - 1 ].value != option.value ) )
                               
                             while ( ( index_toDisable = global_list_toDisable.indexOf ( enable - 1 ) )  > -1 )
                                                         global_list_toDisable.splice  ( index_toDisable ,  1 ) ;
                }
            }
        }

        // -------------------------------------------------------------------------------------------------

        var user_can  = [] ;

        var  user_groups = global_functions.getParam ( 'group' ) ;
        if ( user_groups !== null )
        
           for ( var user_group of user_groups )
               if  ( user_group in      groups )
               
               user_can = user_can.concat ( recusive_option ( groups [ user_group ] , '.' , '.' , [] , [] ) ) ;
        
        for ( var i = 1 ; i < 100 ; i++ )

            if ((                        i <= option_list_len ) &&
                ( user_can.indexOf              ( i     ) < 0 ) && /* is cant   */
                ( global_list_toDisable.indexOf ( i - 1 ) < 0 ) && /* to import */
                ( option_list                   [ i - 1 ].value !=       'None' ) )

                  global_list_toDisable = global_list_toDisable.concat ( i - 1 ) ;

        // -------------------------------------------------------------------------------------------------

        for ( var disable of global_list_toDisable )
        {
              option_list [ disable ].className = 'd-none' ;

              for ( var select of document.getElementsByTagName ( 'select' ) )

                    if ( ( option_list [ disable ].value == select.value ) ) select.value = 'None' ;
        }
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
