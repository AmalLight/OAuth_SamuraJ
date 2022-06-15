import json , os , sys , JSON.FormatHTML

def takeJSONfile ( input_file ) :

    with open ( input_file , 'r' ) as f : return f.read ()
    return ''

def transmuteJSONintoHTML ( JSON_content ) :

    da_ritorno                = {}
    da_ritorno [ 'text'     ] = ''
    da_ritorno [ 'commands' ] = {}

    json_data = json.loads ( JSON_content )

    Names_list_options = []
    for detail in json_data [ 'Name' ].keys () :

        input_enable  = json_data [ 'Name' ][ detail ][ 1 ]
        input_disable = json_data [ 'Name' ][ detail ][ 2 ]

        Names_list_options += [ JSON.FormatHTML.option_text ( detail , input_enable , input_disable ) ]

    da_ritorno [ 'text' ]  = JSON.FormatHTML.start_page
    da_ritorno [ 'text' ] += JSON.FormatHTML.complete_select ( 'Name' , 6 , Names_list_options , True )
    da_ritorno [ 'text' ] += JSON.FormatHTML.end_Names

    Actions = json_data [ 'Actions' ].keys ()

    Actions_inner_col = ''
    for action in Actions :

        input_detail_list = [ option for option in list ( json_data [ 'Actions' ][ action ].keys () ) ]

        Action_list_options = []
        for detail in input_detail_list :

            input_enable  = json_data [ 'Actions' ][ action ][ detail ][ 1 ]
            input_disable = json_data [ 'Actions' ][ action ][ detail ][ 2 ]

            Action_list_options += [ JSON.FormatHTML.option_text ( detail , input_enable , input_disable ) ]
        
        ActionSelect = JSON.FormatHTML.complete_select ( action , 8 , Action_list_options , True )

        Actions_inner_col += ( '' if Actions_inner_col == '' else '\n' ) + ActionSelect

    da_ritorno [ 'text' ] += JSON.FormatHTML.start_form_group
    da_ritorno [ 'text' ] += JSON.FormatHTML.class_row ( Actions_inner_col )
    da_ritorno [ 'text' ] += JSON.FormatHTML.end_form_group

    da_ritorno [ 'commands' ] = json_data
    return da_ritorno

def saveHTMLasShell ( input_file ) :

    JSON_content = takeJSONfile ( input_file )

    transmuted_dictionary = transmuteJSONintoHTML ( JSON_content )

    file_shell = open ( './static/pages/shell.html' , 'w' )

    file_shell.write ( transmuted_dictionary [ 'text' ] )
    file_shell.close ()

    return transmuted_dictionary [ 'commands' ]
