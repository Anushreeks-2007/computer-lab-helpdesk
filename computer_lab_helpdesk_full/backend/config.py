import os
from dotenv import load_dotenv
load_dotenv()
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH=os.getenv("DATABASE_PATH",os.path.join(BASE_DIR,"database","helpdesk.db"))
SECRET_KEY=os.getenv("SECRET_KEY","dev-secret")
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY","dev-jwt-secret")
MAX_UPLOAD_MB=int(os.getenv("MAX_UPLOAD_MB","5"))
