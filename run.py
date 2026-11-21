from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)


# Funcion que calcula el promedio de las 3 notas
def calcular_promedio(n1, n2, n3):
    promedio = (n1 + n2 + n3) / 3
    return promedio


# Funcion que revisa si aprueba o reprueba
def calcular_estado(promedio, asistencia):
    if promedio >= 40 and asistencia >= 75:
        return "APROBADO"
    else:
        return "REPROBADO"


# Funcion que devuelve el nombre mas largo y su cantidad de letras
def nombre_mas_largo(nombre1, nombre2, nombre3):
    mayor = nombre1
    if len(nombre2) > len(mayor):
        mayor = nombre2
    if len(nombre3) > len(mayor):
        mayor = nombre3
    return mayor, len(mayor)


# Pagina principal con los dos botones
@app.route("/")
def index():
    return render_template("index.html")


# Redireccion al menu principal
@app.route("/inicio")
def inicio():
    return redirect(url_for("index"))


# Ejercicio 1: notas y asistencia
@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    promedio = None
    estado = None
    error = None

    if request.method == "POST":
        try:
            nota1 = float(request.form["nota1"])
            nota2 = float(request.form["nota2"])
            nota3 = float(request.form["nota3"])
            asistencia = float(request.form["asistencia"])
        except KeyError:
            # si falta algun dato se aborta la conexion
            abort(400)
        except ValueError:
            error = "Debes ingresar solo numeros"
            return render_template("ejercicio1.html", error=error)

        # las notas van de 10 a 70 y la asistencia de 0 a 100
        if nota1 < 10 or nota1 > 70 or nota2 < 10 or nota2 > 70 or nota3 < 10 or nota3 > 70:
            error = "Las notas deben estar entre 10 y 70"
        elif asistencia < 0 or asistencia > 100:
            error = "La asistencia debe estar entre 0 y 100"
        else:
            promedio = round(calcular_promedio(nota1, nota2, nota3), 1)
            estado = calcular_estado(promedio, asistencia)

    return render_template("ejercicio1.html", promedio=promedio, estado=estado, error=error)


# Ejercicio 2: nombres
@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    nombre = None
    cantidad = None

    if request.method == "POST":
        try:
            nombre1 = request.form["nombre1"].strip()
            nombre2 = request.form["nombre2"].strip()
            nombre3 = request.form["nombre3"].strip()
        except KeyError:
            abort(400)

        nombre, cantidad = nombre_mas_largo(nombre1, nombre2, nombre3)

    return render_template("ejercicio2.html", nombre=nombre, cantidad=cantidad)


# Paginas de error
@app.errorhandler(404)
def error_404(e):
    return render_template("error.html", codigo=404, mensaje="La pagina no existe"), 404


@app.errorhandler(400)
def error_400(e):
    return render_template("error.html", codigo=400, mensaje="Faltan datos en el formulario"), 400


if __name__ == "__main__":
    app.run(debug=True)
