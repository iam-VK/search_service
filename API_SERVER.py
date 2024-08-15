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
                    "method":"[POST]",
                    "parameters": {
                        "search":"search query"
                    }
                }
            }
        }

@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        search_result = query_parser(search_query)  
        search_result["search_query"] = search_query
        print("Search: ",search_query)

        return search_result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, use_reloader = True)