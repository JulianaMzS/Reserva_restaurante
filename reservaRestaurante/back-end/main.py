from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import Reserva
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Jujuba345!@localhost/Reserva_restaurante"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/reservas", methods=["POST"])
def criar_reserva():
    dados = request.json

    try:
        data_convertida = datetime.strptime(dados.get("data"), "%Y-%m-%d").date()
        hora_convertida = datetime.strptime(dados.get("hora"), "%H:%M:%S").time()
    except Exception as e:
        return jsonify({"erro": f"Data ou hora em formato inválido: {str(e)}"}), 400

    nova = Reserva(
        nome_cliente=dados.get("nome_cliente"),
        telefone_cliente=dados.get("telefone_cliente"),
        data=data_convertida,
        hora=hora_convertida,
        numero_pessoas=dados.get("numero_pessoas")
    )

    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Reserva criada com sucesso!"}), 201


@app.route("/reservas", methods=["GET"])
def listar_reservas():
    reservas = Reserva.query.all()
    return jsonify([{
        "id": r.id,
        "nome_cliente": r.nome_cliente,
        "telefone_cliente": r.telefone_cliente,
        "data": str(r.data),
        "hora": str(r.hora),
        "numero_pessoas": r.numero_pessoas,
        "status": r.status
    } for r in reservas])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Conectado ao banco e tabelas prontas!")

    app.run(debug=True)
