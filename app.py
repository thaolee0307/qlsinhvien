from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
import os

def ket_noi_mysql():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "THONGTINSV"),
        port=int(os.environ.get("DB_PORT", "3306"))
    )

@app.route("/")
def home():
    conn = ket_noi_mysql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT MASV, HOTEN, NGAYSINH, LOP FROM SINHVIEN"
    )
    danh_sach = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", danh_sach=danh_sach)

@app.route("/them", methods=["POST"])
def them():
    masv = request.form["masv"]
    hoten = request.form["hoten"]
    ngaysinh = request.form["ngaysinh"] or None
    lop = request.form["lop"]
    conn = ket_noi_mysql()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO SINHVIEN (MASV, HOTEN, NGAYSINH, LOP)
           VALUES (%s, %s, %s, %s)""",
        (masv, hoten, ngaysinh, lop)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("home"))

@app.route("/xoa/<masv>", methods=["POST"])
def xoa(masv):
    conn = ket_noi_mysql()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM SINHVIEN WHERE MASV = %s",
        (masv,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
