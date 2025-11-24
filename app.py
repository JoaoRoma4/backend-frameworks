from flask import Flask, request, jsonify
# Importa os componentes do nosso banco de dados
from database import SessionLocal, Usuario, criar_banco

# Configuração do Flask
app = Flask(__name__)

# Cria o banco de dados e as tabelas na inicialização
criar_banco()

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    # Abre uma nova sessão
    session = SessionLocal()
    # Consulta todos os usuários
    usuarios = session.query(Usuario).all()
    # Fecha a sessão
    session.close()

    # Retorna a lista de usuários em formato JSON
    return jsonify([{"id": u.id, "nome": u.nome} for u in usuarios])

@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    # Obtém os dados JSON enviados na requisição (espera-se 'nome')
    data = request.json
    session = SessionLocal()

    try:
        # Cria um novo objeto Usuario
        novo = Usuario(nome=data["nome"])
        # Adiciona ao session e comita (salva) no banco
        session.add(novo)
        session.commit()
        # Atualiza o objeto para pegar o ID gerado
        session.refresh(novo)

        usuario = {"id": novo.id, "nome": novo.nome}
        
        # Retorna o novo usuário criado com status 201 (Created)
        return jsonify(usuario), 201
    except KeyError:
        # Rollback em caso de erro, como falta do campo 'nome'
        session.rollback()
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400
    finally:
        session.close()

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def remover_usuario(id):
    session = SessionLocal()
    # Busca o usuário pelo ID
    usuario = session.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        session.close()
        return jsonify({"erro": "Usuário não encontrado"}), 404

    # Deleta o usuário e comita
    session.delete(usuario)
    session.commit()
    session.close()

    return jsonify({"mensagem": "Usuário removido com sucesso"})
    

if __name__ == "__main__":
    # Inicia a aplicação Flask (só funciona no ambiente local)
    app.run(debug=True)