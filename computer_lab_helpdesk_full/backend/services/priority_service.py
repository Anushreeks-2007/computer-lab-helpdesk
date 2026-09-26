import os,joblib
MODEL=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"ml_model","priority_model.joblib")
def rule_based_priority(category,description):
 t=(category+" "+description).lower()
 if any(x in t for x in ["fire","smoke","spark","electric shock","server down","network down","exam","not booting"]):return "High"
 if any(x in t for x in ["printer","internet","login","crash","blue screen","overheating"]):return "Medium"
 return "Low"
def predict_priority(category,description):
 if not os.path.exists(MODEL):return rule_based_priority(category,description)
 try:return str(joblib.load(MODEL).predict([category+" "+description])[0])
 except Exception:return rule_based_priority(category,description)
