import os,pandas as pd,joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
BASE=os.path.dirname(__file__);df=pd.read_csv(os.path.join(BASE,"training_data.csv"));X=df.text.fillna("");y=df.priority
a,b,c,d=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
m=Pipeline([("tfidf",TfidfVectorizer(ngram_range=(1,2))),("clf",RandomForestClassifier(n_estimators=200,random_state=42,class_weight="balanced"))]);m.fit(a,c);print(classification_report(b,m.predict(b),zero_division=0));joblib.dump(m,os.path.join(BASE,"priority_model.joblib"))
