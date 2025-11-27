# fix_admin.py - Corrige el admin para que funcione el login
import hashlib
from db_connection import get_connection

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

conn = get_connection()
cur = conn.cursor()
cur.execute("UPDATE usuarios SET password=%s WHERE nombre='admin'", (hash_password("admin123"),))
conn.commit()
cur.close()
conn.close()
print("Admin arreglado: usuario=admin, contraseña=admin123")