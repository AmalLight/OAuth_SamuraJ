
def label_text ( input_name ) : return '<label > {} </label>' .format ( input_name )

def small_text ( input_ads  ) :

    return """<small class="form-text text-muted" >
      {}
    </small>""".format ( input_ads )

def option_text ( input_detail , input_list_enble , input_list_disable ) :

    return '<option id={} class=d-block value={} > {} </option>'.format ( input_list_enble + '_' + input_list_disable , input_detail , input_detail )

# -----------------------------------------------------------

def class_row ( inner_col ) :
    return """
    <div class=row >
      {}
    </div>
""".      format ( inner_col )

def col_auto ( inner_select ) :
      return """
      <div class=col-auto >
        {}
      </div>
""".        format ( inner_select )


def complete_select ( input_name , input_number , list_inner_options , col_auto_bool=False ) :

    da_ritorno = ( ( (  " " * input_number ) if not col_auto_bool else '' ) +

        label_text ( input_name ) + ' <br> \n' + " " * input_number +

        '<select class=form-select id={} onchange="disable()" >'.format ( input_name ) +
        
        ( '\n' + " " * ( input_number + 2 ) ) +
        ( '\n' + " " * ( input_number + 2 ) ).join ( list_inner_options ) +
        ( '\n' + " " *   input_number       ) +

        '</select>' )

    if col_auto_bool: return col_auto ( da_ritorno )
    else:             return            da_ritorno

# -----------------------------------------------------------
# -----------------------------------------------------------

start_page = """
<div id=space></div><div id=space></div>
<form>
  <div class=form-group >
"""

end_Names = """
    {}
  </div>
  <div id=space></div>
  <div id=space></div>
  <div id=space></div>
""".                  format ( small_text ( "Machine's Name you are pointing for ." ) )

# -----------------------------------------------------------

start_form_group = """

  <div class="form-group">
    {} <br>
    {} <br>
    <div id=space></div>
""".                    format (

    label_text ( 'Actions From Selects' ) ,
    small_text ( 'You can Select Here additional Commands to execute on Machine you are pointing for .' )
)

end_form_group = """
  </div>
  <div id=space></div>
  <div id=space></div>
  <div id=space></div>

  <a class="btn btn-primary" onClick="submitParamiko()" href='#' > Submit </a>
</form>
<div id=space></div><div id=space></div>"""
