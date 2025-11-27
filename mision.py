# mision.py
from db_connection import get_connection

class Mision:
    TIPOS_VALIDOS = ["busqueda", "suministros", "vigilancia", "mapeo"]

    def __init__(self, id: int, tipo: str, operador_id: int, estado: str = "pendiente"):
        self.id = id
        self.tipo = tipo
        self.operador_id = operador_id
        self.estado = estado

    @classmethod
    def crear(cls, tipo: str, operador_id: int):
        tipo_lower = tipo.strip().lower()
        if tipo_lower not in cls.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Usa: {', '.join(cls.TIPOS_VALIDOS)}")
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO misiones (tipo, operador_id, estado) VALUES (%s, %s, 'en_curso')",
                (tipo_lower, operador_id)
            )
            conn.commit()
            mision_id = cur.lastrowid
            cur.close()
            conn.close()
            return cls(mision_id, tipo_lower, operador_id, "en_curso")
        except Exception as e:
            if cur: cur.close()
            if conn: conn.close()
            raise ValueError(f"Error al crear misión: {str(e)}")

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, tipo, operador_id, estado FROM misiones ORDER BY id DESC")
            rows = cur.fetchall()
            return [cls(row[0], row[1], row[2], row[3]) for row in rows]
        finally:
            cur.close()
            conn.close()

    def completar(self, rescatista_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE misiones 
                SET estado = 'completada', fecha_finalizacion = NOW() 
                WHERE id = %s
            """, (self.id,))
            
            cur.execute("""
                INSERT INTO reportes (mision_id, rescatista_id, observaciones)
                VALUES (%s, %s, %s)
            """, (self.id, rescatista_id, f"Misión completada por rescatista ID {rescatista_id}"))
            
            conn.commit()
        finally:
            cur.close()
            conn.close()
        self.estado = "completada"

    def __str__(self):
        return f"Misión {self.id} | Tipo: {self.tipo.upper()} | Estado: {self.estado.upper()} | Batería: 100% | Prioridad: ALTA"