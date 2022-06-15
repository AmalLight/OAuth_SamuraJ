<script type='text/javascript' >

    (function loadTokenData () {

           setTimeout ( function () {

               if ( global_functions.getState () !== null )
               {
                   $( '#text_data1' ). val (
                   
                       JSON.stringify ( JSON.parse (

                           base64UrlDecode ( global_functions.getState () [ 'access_token' ].split ( '.' ) [ 0 ] )

                       ) , null , 2 )
                   ) ;
                   
                   $( '#text_data2' ). val (
                   
                       JSON.stringify ( JSON.parse (

                           base64UrlDecode ( global_functions.getState () [ 'access_token' ].split ( '.' ) [ 1 ] )

                       ) , null , 4 )
                   ) ;

               }} , 1000 ) ;
    }()) ;

</script>
