from datetime import datetime

from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///base.db")


@app.route("/")
def index():
    paquete = db.execute("SELECT * FROM Paquetes ORDER BY id ASC")
    paquetelen = len(paquete)
    if 'user' in session:
        return render_template("index.html", paquete=paquete, paquetelen=paquetelen, session=session)
    return render_template("index.html", paquete=paquete, paquetelen=paquetelen)


@app.route("/Envio/")
def envio():
    id = int(request.args.get('id'))
    image = (request.args.get('image'))
    price = (request.args.get('price'))
    name = (request.args.get('name'))
    paquete = db.execute("SELECT * FROM Paquetes ORDER BY id ASC")
    paquetelen = len(paquete)
    if 'user' in session:
        return render_template("Envio.html", name=name, price=price, id=id, image=image)
    return render_template("index.html", msg="Ingresa para reservar", paquete=paquete, paquetelen=paquetelen)


@app.route("/hecho/")
def hecho():
    id = int(request.args.get('id'))
    image = (request.args.get('image'))
    price = (request.args.get('price'))
    name = (request.args.get('name'))
    calle = (request.args.get('calle'))
    colonia = (request.args.get('colonia'))
    ncasa = (request.args.get('ncasa'))
    ciudad = (request.args.get('ciudad'))
    num = (request.args.get('cel'))
    date = (request.args.get('fecha'))
    db.execute(
        "INSERT INTO Compras(uid, image, id, name, price, date, calle, num, colonia, ncasa, ciudad)VALUES(:uid, :image, :id, :name, :price, :date, :calle, :num, :colonia, :ncasa, :ciudad)",
        uid=session["uid"], image=image, id=id, name=name, price=price, date=date, calle=calle, num=num,
        colonia=colonia, ncasa=ncasa, ciudad=ciudad)
    db.execute(
        "INSERT INTO envio(uid, calle, colonia, ncasa, ciudad, num) VALUES(:uid, :calle, :colonia, :ncasa, :ciudad, :num)",
        uid=session["uid"], calle=calle, num=num, colonia=colonia, ncasa=ncasa, ciudad=ciudad)
    paquete = db.execute("SELECT * FROM Paquetes ORDER BY id ASC")
    paquetelen = len(paquete)
    return render_template("index.html", paquete=paquete, paquetelen=paquetelen)


@app.route("/cancelar/")
def cancelar():
    paquete = db.execute("SELECT * FROM Paquetes ORDER BY id ASC")
    paquetelen = len(paquete)
    return render_template("index.html", paquete=paquete, paquetelen=paquetelen)


@app.route("/registro/", methods=["POST"])
def registration():
    username = request.form["username"]
    password = request.form["password"]
    fname = request.form["fname"]
    pname = request.form["pname"]
    mname = request.form["mname"]
    email = request.form["email"]
    rows = db.execute("SELECT * FROM Usuario WHERE username = :username ", username=username)
    if len(rows) > 0:
        return render_template("Registro.html", msg="Este usuario ya existe!")
    new = db.execute(
        "INSERT INTO Usuario (username, password, fname, pname, mname, email)VALUES(:username, :password, :fname, :pname, :mname, :email)",
        username=username, password=password, fname=fname, pname=pname, mname=mname, email=email)
    return render_template("Ingresar.html", msg="Registro correcto")


@app.route("/ingresar/", methods=["GET"])
def new():
    return render_template("Ingresar.html")


@app.route("/registrar/", methods=["GET"])
def login():
    return render_template("Registro.html")


@app.route("/ingresado/", methods=["POST"])
def logged():
    user = request.form["username"].lower()
    pwd = request.form["password"]
    if user == "" or pwd == "":
        return render_template("Ingresar.html", msg="Espacios vacios")
    query = "SELECT * FROM Usuario WHERE username = :user AND password = :pwd"
    rows = db.execute(query, user=user, pwd=pwd)
    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.now()
        session['uid'] = rows[0]["id"]
    if 'user' in session:
        return redirect("/")
    return render_template("Ingresar.html", msg="Contraseña o usario incorrecto")


@app.route("/salir/")
def logout():
    session.clear()
    return redirect("/")


@app.route("/historial/")
def history():
    compra = db.execute("SELECT * FROM Compras WHERE uid=:uid ORDER BY id DESC", uid=session["uid"])
    compralen = len(compra)
    return render_template("Historial.html", session=session, compra=compra, compralen=compralen)


@app.route("/editar/")
def editar():
    id = int(request.args.get('id'))
    paquete = db.execute("SELECT * FROM Compras WHERE id=:id", id=id)
    return render_template("Editar.html", paquete=paquete)


@app.route("/borrar/")
def borrar():
    id = int(request.args.get('id'))
    db.execute('DELETE FROM Compras WHERE id=:id', id=id)
    compra = db.execute("SELECT * FROM Compras WHERE uid=:uid", uid=session["uid"])
    compralen = len(compra)
    return render_template("Historial.html", session=session, compra=compra, compralen=compralen)


@app.route("/editado/")
def editado():
    id = int(request.args.get('id'))
    name = (request.args.get('name'))
    price = int(request.args.get('price'))
    calle = (request.args.get('calle'))
    image = (request.args.get('image'))
    colonia = (request.args.get('colonia'))
    ncasa = int(request.args.get('ncasa'))
    ciudad = (request.args.get('ciudad'))
    num = int(request.args.get('cel'))
    date = (request.args.get('fecha'))
    db.execute("DELETE FROM Compras WHERE id = :id", id=id)
    db.execute(
        "INSERT INTO Compras(uid,image, id, name,price, calle, colonia, ncasa, ciudad, num, date) VALUES(:uid, :image, :id, :name, :price, :calle, :colonia, :ncasa, :ciudad, :num, :date)",
        uid=session["uid"], image=image, price=price, calle=calle, num=num, colonia=colonia, ncasa=ncasa, ciudad=ciudad,
        date=date, id=id, name=name)
    compra = db.execute("SELECT * FROM Compras WHERE uid=:uid", uid=session["uid"])
    compralen = len(compra)
    return render_template("Historial.html", session=session, compra=compra, compralen=compralen)


if __name__ == '__main__':
    app.run()
