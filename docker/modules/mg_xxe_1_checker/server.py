from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/' + os.environ['SECRET'], methods=['POST'])
def solution_check():
    submitted_solution = request.json['solution']
    
    if submitted_solution != "XML_IS_LIKE_VIOLENCE__IF_IT_DOESNT_SOLVE_YOUR_PROBLEM_YOU_ARE_NOT_USING_ENOUGH_OF_IT":
         return jsonify(solved=False)
         
    return jsonify(solved=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=False)
