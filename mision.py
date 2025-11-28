from db_connection import get_connection
from typing import List, Optional


class Mision:
    TIPOS_VALIDOS = ['búsqueda', 'suministros', 'vigilancia', 'mapeo']

    def __init__(self, id: int, tipo: str, drone_id: Optional[int], operador_id: int, estado: str,
                fecha_asignacion=None, fecha_finalizacion=None, rescatista_id: Optional[int] = None):
        self.id = id
        self.tipo = tipo
        self.drone_id = drone_id
        self.operador_id = operador_id
        self.estado = estado
        self.fecha_asignacion = fecha_asignacion
        self.fecha_finalizacion = fecha_finalizacion
        self.rescatista_id = rescatista_id

    @classmethod
    def crear(cls, tipo: str, operador_id: int):
        tipo = tipo.strip().lower()

        mapeo = {
            "búsqueda": "búsqueda", "busqueda": "búsqueda",
            "suministros": "suministros", "entrega": "suministros", "suministro": "suministros",
            "vigilancia": "vigilancia",
            "mapeo": "mapeo", "mapeo_terreno": "mapeo", "mapeo terreno": "mapeo"
        }

        tipo_normalizado = mapeo.get(tipo)
        if not tipo_normalizado:
            raise ValueError("Tipo de misión inválido. Usa: búsqueda, suministros, vigilancia o mapeo")

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO misiones (tipo, operador_id, estado) 
                VALUES (%s, %s, 'en_curso')
            """, (tipo_normalizado, operador_id))
            mision_id = cur.lastrowid
            conn.commit()

            return cls(mision_id, tipo_normalizado, None, operador_id, "en_curso")
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Error al crear misión: {str(e)}")
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls) -> List['Mision']:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM misiones ORDER BY fecha_asignacion DESC")
            rows = cur.fetchall()
            return [cls(*row) for row in rows]
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
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Error al completar misión: {str(e)}")
        finally:
            cur.close()
            conn.close()

        self.estado = "completada"

    def __str__(self):
        return f"Misión {self.id}: {self.tipo} - {self.estado}"