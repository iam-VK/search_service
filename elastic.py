from elasticsearch import Elasticsearch
import os

client = Elasticsearch(
  "https://localhost:9200/",
  api_key="N2l1TUlwSUJTMWxfTmtUOGlpR1M6cThDOVNGTEJUNXVwZ2VzY2t2OG4tdw==",
  verify_certs=False,
  ssl_show_warn=False
)

def file_name_extract(file_path):
    file_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(file_name)
    return file_name, file_name_without_extension

def search_elastic(search_tag):
    elastic_query = {'query': {'match': {'transcription': search_tag}}}
    resp = client.search(index="transcription-index", body=elastic_query)

    total_hits = resp['hits']['total']['value']

    elastic_results = []

    if total_hits > 0:
        for hit in resp['hits']['hits']:
          file_id = hit['_source']['video_id'] ##change video_id to file_id in elastic search db
          file_name = hit['_source']['file_name']
          _, file_name = file_name_extract(file_name)
          
          result = {
                      "search_tag": search_tag,
                      "file_id": file_id,
                      "file_name": file_name,
                      "match_type":"speech"
                  }
        elastic_results.append(result)

        return {
                "status":"SUCCESS",
                "tag":search_tag,
                "hits":total_hits,
                "elastic_results":elastic_results
                }
    
    return {"elastic_results":{"search_tag":search_tag,
                               "speech_hit":False},
            "hits":total_hits
                }