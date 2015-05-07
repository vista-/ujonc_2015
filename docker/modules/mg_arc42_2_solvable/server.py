from flask import Flask, jsonify, request
import os
import subprocess
import binascii

app = Flask(__name__)

@app.route('/')
def index():
    result = ''
    text = binascii.unhexlify(request.args.get('text', ''))
    if text:
        result = subprocess.check_output(['setarch', 'x86_64', '-R', './arc42_v2', 'READING_GLOBALS_IS_EASY', text], stderr=subprocess.STDOUT, env={})
        result = result.replace('\n', '<br>') + '<br><br>'

    return b"""<!DOCTYPE html>
    <html>
    <head><title>ARC42 encrypter</title></head>
    <body>
    %s
    <form action="/" method="GET">
    <input name="text" id="text" value="%s">
    <input type="submit" value="Encrypt!" onclick="text.value = text.value.split('').map(function(x) {return x.charCodeAt(0).toString(16)}).join('')">
    </form>
    </body>
    </html>
    """ % (result, text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)
