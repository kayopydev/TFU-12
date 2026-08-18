# TechBuy API — Módulo 5

**Trabalho Final da Unidade — Módulo 5 (API RESTful)**
**Tema B — Sistema de E-commerce | Projeto: TechBuy — Loja Virtual de Eletrônicos**

## Continuidade do projeto

Este trabalho dá continuidade ao projeto TechBuy construído ao longo do curso:

- **Módulo 2 (Banco de Dados):** modelo relacional em MySQL (Clientes, Endereços, Categoria, Produtos, Pedidos, Itens_Pedido).
- **Módulo 3 (Modelagem de Sistemas):** documento de requisitos e diagramas UML (Caso de Uso, Atividade, Classes, Sequência, Estados, Componente).
- **Módulo 4 (Orientação a Objetos):** classes em Python (`Usuario`, `Cliente`, `Administrador`, `Endereco`, `Categoria`, `Produto`, `Pedido`, `ItemPedido`), com herança, encapsulamento e polimorfismo.
- **Módulo 5 (este trabalho):** a API RESTful que dá vida ao sistema, com persistência real em banco de dados, validação, tratamento de erros e autenticação.

## Escopo escolhido

Para manter o projeto simples e dentro do prazo do módulo, a API foi construída em torno de duas entidades principais do diagrama de classes:

- **Categoria** → CRUD completo.
- **Produto** → CRUD completo, sempre vinculado a uma categoria existente (relacionamento um-para-muitos, igual ao definido no Bloco B).
- **Usuario** → cadastro e login, para cumprir o requisito de autenticação (segue o mesmo padrão da classe `Usuario` do Módulo 4: senha nunca é salva em texto puro).

As entidades `Cliente`, `Pedido` e `ItemPedido`, já modeladas nos módulos anteriores, ficam como sugestão de expansão futura da API (mencionada também no enunciado do trabalho).

## Estrutura do projeto

```
techbuy_api/
├── database.py         # conexão com o banco e SessionDep
├── criar_tabelas.py     # cria as tabelas no banco (rodar uma vez)
├── main.py              # ponto de entrada da API
├── security.py          # hash de senha e geração/validação de JWT
├── utils.py              # função obter_ou_404, usada nas rotas
├── requirements.txt
├── .gitignore
├── models/               # classes do SQLAlchemy (tabelas do banco)
│   ├── categoria.py
│   ├── produto.py
│   └── usuario.py
├── schemas/               # classes do Pydantic (validação de entrada/saída)
│   ├── categoria.py
│   ├── produto.py
│   └── usuario.py
└── routers/                # rotas da API, organizadas por entidade
    ├── categorias.py
    ├── produtos.py
    └── auth.py
```

## Como instalar e rodar

1. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie as tabelas do banco de dados (gera o arquivo `techbuy.db`):

```bash
python criar_tabelas.py
```

4. Rode a API:

```bash
fastapi dev main.py
```

5. Acesse a documentação interativa (Swagger) em:

```
http://127.0.0.1:8000/docs
```

## Principais rotas

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/` | Confirma que a API está no ar |
| POST | `/usuarios` | Cadastra um novo usuário |
| POST | `/token` | Login — devolve o token JWT |
| GET | `/usuarios/me` | Dados do usuário logado (rota protegida) |
| POST | `/categorias/` | Cadastra uma categoria |
| GET | `/categorias/` | Lista todas as categorias |
| GET | `/categorias/{id}` | Busca uma categoria, com seus produtos |
| PUT | `/categorias/{id}` | Atualiza uma categoria |
| DELETE | `/categorias/{id}` | Remove uma categoria (se não houver produtos vinculados) |
| POST | `/produtos/` | Cadastra um produto (precisa de uma categoria existente) |
| GET | `/produtos/` | Lista produtos (aceita filtro `?id_categoria=`) |
| GET | `/produtos/{id}` | Busca um produto, com a categoria aninhada |
| PUT | `/produtos/{id}` | Atualiza um ou mais campos de um produto |
| DELETE | `/produtos/{id}` | Remove um produto |

## Como testar o login pelo Swagger

1. Cadastre um usuário em `POST /usuarios`.
2. Clique no botão **Authorize** (cadeado, no topo da página `/docs`).
3. Informe o e-mail no campo *username* e a senha no campo *password*.
4. Depois disso, a rota `GET /usuarios/me` já pode ser testada autenticada.

## Versionamento (Git e GitHub)

O projeto já está com o Git iniciado localmente, com commits separados por etapa do desenvolvimento (estrutura inicial, models, schemas, CRUD de categoria, CRUD de produto, autenticação, integração no main.py e README). Para publicar no GitHub, faltam apenas os passos abaixo, que exigem a sua conta:

```bash
# 1. Crie um repositório vazio no GitHub (sem README, sem .gitignore)
# 2. No terminal, dentro da pasta do projeto:
git remote add origin https://github.com/SEU-USUARIO/techbuy-api.git
git branch -M main
git push -u origin main
```

## Decisões de projeto

- **Banco de dados SQLite**, por ser simples de configurar e não exigir instalação de um servidor separado — coerente com o nível do trabalho.
- **Erro 404 centralizado** na função `obter_ou_404()` (`utils.py`), evitando repetir a mesma verificação em cada rota.
- **Sessão do banco injetada via `Depends`**, usando o apelido `SessionDep`, conforme pedido no enunciado.
- **Senha do usuário** é sempre convertida em hash (biblioteca `passlib`) antes de ser salva; nunca é devolvida nas respostas da API.
- **Login com JWT** (biblioteca `python-jose`), com uma rota protegida de exemplo (`/usuarios/me`) para demonstrar o uso do token.
