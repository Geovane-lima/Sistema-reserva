from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="reservas_db"
)

cursor = conexao.cursor(dictionary=True)

@app.route('/login', methods=['POST'])
def login():

    dados = request.json

    usuario = dados['usuario']
    senha = dados['senha']

    sql = """
    SELECT * FROM usuarios
    WHERE usuario = %s AND senha = %s
    """

    valores = (usuario, senha)

    cursor.execute(sql, valores)

    resultado = cursor.fetchone()

    if resultado:
        return jsonify({
            "status": "sucesso",
            "mensagem": "Login realizado com sucesso!",
            "usuario": resultado["usuario"],
            "privilegio": resultado["privilegio"]
        })

    return jsonify({
        "status": "erro",
        "mensagem": "Usuário ou senha inválidos!"
    })

@app.route('/reservas', methods=['GET'])
def listar_reservas():

    sql = "SELECT * FROM reservas"

    cursor.execute(sql)

    reservas = cursor.fetchall()

    return jsonify(reservas)

@app.route('/reservar', methods=['POST'])
def reservar():

    dados = request.json

    sala = dados['sala']
    data = dados['data']
    horario = dados['horario']
    usuario = dados['usuario']

    sql_verifica = """
    SELECT * FROM reservas
    WHERE sala = %s
    AND data_reserva = %s
    AND horario = %s
    """

    valores_verifica = (sala, data, horario)

    cursor.execute(sql_verifica, valores_verifica)

    conflito = cursor.fetchone()

    if conflito:
        return jsonify({
            "status": "erro",
            "mensagem": "Horário já reservado!"
        })

    sql = """
    INSERT INTO reservas
    (sala, data_reserva, horario, usuario)
    VALUES (%s, %s, %s, %s)
    """

    valores = (sala, data, horario, usuario)

    cursor.execute(sql, valores)

    conexao.commit()

    return jsonify({
        "status": "sucesso",
        "mensagem": "Reserva realizada com sucesso!"
    })

@app.route('/cancelar/<int:id>', methods=['DELETE'])
def cancelar_reserva(id):

    sql = "DELETE FROM reservas WHERE id = %s"

    cursor.execute(sql, (id,))

    conexao.commit()

    return jsonify({
        "status": "sucesso",
        "mensagem": "Reserva cancelada!"
    })

if __name__ == '__main__':
    app.run(debug=True)
