from flask import Flask, url_for , request , g , send_from_directory , session
import random , os.path

# g is global ?

# --------------------------------------------------------

def dump_request_detail ( request ):

    request_detail = """ # Before Request #
request.endpoint:   {request.endpoint}
request.method:     {request.method}
request.view_args:  {request.view_args}
request.args:       {request.args}
request.form:       {request.form}
request.user_agent: {request.user_agent}
request.files:      {request.files}
"""
    # request_detail += 'request.is_xhr: {request.is_xhr}'

    request_detail += """ # Headers #
{request.headers}
"""
    return request_detail.format ( request = request ).strip()

# --------------------------------------------------------

app = Flask ( __name__ , static_folder=None )

@app.route ( '/static/sensible/<path:filename>' )
def assets ( filename ):
    return send_from_directory ( 'static/sensible' , filename )

# --------------------------------------------------------

@app.before_request
def callme_before_every_request():
    app.logger.debug('\n\n')
    id_g = ''
    for i in range ( 9 ): id_g += str ( random.randint(0, 9) )
    app.logger.debug('Before request id: {}'.format(id_g))
    app.logger.debug(dump_request_detail(request))
    g.id_g = id_g

@app.after_request
def callme_after_every_response(response):
    app.logger.debug('After Request #\n' + repr(response))
    app.logger.debug('after request id: {g.id_g}'.format(g=g))
    app.logger.debug('\n\n')
    return response

# --------------------------------------------------------

@app.errorhandler(404)
def error_not_found(error):
    return send_from_directory ('error' , '404.html') , 404

@app.route ( '/' )
def basic ():
    return 'a.' # per != appointments ? no only for empty or ///../

@app.route ( '/<path:default>/' ) # considering route collision
def regex_impact ( default ): # per != { empty , appointments }
    return 'b.'

# --------------------------------------------------------

if __name__ == "__main__": app.run( debug=True )
