from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/' + os.environ['SECRET'], methods=['POST'])
def solution_check():
    submitted_solution = request.json['solution']
    
    if submitted_solution != "OUR_PHP_USES_ROT13_FOR_MAXIMUM_SECURITY":
         return jsonify(solved=False)
         
    return jsonify(solved=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=False)
