import os
from flask import Flask,send_from_directory
from flask_cors import CORS
from backend.config import SECRET_KEY,MAX_UPLOAD_MB
from backend.db import init_db
from backend.routes.auth_routes import auth_bp
from backend.routes.ticket_routes import ticket_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.device_routes import device_bp
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));FRONT=os.path.join(BASE,"frontend")
app=Flask(__name__,static_folder=os.path.join(FRONT,"static"));app.config["SECRET_KEY"]=SECRET_KEY;app.config["MAX_CONTENT_LENGTH"]=MAX_UPLOAD_MB*1024*1024;CORS(app)
init_db()
app.register_blueprint(auth_bp);app.register_blueprint(ticket_bp);app.register_blueprint(admin_bp);app.register_blueprint(device_bp)
@app.get("/")
def home():return send_from_directory(FRONT,"index.html")
@app.get("/<path:p>")
def page(p):
 return send_from_directory(FRONT,p) if os.path.isfile(os.path.join(FRONT,p)) else send_from_directory(FRONT,"index.html")
@app.get("/api/health")
def health():return {"status":"ok"}
if __name__=="__main__":app.run(debug=True)
