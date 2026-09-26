import sqlite3,os
from backend.config import DATABASE_PATH
def get_db():
 os.makedirs(os.path.dirname(DATABASE_PATH),exist_ok=True)
 c=sqlite3.connect(DATABASE_PATH); c.row_factory=sqlite3.Row; c.execute("PRAGMA foreign_keys=ON"); return c
def init_db():
 c=get_db()
 with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"database","schema.sql"),encoding="utf-8") as f:c.executescript(f.read())
 from werkzeug.security import generate_password_hash
 users=[("Admin","admin@lab.local",generate_password_hash("admin123"),"admin"),
 ("Ravi Technician","ravi@lab.local",generate_password_hash("ravi123"),"technician"),
 ("Student Demo","student@lab.local",generate_password_hash("student123"),"student")]
 for u in users:c.execute("INSERT OR IGNORE INTO users(name,email,password,role) VALUES(?,?,?,?)",u)
 for l in [("CSE Lab 1","Block A"),("CSE Lab 2","Block A"),("ECE Lab","Block B")]:
  c.execute("INSERT OR IGNORE INTO labs(name,location) VALUES(?,?)",l)
 for l in c.execute("SELECT id FROM labs").fetchall():
  if c.execute("SELECT COUNT(*) n FROM devices WHERE lab_id=?",(l["id"],)).fetchone()["n"]==0:
   for i in range(1,11):c.execute("INSERT INTO devices(lab_id,device_number,device_type,specifications,status) VALUES(?,?,?,?,?)",(l["id"],f"PC-{i:02d}","PC","Core i5 | 16 GB RAM | 512 GB SSD","Working"))
 c.commit();c.close()
