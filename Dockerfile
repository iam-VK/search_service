FROM python

WORKDIR /app 

COPY API_SERVER.py          \
    mysql_DB.py             \
    requirements.txt        \
    search_query_parse.py   \
    /app/

RUN pip install -r /app/requirements.txt

EXPOSE 5003

CMD python API_SERVER.py