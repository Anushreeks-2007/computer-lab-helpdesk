from flask import Blueprint,jsonify
from backend.auth import login_required,role_required
from backend.db import get_db
admin_bp=Blueprint("admin",__name__,url_prefix="/api/admin")
@admin_bp.get("/dashboard")
@login_required
@role_required("admin")
def dashboard(u):
 c=get_db();stats={}
 for k,q in {"total":"SELECT COUNT(*) n FROM tickets","open":"SELECT COUNT(*) n FROM tickets WHERE status='Open'","progress":"SELECT COUNT(*) n FROM tickets WHERE status='In Progress'","resolved":"SELECT COUNT(*) n FROM tickets WHERE status IN ('Resolved','Closed')","repair":"SELECT COUNT(*) n FROM devices WHERE status='Under Repair'"}.items():stats[k]=c.execute(q).fetchone()["n"]
 cats=[dict(x) for x in c.execute("SELECT category,COUNT(*) count FROM tickets GROUP BY category").fetchall()];c.close();return jsonify({"stats":stats,"categories":cats})
