from flask import Blueprint,request,jsonify
from backend.auth import login_required,role_required
from backend.db import get_db
device_bp=Blueprint("devices",__name__,url_prefix="/api/devices")
@device_bp.get("")
@login_required
def all_devices(u):
 c=get_db();r=c.execute("SELECT d.*,l.name lab_name FROM devices d JOIN labs l ON l.id=d.lab_id ORDER BY l.name,d.device_number").fetchall();c.close();return jsonify([dict(x) for x in r])
@device_bp.post("")
@login_required
@role_required("admin")
def add(u):
 d=request.get_json() or {};c=get_db();c.execute("INSERT INTO devices(lab_id,device_number,device_type,specifications,status) VALUES(?,?,?,?,?)",(d.get("lab_id"),d.get("device_number"),d.get("device_type","PC"),d.get("specifications",""),d.get("status","Working")));c.commit();c.close();return jsonify({"message":"Device added"}),201
