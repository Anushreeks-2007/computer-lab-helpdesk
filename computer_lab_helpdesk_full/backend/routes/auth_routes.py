from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash
from backend.db import get_db
from backend.auth import create_token
auth_bp=Blueprint("auth",__name__,url_prefix="/api/auth")
@auth_bp.post("/login")
def login():
 d=request.get_json() or {};c=get_db();u=c.execute("SELECT * FROM users WHERE email=?",(d.get("email",""),)).fetchone();c.close()
 if not u or not check_password_hash(u["password"],d.get("password","")):return jsonify({"error":"Invalid email or password"}),401
 return jsonify({"token":create_token(u),"user":{"id":u["id"],"name":u["name"],"email":u["email"],"role":u["role"]}})
