import os
import cgi
import lxml
import lxml.objectify
import simplejson as json
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    xml = request.form['xml'] if request.method == 'POST' else '<a><b><c>123</c><d>456</d></b></a>'
    json = objectJSONEncoder().encode(lxml.objectify.fromstring(xml)) if request.method == 'POST' else ''
    
    return """<!doctype html>
    <html>
    <head>
    </head>
    <body>
    <h1>An open source XML to JSON converter</h1>
    <form action="" method="POST">
        <textarea name="xml" cols="120" rows="30">%s</textarea><br>
        <input type="submit">
    </form>
    <pre>%s</pre>
    <h2>Source code:</h2>
    <pre>%s</pre>
    </body>
    </html>
    """ % (cgi.escape(xml), cgi.escape(json), cgi.escape(open(__file__).read()))

@app.route('/flag', methods=['GET'])
def flag():
    #return cgi.escape(open('flag').read())
    return ''

class objectJSONEncoder(json.JSONEncoder):
    """Source: http://stackoverflow.com/questions/471946/how-to-convert-xml-to-json-in-python
    A specialized JSON encoder that can handle simple lxml objectify types
    >>> from lxml import objectify
    >>> obj = objectify.fromstring("<Book><price>1.50</price><author>W. Shakespeare</author></Book>")       
    >>> objectJSONEncoder().encode(obj)
    '{"price": 1.5, "author": "W. Shakespeare"}'       
    """
    def default(self,o):
        if isinstance(o, lxml.objectify.IntElement):
            return int(o)
        if isinstance(o, lxml.objectify.NumberElement) or isinstance(o, lxml.objectify.FloatElement):
            return float(o)
        if isinstance(o, lxml.objectify.ObjectifiedDataElement):
            return str(o)
        if hasattr(o, '__dict__'):
            #For objects with a __dict__, return the encoding of the __dict__
            return o.__dict__
        return json.JSONEncoder.default(self, o)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)


