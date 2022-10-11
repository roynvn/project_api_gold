import json
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

"""
def _remove_punct(s):
    return re.sub(r"[^\w\d\s]+", "",s)

@swag_from("swagger_config_post.yml", methods=['POST'])
@app.route("/clean_text/v1", methods=['POST']) 
def remove_punct_post():
    s = request.get_json()
    non_punct = _remove_punct(s['text'])
    return jsonify({"hasil_bersih":non_punct})

@swag_from("swagger_config.yml", methods=['GET'])
@app.route("/get_text/v1", methods=['GET']) #ini adalah decorator
def return_text():
    name_input = request.args.get('name')
    nohp_input = request.args.get('nomerhp')
    return_text = {
        "text":f"halo semuanyaa!!! nama saya adalah {name_input}",
        "no_hape":nohp_input
    }
    return jsonify(return_text) #return dalam bentuk JSON
"""

@swag_from("swagger_config_form.yml", methods = ['POST'])
@app.route('/post_form/v1',methods = ['POST'])
def post_form():
    result = request.form["text"]
    print(type(result))
    result = replace_ascii(result)
    result = remove_special_char(result)
    result = remove_punctuation(result)
    result = remove_whitespace_LT(result)
    result = remove_whitespace_multiple(result) 
    """
    result = replace_ascii(result["text"])
    result = remove_special_char(result["text"])
    result = remove_punctuation(result["text"])
    result = remove_whitespace_LT(result["text"])
    result = remove_whitespace_multiple(result["text"]) 
    """
    return jsonify({"hasil input: ":result})

@swag_from("swagger_config_file.yml",methods =['POST'])
@app.route("/post_file/v1",methods =['POST'])
def post_file():
    file = request.files["file"]
    df = pd.read_csv(file, encoding='latin-1')
    df = pd.DataFrame(df['Tweet'])

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
    df_tweet = pd.DataFrame().assign(Before=df['Tweet'], After=df['Tweet_Clean'])
    
    #import ke db
    data = df_tweet
    sql_data = 'TRAINING.db' #- Creates DB names SQLite
    conn = sq.connect(sql_data)
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS TRAINING''')
    data.to_sql('TRAINING', conn, if_exists='replace', index=False) # - writes the pd.df to SQLIte DB
    conn.commit()
    conn.close()

    return jsonify({"halo": str(df['Tweet'][2])})



if __name__ == "__main__":
    app.run(port=1234, debug=True) #debug => kode otomatis update ketika ada perubahan