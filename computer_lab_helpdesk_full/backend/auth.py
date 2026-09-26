from functools import wraps
from flask import request,jsonify
import jwt
from backend.config import JWT_SECRET_KEY
from backend.db import get_db
def create_token(u):return jwt.encode({"user_id":u["id"],"role":u["role"]},JWT_SECRET_KEY,algorithm="HS256")
def current_user():
 a=request.headers.get("Authorization","")
 if not a.startswith("Bearer "):return None
 try:
  p=jwt.decode(a[7:],JWT_SECRET_KEY,algorithms=["HS256"]);c=get_db()
  u=c.execute("SELECT id,name,email,role FROM users WHERE id=?",(p["user_id"],)).fetchone();c.close()
  return dict(u) if u else None
 except Exception:return None
def login_required(fn):
 @wraps(fn)
 def w(*args,**kwargs):
  u=current_user()
  if not u:return jsonify({"error":"Authentication required"}),401
  return fn(u,*args,**kwargs)
 return w
def role_required(*roles):
 def d(fn):
  @wraps(fn)
  def w(u,*args,**kwargs):
   if u["role"] not in roles:return jsonify({"error":"Insufficient permissions"}),403
   return fn(u,*args,**kwargs)
  return w
 return d
