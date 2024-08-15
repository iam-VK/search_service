import spacy
######python -m spacy download en_core_web_sm
from mysql_DB import search_video

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
    
    search_results = []
    for tag in query_tag:
        print(tag)
        db_results = search_video(tag)
        if db_results["status"] == "SUCCESS":
            search_results.append(db_results["results"][0])
        else:
            print("NO Match for: ", tag) 
            query_tag.remove(tag)


    return {
                "status": "SUCCESS",
                "tags": query_tag,
                "total_results": len(search_results),
                "results": search_results
            }

# print(query_parser("show videos of foods and swimming"))