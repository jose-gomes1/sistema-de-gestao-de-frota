from storage import get_conn
from carro import Carro
from mota import Mota
import sqlite3

class Frota:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = get_conn()
        conn.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            marca TEXT,
            modelo TEXT,
            preco REAL,
            vel INTEGER,
            combustivel TEXT,
            cor TEXT,
            eletrico INTEGER,
            consumo REAL,
            cilindrada INTEGER,
            com_iva INTEGER DEFAULT 0
        )
        """)
        # Add com_iva if missing in older DBs
        try:
            conn.execute("SELECT com_iva FROM veiculos LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE veiculos ADD COLUMN com_iva INTEGER DEFAULT 0")
        conn.commit()

    # ---------------- LOAD ----------------
    def listar(self):
        conn = get_conn()
        return conn.execute("SELECT * FROM veiculos").fetchall()

    # ---------------- ADD ----------------
    def adicionar_veiculo(self, v):
        conn = get_conn()
        conn.execute("""
        INSERT INTO veiculos
        (tipo, marca, modelo, preco, vel, combustivel, cor, eletrico, consumo, cilindrada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            v.tipo, v.marca, v.modelo, v.preco, v.vel, v.combustivel,
            v.cor,
            int(getattr(v, "eletrico", False)),
            getattr(v, "consumo_kwh", None),
            getattr(v, "cilindrada", None)
        ))
        conn.commit()

    # ---------------- DELETE ----------------
    def remover(self, vid):
        conn = get_conn()
        conn.execute("DELETE FROM veiculos WHERE id=?", (vid,))
        conn.commit()

    # ---------------- DISCOUNT ----------------
    def toggle_desconto(self, vid):
        conn = get_conn()
        row = conn.execute(
            "SELECT preco, com_iva FROM veiculos WHERE id=?", (vid,)
        ).fetchone()

        if not row:
            return

        if row["com_iva"]:
            novo = row["preco"] / 0.9  # remove 10% IVA
            iva = 0
        else:
            novo = row["preco"] * 0.9  # add 10% IVA
            iva = 1

        conn.execute(
            "UPDATE veiculos SET preco=?, com_iva=? WHERE id=?",
            (novo, iva, vid)
        )
        conn.commit()

    # ---------------- UPDATE ----------------
    def atualizar(self, vid, marca, modelo, preco, vel, combustivel, cor):
        conn = get_conn()
        conn.execute("""
        UPDATE veiculos
        SET marca=?, modelo=?, preco=?, vel=?, combustivel=?, cor=?
        WHERE id=?
        """, (marca, modelo, preco, vel, combustivel, cor, vid))
        conn.commit()

    # ---------------- FILTER ----------------
    def filtrar_por_marca(self, marca):
        conn = get_conn()
        return conn.execute(
            "SELECT * FROM veiculos WHERE LOWER(marca)=LOWER(?)",
            (marca,)
        ).fetchall()
