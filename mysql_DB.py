import mysql.connector

'''
mysqldump -u groot -p search_engine videos categories video_categories > "D:\\Code Space\\Projects\\Video Transcription\\SETUP\\DB_Backup.sql"
'''

db = mysql.connector.connect(
    host="localhost", # "db" for docker | # "localhost" for non docker execution
    user="groot",
    password="iamgroot",
    database = "search_engine"
)

def search_video(search_tag:str):
    try:
        dbcursor = db.cursor()
        query = f"select file_path,file_name,category_name from search_engine.video_index where category_name like '%{search_tag}%';"
        dbcursor.execute(query)
        db_result=dbcursor.fetchall()
        dbcursor.close()
        search_results = []

        if db_result:
            for item in db_result:
                path, file_name, category_list = item
                search_result = {
                    "file_path": path,
                    "file_name": file_name,
                    "category_list": category_list
                }
                if file_name not in (result["file_name"] for result in search_results):
                    search_results.append(search_result)
            
            
            return {
                "status": "SUCCESS",
                "tag": search_tag,
                "total_results": len(search_results),
                "results": search_results
            }
        
        else:
            print("$$ No match Found")
            return {"status": "NO_MATCH"}

    except mysql.connector.Error as error:
        print("$$ Error Searching video from Video_Index:", error)
        return {
            "status": "ERROR",
            "error": error
            }
