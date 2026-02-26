from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

caminho_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'gestao_dispositivos.db')

def conectar_db():
    return sqlite3.connect(caminho_db)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "sistema": "Gestão de Dispositivos API",
        "status": "Online",
        "documentacao": "Aceda a /aparelhos para listar os dispositivos"
    })

@app.route('/aparelhos', methods=['GET'])
def get_aparelhos():
    try:
        conexao = conectar_db()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT id, modelo, imei, numero_serie, status FROM aparelhos")
        
        # Pegamos os nomes das colunas
        colunas = [column[0] for column in cursor.description]
        
        # Pegamos os dados (apenas UMA vez)
        linhas = cursor.fetchall()
        
        # Montamos a lista de dicionários
        resultados = []
        for row in linhas:
            resultados.append(dict(zip(colunas, row)))
        
        conexao.close() # Fechamos a conexão FORA do loop
        return jsonify(resultados) # Retornamos os dados FORA do loop
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route('/aparelhos', methods=['POST'])
def add_aparelho():
    try:
        # Resolve o erro de tipo definindo um dicionário padrão
        dados = request.get_json() or {}
        
        conexao = conectar_db()
        cursor = conexao.cursor()
        
        # Usar .get() limpa os erros de aviso no VS Code
        cursor.execute(
            "INSERT INTO aparelhos (modelo, imei, numero_serie, status) VALUES (?, ?, ?, ?)",
            (dados.get('modelo'), dados.get('imei'), dados.get('numero_serie'), dados.get('status'))
        )
        
        conexao.commit()
        conexao.close()
        return jsonify({"mensagem": "Sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == '__main__':
    # Roda o servidor. debug=True ajuda a ver erros em tempo real
    app.run(host='0.0.0.0', port=5000, debug=True)