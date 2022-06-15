function getTextHTML ( url_start , url_end , callback1 , callback2 ) {

    var request = new XMLHttpRequest () ;

    request.onreadystatechange = function ()
    {
        if ( request.readyState === 4 && request.status === 200 )
        {
            var type = request.getResponseHeader ( 'Content-Type' ) ;

            if ( type.indexOf ( "text" ) !== 1 )
            {
                if ( callback1 !== null ) callback1 ( request.responseText ) ;

                // ----------------------------------------------------------------

                if ( url_end.includes ( 'html' ) ) {

                     if ( ( url_start == 'shell' ) && ( typeof groups === 'undefined' ) )
                     {
                          var re = /<script>.+<\/script>/g ;
                          var REvalue = request.responseText.match ( re ) ;
                          $( document.body ).append ( REvalue ) ;
                     }

                     getTextHTML ( url_start  , 'js'   , function ( file_text ) {
                          if ( ( ( url_start == 'data'  ) && ( typeof loadTokenData === 'undefined' ) ) ||
                               ( ( url_start == 'shell' ) && ( typeof disable       === 'undefined' ) ) )
                          {
                               $( document.body ).append ( file_text ) ;
                          }} , callback2
                     ) ;
                }

                // ----------------------------------------------------------------

                if ( callback2 !== null && url_end.includes ( 'js' ) )
                     callback2 () ; // run the disable and loadTokenData
            }
        }
    }
    
    url = ( url_end.includes ( 'html' ) ? ( '/static/pages/' + url_start + '.html' ) :
                                          ( '/static/js/'    + url_start + '.js' ) ) ;
    request.open ( 'GET', url , true ) ;
    request.send ( null              ) ;
}

function loadcontent ( url , callback ) {

   getTextHTML ( url , 'html' , function ( file_text )
   {
      if ( file_text.length > 0 )

           document.getElementById ( 'toloadcontent' ).innerHTML = file_text ;

   } , callback ) ;
}
