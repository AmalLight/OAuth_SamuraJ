from flask import Flask, url_for

app = Flask(__name__)

# --------------------------------------------------------

@app.route('/')
def basic():
    return 'a.' # per != appointments ? no only for empty or ///../

@app.route('/appointments/')
def appointment():
    return 'b.' # per less appointments && appointments/... ?
                # no only for /appointments/

@app.route ( '/<path:default>/' ) # considering route collision
def regex_impact ( default ): # per != { empty , appointments }
    return 'c.'

# --------------------------------------------------------

if __name__ == "__main__": app.run( debug=True )