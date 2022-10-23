all of information about this work :)

## About this data
Here we provide our dataset for multi-label hate speech and abusive language detection in the Indonesian Twitter. The main dataset can be seen at **re_dataset** with labels information as follows:
* **HS** : hate speech label;
* **Abusive** : abusive language label;
* **HS_Individual** : hate speech targeted to an individual;
* **HS_Group** : hate speech targeted to a group;
* **HS_Religion** : hate speech related to religion/creed;
* **HS_Race** : hate speech related to race/ethnicity;
* **HS_Physical** : hate speech related to physical/disability;
* **HS_Gender** : hate speech related to gender/sexual orientation;
* **HS_Gender** : hate related to other invective/slander;
* **HS_Weak** : weak hate speech;
* **HS_Moderate** : moderate hate speech;
* **HS_Strong** : strong hate speech.

For each label, `1` means `yes` (tweets including that label), `0` mean `no` (tweets are not included in that label). 


## Data Used 
* abusive.csv
* data.csv
* new_kamusalay.csv

## Code Used
* cleansing.py          : save all function that used for cleansing data
* most_word.ipynb       : to see the total number of abusive words especially top 10 abusive word
* report_gold_challenge.ipyb : information about all report (pie chart, bar chart) for each sentence
* see_database.ipyb     : CRUD about DATABASE used to STORE TEXT or TWEET 
* swagger.py            : code API to launch program 