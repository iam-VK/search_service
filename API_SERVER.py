from flask import Flask, request
from flask_cors import CORS
from search_query_parse import query_parser

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST','GET'])
def service_status():
    return {
        "status":'Alive',
            "endpoints": {
                "/search": {
                    "method":"[GET]",
                    "parameters": {
                        "search":"search query",
                        "file-type":"file type"
                    }
                }
            }
        }

@app.route("/search", methods=['GET'])
def search():
    if request.method == 'GET':
        search_query = request.args.get('query')
        file_type = request.args.get('file-type')
        search_result = query_parser(search_query)

        return search_result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, use_reloader = True)