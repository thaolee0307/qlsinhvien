
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def ket_noi_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Thaoancut2103@",
        database="THONGTINSV"
    )


def tao_bang():
    conn = ket_noi_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SINHVIEN (
                MASV VARCHAR(20) PRIMARY KEY,
                HOTEN VARCHAR(100) NOT NULL,
                NGAYSINH DATE,
                LOP VARCHAR(50)
            )
        """)
        conn.commit()
        cursor.close()
    finally:
        conn.close()



@app.route("/")
def home():
    conn = ket_noi_db()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT MASV, HOTEN, NGAYSINH, LOP
                FROM SINHVIEN
                ORDER BY MASV
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
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SINHVIEN (MASV, HOTEN, NGAYSINH, LOP)
            VALUES (%s, %s, %s, %s)
        """, (masv, hoten, ngaysinh, lop))
        conn.commit()
        cursor.close()
    finally:
        conn.close()

    return redirect(url_for("home"))


@app.route("/xoa/<masv>", methods=["POST"])
def xoa(masv):
    conn = ket_noi_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM SINHVIEN WHERE MASV = %s",
            (masv,)
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    tao_bang()
    app.run(debug=True)
