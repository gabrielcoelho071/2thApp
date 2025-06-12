from flask import Flask, jsonify, request, redirect
from flask_pydantic_spec import FlaskPydanticSpec
from sqlalchemy.exc import IntegrityError

from models_livro import *
from sqlalchemy import select

app = Flask(__name__)
spec = FlaskPydanticSpec('flask',
                         title='Livraria API - SENAI',
                         version='1.0.0')
spec.register(app)
app.config['SECRET_KEY'] = 'chave_secretinha'

@app.route('/')
def index():
    """
        API para gerenciar uma biblioteca integrada a um banco de dados

    """
    return redirect('/livros')

@app.route("/livros_post", methods=['POST'])
def post_livros():
    db = db_session()
    try:
        dados_livro = request.get_json()
        livro = dados_livro['livro']
        autor = dados_livro['autor']
        categoria = dados_livro['categoria']
        descricao = dados_livro['descricao']

        if not livro or not autor or not categoria or not descricao:
            return jsonify({"mensagem": "Erro de requisicao"}), 400

        form_evento = Livro(
            livro=livro,
            autor=autor,
            categoria=categoria,
            descricao=descricao
        )
        form_evento.save()
        db.close()
        return jsonify({"mensagem": "OK"}), 200
    except ValueError as e:
        return jsonify({"mensagem": str(e)}), 400

@app.route('/livros_get', methods=['GET'])
def get_livros():
    db = db_session()
    try:
        lista = db.execute(select(Livro)).scalars().all()
        resultados = []
        for livro in lista:
            resultados.append(livro.serialize())
        db.close()
        return jsonify(resultados), 200
    except ValueError:
        return jsonify({"mensagem": "Formato inválido."}), 400
    except TypeError:
        return jsonify({'mensagem': 'Error. Integrity Error (faltam informações ou informações corretas) '}), 400
    except Exception as e:
        return jsonify({"mensagem": str(e)}), 500

@app.route('/livros_put/<int:id_livro>', methods=['PUT'])
def put_livro(id_livro):
    db = db_session()
    try:
        # Fetch the task from the database
        livro = db.execute(select(Livro).where(Livro.id_livro == id_livro)).scalar()

        if livro is None:
            return jsonify({"mensagem": "Livro não encontrado."})

        dados_livro = request.get_json()
        # Captura os valores dos campos do formulário
        titulo = dados_livro['livro']
        autor = dados_livro["autor"]
        ISBN = dados_livro["categoria"]
        resumo = dados_livro["descricao"]

        livro.livro = titulo
        livro.autor = autor
        livro.ISBN = ISBN
        livro.resumo = resumo

        # Save changes to the database
        livro.save()
        db.close()
        return jsonify({"mensagem": "Livro atualizado com sucesso!"}), 200
    except ValueError:
        return jsonify({"mensagem": "Formato inválido."}), 400
    except TypeError:
        return jsonify({'result': 'Error. Integrity Error (faltam informações ou informações corretas) '}), 400
    except Exception as e:
        return jsonify({"mensagem": str(e)}), 500

@app.route('/livros/<int:id_livro>', methods=['DELETE'])
def delete_livro(id_livro):
    db = db_session()
    try:
        var_livro = select(Livro).where(Livro.id_livro == id_livro)
        var_livro = db.execute(var_livro).scalar()
        var_livro.delete()
        db.close()
        return jsonify({"mensagem": "Livro deletado com sucesso!"})
    except ValueError:
        return jsonify({"mensagem": "Formato inválido."}), 400
    except TypeError:
        return jsonify({'result': 'Error. Integrity Error (faltam informações ou informações corretas) '}), 400
    except Exception as e:
        return jsonify({"mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)