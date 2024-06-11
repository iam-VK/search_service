from flask import Flask, request
from flask_cors import CORS
import requests
from mysql_DB import search_video

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        search_result = search_video(search_query)  
        print(search_query)
        # if search_result['status'] == "SUCCESS": 
        #     url = 'http://localhost:5004/get_video'
        #     post_data = {'file_path': search_result['file_path'], 
        #                 'file_name': search_result['file_name']}
        #     post_response = requests.post(url, json=post_data)
        #     print("Response from Media_Files_DB: ",post_response)
        #     return {"status":"SUCCESS"}
        
        return search_result ## temp
    
    return {
        "status":"ERROR",
        "request_method":request.method,
        "description":f"{request.method} methods not accepted."
        }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, use_reloader = True)