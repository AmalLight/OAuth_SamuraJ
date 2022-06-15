function getTextHTML ( url , callback1 , callback2 ) {

    var request = new XMLHttpRequest () ;
    
    request.onreadystatechange = function ()
    {
        if ( request.readyState === 4 && ( url === 'manage'  || request.status === 200 ) )
        {
            var type = request.getResponseHeader ( 'Content-Type' ) ;
            if ( type.indexOf ( "text" ) !== 1 )
            {
                if ( callback1 !== null ) callback1 ( request.responseText ) ;
                if ( callback2 !== null ) callback2 ( request.responseText ) ; // for inject disable+CANT in the shell
            }
        }
    }
    
    if ( url == 'manage.html' ) {
    
        var data_to_send = {}
    
        if ( global_functions.getParam ( 'access_token' ) != null )

             data_to_send [ 'access_token' ] = global_functions.getParam ( 'access_token' ) ;

        request.open ( 'POST', '/manage' ) ;
        request.setRequestHeader ( "Content-Type" , "application/json;charset=UTF-8" ) ;
        request.send ( JSON.stringify ( data_to_send ) ) ;
    }
    
    else {
    
        url = ( url.includes ( '.html' ) ? '/static/pages/' : '/static/js/' ) + url ;

        request.open ( 'GET', url , true  ) ;
        request.send ( null               ) ;
    }
}

function loadcontent ( url , callback ) {
	
	 getTextHTML ( url + '.html' , function ( file_text )
	 {
             if ( file_text.length > 0 )
             {
                 if ( url != 'manage' ) 

                      { document.getElementById ( 'toloadcontent1' ).innerHTML = file_text ;
                        document.getElementById ( 'toloadcontent2' ).innerHTML = "" ; }
                 else { document.getElementById ( 'toloadcontent2' ).innerHTML = "<br><text>" + file_text + "</text>" ;
                        document.getElementById ( 'toloadcontent1' ).innerHTML = "" ; 

                 if ( file_text.includes ( 'iframe' ) ) document.getElementById ( 'toloadcontent2' ).innerHTML = file_text ; }
             }

         } , null ) ;
	
	 if ( url !== 'manage' )
         {
              getTextHTML ( url + '.js' ,

              function ( file_text ) { $( document.body ).append ( file_text ) ; }

	, callback )} ;
}
