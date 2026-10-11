
from flask import Flask, render_template, request, redirect, url_for
import psycopg
from psycopg.rows import dict_row
import os

app = Flask(__name__)

def ket_noi_db():
    return psycopg.connect(
        os.environ["DATABASE_URL"],
        row_factory=dict_row,
        sslmode="require"
    )


def tao_bang():
    conn = ket_noi_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sinhvien (
                    masv VARCHAR(20) PRIMARY KEY,
                    hoten VARCHAR(100) NOT NULL,
                    ngaysinh DATE,
                    lop VARCHAR(50)
                )
            """)
        conn.commit()
    finally:
        conn.close()


@app.route("/")
def home():
    conn = ket_noi_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    masv AS "MASV",
                    hoten AS "HOTEN",
                    ngaysinh AS "NGAYSINH",
                    lop AS "LOP"
                FROM sinhvien
                ORDER BY masv
                """)
            danh_sach = cursor.fetchall()
    finally:
        conn.close()

    return render_template("index.html", danh_sach=danh_sach)


@app.route("/them", methods=["POST"])
def them():
    masv = request.form["masv"]
    hoten = request.form["hoten"]
    ngaysinh = request.form["ngaysinh"] or None
    lop = request.form["lop"]

    conn = ket_noi_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sinhvien (masv, hoten, ngaysinh, lop)
                VALUES (%s, %s, %s, %s)
                """,
                (masv, hoten, ngaysinh, lop)
            )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("home"))


@app.route("/xoa/<masv>", methods=["POST"])
def xoa(masv):
    conn = ket_noi_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sinhvien WHERE masv = %s",
                (masv,)
            )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("home"))


# Tao bang khi ung dung khoi dong
with app.app_context():
    tao_bang()


if __name__ == "__main__":
    app.run(debug=True)
