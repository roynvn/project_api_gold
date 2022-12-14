import json
from unittest import result
from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
import re
import pandas as pd

#import function cleansing
from cleansing import *

#import db
import sqlite3 as sq

app = Flask(__name__) #deklarasi Flask
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Indonesian Abusive and Hate Speech Twitter Text'),
    'version': LazyString(lambda: '1'),
    'description': LazyString(lambda: 'merupakan API khususnya untuk melakukan CLEANSING data pada https://www.kaggle.com/datasets/ilhamfp31/indonesian-abusive-and-hate-speech-twitter-text'),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

#swagger form
@swag_from("swagger_config_form.yml", methods = ['POST'])
@app.route('/post_form/v1',methods = ['POST'])
def post_form():

    result_before = request.form["text"]
    result_after = replace_ascii(result_before)
    result_after = remove_special_char(result_after)
    result_after = remove_punctuation(result_after)
    result_after = remove_whitespace_LT(result_after)
    result_after = remove_whitespace_multiple(result_after) 
    df_result = pd.DataFrame(columns=['Before','After']).assign(Before = [result_before],After = [result_after])
 
    #create and insert into db 
    conn = sq.connect("STORE_TEXT.db")
    df_result.to_sql('TEXT_DATA', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()
    return jsonify({"hasil input: ":result_after})


#swagger file
@swag_from("swagger_config_file.yml",methods =['POST'])
@app.route("/post_file/v1",methods =['POST'])
def post_file():
    file = request.files["file"]
    df = pd.read_csv(file, encoding='latin-1')
    #df = pd.DataFrame(df['Tweet'])

    #cleansing
    #case fold 
    df['Tweet_Clean'] = df['Tweet'].str.lower()
    #replace ascii
    df['Tweet_Clean'] = df['Tweet_Clean'].apply(replace_ascii)
    #remove special
    df['Tweet_Clean'] = df['Tweet_Clean'].apply(remove_special_char)
    #remove_punctuation
    df['Tweet_Clean']= df['Tweet_Clean'].apply(remove_punctuation)
    #remove whitespace leading & trailing
    df['Tweet_Clean']= df['Tweet_Clean'].apply(remove_whitespace_LT)
    #remove multiple whitespace into single whitespace
    df['Tweet_Clean'] = df['Tweet_Clean'].apply(remove_whitespace_multiple)
    # remove single char
    df['Tweet_Clean']= df['Tweet_Clean'].apply(remove_single_char)
    #hapus url
    df['Tweet_Clean'] = df['Tweet_Clean'].apply(remove_urls)
    #df_tweet = pd.DataFrame().assign(Before=df['Tweet'], After=df['Tweet_Clean'])
    
    #import ke db
    #data = df_tweet
    data = df
    sql_data = 'STORE_TWEET.db' #- Creates DB names SQLite
    conn = sq.connect(sql_data)
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS TWEET_DATA''')
    data.to_sql('TWEET_DATA', conn, if_exists='replace', index=False) # - writes the df to SQLIte DB
    conn.commit()
    conn.close()

    return jsonify({"RESULT": "SUCCESSFUL TO CREATE DB"})

if __name__ == "__main__":
    app.run(port=1234, debug=True) #debug => kode otomatis update ketika ada perubahan