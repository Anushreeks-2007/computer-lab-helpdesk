from flask import Blueprint,request,jsonify
from backend.auth import login_required,role_required
from backend.db import get_db
from backend.services.priority_service import predict_priority
ticket_bp=Blueprint("tickets",__name__,url_prefix="/api/tickets")
@ticket_bp.get("")
@login_required
def tickets(u):
 c=get_db()
 if u["role"] in ("admin","technician"):
  r=c.execute("SELECT t.*,u.name reporter,d.device_number,l.name lab_name,a.name technician FROM tickets t JOIN users u ON u.id=t.user_id LEFT JOIN devices d ON d.id=t.device_id LEFT JOIN labs l ON l.id=d.lab_id LEFT JOIN users a ON a.id=t.assigned_to ORDER BY t.id DESC").fetchall()
 else:r=c.execute("SELECT t.*,d.device_number,l.name lab_name,a.name technician FROM tickets t LEFT JOIN devices d ON d.id=t.device_id LEFT JOIN labs l ON l.id=d.lab_id LEFT JOIN users a ON a.id=t.assigned_to WHERE t.user_id=? ORDER BY t.id DESC",(u["id"],)).fetchall()
 c.close();return jsonify([dict(x) for x in r])
@ticket_bp.post("")
@login_required
def create(u):
 d=request.get_json() or {};desc=d.get("description","").strip()
 if not desc:return jsonify({"error":"Description is required"}),400
 cat=d.get("category","Hardware");pri=d.get("priority") or predict_priority(cat,desc);c=get_db()
 cur=c.execute("INSERT INTO tickets(user_id,device_id,category,description,priority,status) VALUES(?,?,?,?,?,'Open')",(u["id"],d.get("device_id"),cat,desc,pri))
 tid=cur.lastrowid;no=f"CL{1000+tid}";c.execute("UPDATE tickets SET ticket_no=? WHERE id=?",(no,tid))
 c.execute("INSERT INTO ticket_history(ticket_id,new_status,changed_by,note) VALUES(?,?,?,?)",(tid,"Open",u["id"],"Ticket created"));c.commit();c.close()
 return jsonify({"message":"Ticket created","ticket_no":no,"priority":pri}),201
@ticket_bp.patch("/<int:tid>/assign")
@login_required
@role_required("admin")
def assign(u,tid):
 d=request.get_json() or {};c=get_db();c.execute("UPDATE tickets SET assigned_to=?,assigned_at=CURRENT_TIMESTAMP,status='Assigned' WHERE id=?",(d.get("technician_id"),tid));c.commit();c.close();return jsonify({"message":"Ticket assigned"})
@ticket_bp.patch("/<int:tid>/status")
@login_required
def status(u,tid):
 d=request.get_json() or {};s=d.get("status");allowed={"Assigned","In Progress","Resolved","Closed"}
 if s not in allowed:return jsonify({"error":"Invalid status"}),400
 c=get_db();old=c.execute("SELECT status,assigned_to FROM tickets WHERE id=?",(tid,)).fetchone()
 if not old:c.close();return jsonify({"error":"Ticket not found"}),404
 if u["role"]=="technician" and old["assigned_to"] not in (None,u["id"]):c.close();return jsonify({"error":"Not assigned to you"}),403
 c.execute("UPDATE tickets SET status=?,resolution_note=COALESCE(NULLIF(?,'') ,resolution_note),resolved_at=CASE WHEN ?='Resolved' THEN CURRENT_TIMESTAMP ELSE resolved_at END,closed_at=CASE WHEN ?='Closed' THEN CURRENT_TIMESTAMP ELSE closed_at END WHERE id=?",(s,d.get("resolution_note",""),s,s,tid))
 c.execute("INSERT INTO ticket_history(ticket_id,old_status,new_status,changed_by,note) VALUES(?,?,?,?,?)",(tid,old["status"],s,u["id"],d.get("resolution_note","")));c.commit();c.close();return jsonify({"message":"Status updated"})
