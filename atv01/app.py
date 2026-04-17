from flask import Flask, jsonify, render_template, request

from src.agente_temperatura import AgenteTemperatura

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/decidir")
def decidir():
    dados = request.get_json(silent=True) or {}

    try:
        temperatura_atual = float(dados.get("temperatura_atual"))
        temperatura_desejada = float(dados.get("temperatura_desejada", 25))
    except (TypeError, ValueError):
        return jsonify(
            {"erro": "Valores invalidos. Informe numeros para as temperaturas."}
        ), 400

    agente = AgenteTemperatura(temperatura_desejada=temperatura_desejada)
    acao = agente.decidir(temperatura_atual)
    custo = agente.custo(temperatura_atual)

    return jsonify(
        {
            "temperatura_atual": temperatura_atual,
            "temperatura_desejada": temperatura_desejada,
            "limite_inferior": round(agente.limite_inferior(), 2),
            "limite_superior": round(agente.limite_superior(), 2),
            "acao": acao,
            "modo": agente.modo,
            "sistema_ligado": agente.sistema_ligado,
            "custo": round(custo, 2),
        }
    )


@app.post("/simular")
def simular():
    dados = request.get_json(silent=True) or {}

    try:
        temperatura_atual = float(dados.get("temperatura_atual"))
        temperatura_desejada = float(dados.get("temperatura_desejada", 25))
    except (TypeError, ValueError):
        return jsonify(
            {"erro": "Valores invalidos. Informe numeros para as temperaturas."}
        ), 400

    max_ciclos = dados.get("max_ciclos", 40)
    try:
        max_ciclos = int(max_ciclos)
    except (TypeError, ValueError):
        return jsonify({"erro": "max_ciclos deve ser um numero inteiro."}), 400

    if max_ciclos < 1 or max_ciclos > 200:
        return jsonify({"erro": "max_ciclos deve estar entre 1 e 200."}), 400

    agente = AgenteTemperatura(temperatura_desejada=temperatura_desejada)
    resultado = agente.gerar_trace(temperatura_atual, max_ciclos=max_ciclos)

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)
