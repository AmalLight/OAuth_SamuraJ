import json , os , sys , JSON.FormatHTML
import SQLdb.default 

import BaseModel.buildExtended as builtBaseModel

def takeJSONfile ( input_file ) :
    with open    ( input_file , 'r' ) as f : return f.read ()
    return ''

def transmuteJSONintoHTML ( JSON_content ) :
    # --------------------------------------------------------------

    da_ritorno                = {}
    da_ritorno [ 'text'     ] = ''
    da_ritorno [ 'commands' ] = {}

    json_data = json.loads ( JSON_content )
    Actions_dict = {}
    
    # --------------------------------------------------------------
    
    Names_list_options = []
    for name in json_data [ 'Name' ].keys () :

        input_cmd     = json_data [ 'Name' ][ name ][ 0 ]
        input_enable  = json_data [ 'Name' ][ name ][ 1 ]
        input_disable = json_data [ 'Name' ][ name ][ 2 ]
        input_id      = json_data [ 'Name' ][ name ][ 3 ]

        Names_list_options += [ JSON.FormatHTML.option_text  ( name , input_enable , input_disable ) ]

        if not name == 'None' : Actions_dict [ name ] = [ input_cmd , input_enable , input_disable , input_id ]

    da_ritorno [ 'text' ]  = JSON.FormatHTML.start_page
    da_ritorno [ 'text' ] += JSON.FormatHTML.complete_select ( 'Name' , 6 , Names_list_options , True )
    da_ritorno [ 'text' ] += JSON.FormatHTML.end_Names

    # --------------------------------------------------------------

    Actions = json_data [ 'Actions' ].keys ()
    Actions_inner_col = ''
    for action in Actions :

        Action_list_options = []
        for option in list ( json_data [ 'Actions' ][ action ].keys () ) :

            input_cmd     = json_data [ 'Actions' ][ action ][ option ][ 0 ]
            input_enable  = json_data [ 'Actions' ][ action ][ option ][ 1 ]
            input_disable = json_data [ 'Actions' ][ action ][ option ][ 2 ]
            input_id      = json_data [ 'Actions' ][ action ][ option ][ 3 ]

            Action_list_options += [ JSON.FormatHTML.option_text  (  option , input_enable , input_disable ) ]

            if not option == 'None' : Actions_dict [ option ] = [ input_cmd , input_enable , input_disable , input_id ]
        
        ActionSelect = JSON.FormatHTML.complete_select ( action , 8 , Action_list_options , True )

        Actions_inner_col += ( '' if Actions_inner_col == '' else '\n' ) + ActionSelect

    da_ritorno [ 'text' ] += JSON.FormatHTML.start_form_group
    da_ritorno [ 'text' ] += JSON.FormatHTML.class_row ( Actions_inner_col )
    da_ritorno [ 'text' ] += JSON.FormatHTML.end_form_group
    
    # --------------------------------------------------------------

    da_ritorno [ 'text' ] += " <script> "
    da_ritorno [ 'text' ] += " var groups = {} ; "

    group_id = 0
    Groups_dict = {}
    for group_name in json_data [ 'Groups' ].keys () :

        group_id  = group_id + 1
        group_can = json_data [ 'Groups' ][ group_name ]
        Groups_dict [ group_name ] = [ group_id , group_can ]

        da_ritorno [ 'text' ] += " groups [ '{}' ] = '{}' ; ".format ( group_name , group_can )
    da_ritorno     [ 'text' ] += " </script> "

    SQLdb.default.create ( )
    SQLdb.default.clean  ( )
    SQLdb.default.reset  ( Actions_dict , Groups_dict )

    # --------------------------------------------------------------
    
    builtBaseModel.buildit ( JSON_content )

    return da_ritorno

def saveHTMLasShell ( input_file ) :

    JSON_content = takeJSONfile ( input_file )

    transmuted_dictionary = transmuteJSONintoHTML ( JSON_content )

    file_shell = open ( './static/pages/shell.html' , 'w' )

    file_shell.write ( transmuted_dictionary [ 'text' ] )
    file_shell.close ()
    
    return True
