/***********************/
/* OAuth 2.0 functions */
/***********************/

function loadDiscovery ()
{
    // alert ( 'B' ) ;

    global_functions.setState ( 'issuer' , 'https://keycloak/auth/realms/myrealm' ) ;

    var req = new XMLHttpRequest () ;

    req.onreadystatechange = function ()
    {
        if ( req.readyState === 4 )
        {
            global_functions.setState ( 'authorization_endpoint' , JSON.parse ( req.responseText ) [ 'authorization_endpoint' ] ) ;
            global_functions.setState ( 'token_endpoint'         , JSON.parse ( req.responseText ) [ 'token_endpoint'         ] ) ;
        }
    }

    req.open ( 'GET' , global_functions.getParam ( 'issuer' ) + '/.well-known/openid-configuration' , true ) ;
    req.send () ;
}

function generateAuthorizationRequest ()
{
    // alert ( 'D' ) ;

    var req  = global_functions.getParam ( 'authorization_endpoint' ) ;

        req += '?response_type=code' ;
        req += '&client_id='    + global_functions.getClientId () ; // optional for scope : scope
        req += '&redirect_uri=' + global_functions.getRedirect () ;

    document.location.href = req ;
}
// --------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------

function tryLogin () // authorizationRequest ()
{
    // alert ( 'C' ) ;

    alert ( 'You Pressed Login button.' ) ;

    generateAuthorizationRequest () ;
}

function tryLogout () // reset ()
{
    alert ( 'You Pressed Logout button.' ) ;

    var redirect = global_functions.getRedirect (          ) ;
    var main_url = global_functions.getParam    ( 'issuer' ) ;
                   global_functions.resetState  (          ) ;

    var req = main_url + '/protocol/openid-connect/logout?redirect_uri=' + redirect ;

    localStorage.removeItem ( 'state' ) ;
    window.location.reload  (         ) ;
    document.location.href       = req  ;
}

// --------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------

function getQueryVariable ( key )
{
    var query = window.location.search.substring ( 1 ) ;
    var vars  = query.split ( '&' ) ;

    for ( var i = 0 ; i < vars.length ; i++ )
    {
        var pair = vars [ i ].split ( '=' ) ;
        if ( decodeURIComponent ( pair [ 0 ] ) == key ) return decodeURIComponent ( pair [ 1 ] ) ;
    }
}

function base64UrlDecode ( input ) {

    input = input
        .replace ( /-/g , '+' )
        .replace ( /_/g , '/' ) ;

    var    pad = input.length % 4;
    if (   pad )
    {
      if ( pad === 1 ) {

          throw new Error ( 'InvalidLengthError: Input base64url string is the wrong length to determine padding' ) ;
      }

      input += new Array ( 5-pad ).join ( '=' ) ;
    }

    return atob ( input ) ;
}

// --------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------

function loadTokens ( code )
{
    // alert ( 'E' ) ;

    var params  = 'grant_type=authorization_code' ;
        params += '&code='         + code                            ;
        params += '&client_id='    + global_functions.getClientId () ;
        params += '&redirect_uri=' + global_functions.getRedirect () ;

    var req = new XMLHttpRequest () ;
    req.onreadystatechange = function ()
    {
        if ( req.readyState === 4 )
        {
            var response = JSON.parse ( req.responseText ) ;

            if ( response [ 'access_token' ] )
            {   global_functions.setState ( 'access_token'  , response [ 'access_token'  ] ) ;
                global_functions.setState ( 'refresh_token' , response [ 'refresh_token' ] ) ;
                
                loadcontent ( 'data' , null ) ;
                client_init (               ) ;
            }
        }
    }

    req.open ( 'POST' , global_functions.getParam ( 'token_endpoint' ) , true ) ;
    req.setRequestHeader ( 'Content-type' , 'application/x-www-form-urlencoded' ) ;
    req.send ( params ) ;

    window.history.pushState ( {} , document.title , '/' ) ;
}

function jqueryId_none ( list_id , ifNone ) {

    for ( var id of list_id )

        if ( ifNone == true ) {

            if ( $( id ).attr     ( 'class'  ).includes    ( 'd-block' ) )
                 $( id ).addClass ( 'd-none' ).removeClass ( 'd-block' )
        }
        
        else {
        
            if ( $( id ).attr     ( 'class'   ).includes    ( 'd-none' ) )
                 $( id ).addClass ( 'd-block' ).removeClass ( 'd-none' )
        }
}

function client_init ()
{
    // alert ( 'A' ) ;
    
    jqueryId_none ( [ '#Data' , '#Manage' , '#Shell' ] , true ) ;

    global_functions.loadOldState () ;
    global_functions.setState ( 'CAN' , null ) ;
    
    loadDiscovery () ;
    
    if ( global_functions.getParam ( 'access_token' ) != null ) {

        jqueryId_none ( [ '#Data' , '#Manage' , '#Shell' ] , false ) ;
        
        var payload = JSON.parse ( base64UrlDecode  ( global_functions.getParam ( 'access_token' ).split ( '.' ) [ 1 ] ) ) ;

        if ( 'CANT' in payload )

            global_functions.setState ( 'CANT' , recusive_option ( payload [ 'CANT' ] , '' , '.' , [] , [] ) ) ;
    }

    var  code = getQueryVariable ( 'code' ) ; // get 'www.../?...' and it searches for 'code=X' then it will return X
    if ( code ) {     loadTokens (  code  ) ; }

    var  error            = getQueryVariable ( 'error'             ) ;
    var  errorDescription = getQueryVariable ( 'error_description' ) ;
    if ( error ) alert ( 'error-authorizationResponse: ' + errorDescription ) ;
}
