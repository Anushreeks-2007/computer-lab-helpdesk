import os,joblib
m=joblib.load(os.path.join(os.path.dirname(__file__),"priority_model.joblib"))
print(m.predict(["computer is not booting before exam"])[0])
