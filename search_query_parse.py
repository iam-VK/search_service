import spacy
######python -m spacy download en_core_web_sm
from mysql_DB import search_video
from elastic import search_elastic

nlp = spacy.load("en_core_web_sm")

def extract_tags(query):
    doc = nlp(query)
    tags=[]
    media_type = None
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            if token.lemma_ in ["picture", "video"]:
                media_type = token.lemma_
                continue
            tags.append(token.lemma_)
            
    return media_type,tags

def check_operators(query):
    query_lower = query.lower()
    if " and " in query_lower:
        return True
    elif " or " in query_lower:
        return True
    return False

def split_operators(query):
    query_lower = query.lower()
    if " and " in query_lower:
        parts = query_lower.split(" and ")
        operator  = "and"

    elif " or " in query_lower:
        parts = query_lower.split(" or ")
        operator = "or"

    else:
        return None
    return parts,operator

def query_parser(query):
    # query = "get pictures of dogs in beach and also mountains with birthday party"

    # parts,operator = split_operators(query)
    media_type, query_tag = extract_tags(query)
    hit_tags = []+query_tag
    
    search_results = []
    result_vid_ids = set()

    for tag in query_tag:
        db_results = search_video(tag)
        elastic_results = search_elastic(tag)
        mysql_result = []
        elastic_result = []

        elastic_flag, mysql_flag = False, False
        if db_results["hits"] > 0:
            mysql_result = db_results["mysql_results"]
            
            if len(mysql_result)>0:
                mysql_flag = True
                for result in mysql_result:
                    if result["video_id"] not in result_vid_ids:
                        result_vid_ids.add(result["video_id"])
                        result['matching_tags'] = [result['search_tag']]
                        del result['search_tag']
                        search_results.append(result)

                    elif result["video_id"] in result_vid_ids:
                        for ele in search_results:
                            if result["video_id"] == ele["video_id"]:

                                if result['search_tag'] not in ele['matching_tags']:
                                    ele['matching_tags'].append(result['search_tag'])

                                if ele['match_type'] == 'speech':
                                    ele['match_type'] = 'vsn-sph'
                                
                                if 'category_list' in ele:
                                    if ele["category_list"] not in result["category_list"]:
                                        ele["category_list"] += result["category_list"]
                                elif 'category_list' not in ele:
                                    ele['category_list'] = result['category_list']


        if elastic_results['hits'] > 0:
            elastic_result = elastic_results["elastic_results"]

            if len(elastic_result)>0:
                elastic_flag = True
                for result in elastic_result:
                    if result["video_id"] not in result_vid_ids:
                        result_vid_ids.add(result["video_id"])
                        result['matching_tags'] = [result['search_tag']]
                        del result['search_tag']
                        search_results.append(result)

                    elif result["video_id"] in result_vid_ids:
                        for ele in search_results:
                            if result["video_id"] == ele["video_id"]:

                                if result['search_tag'] not in ele['matching_tags']:
                                    ele['matching_tags'].append(result['search_tag'])

                                if ele['match_type'] == 'vision':
                                    ele['match_type'] = 'vsn-sph'
    
        if not elastic_flag and not mysql_flag:
            print("NO Match: ", tag)
            hit_tags.remove(tag)
        
    return {
                "status": "SUCCESS",
                "total_results": len(search_results),
                "search_query": query,
                "extracted_tags": query_tag,
                "hitting_tags":hit_tags,
                "results": search_results
            }


# print(query_parser("a racing truck was hit by the police and the driver ran off"))