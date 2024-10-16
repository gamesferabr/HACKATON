# Projeto MyORMProject

Este projeto Django foi criado com o objetivo de utilizar a ORM (Object Relational Mapping) do Django para interação com o banco de dados MySQL. Aqui estão as instruções detalhadas para configurar o ambiente, instalar dependências e executar o projeto.

## Pré-requisitos

Antes de iniciar, você precisará ter instalado:

- **Python 3.13** ou versão superior.
- **MySQL** (ou MariaDB) configurado no seu sistema.
- Ferramentas de desenvolvimento como o **pip** e **virtualenv**.

## Instruções de Configuração

### 1. Criar um Ambiente Virtual

Recomendamos a criação de um ambiente virtual para isolar as dependências do projeto.

#### No Windows:

1. Navegue até o diretório do projeto e crie o ambiente virtual:

\`\`\`
python -m venv myenv
\`\`\`

2. Ative o ambiente virtual:

\`\`\`
myenv\\Scripts\\activate
\`\`\`

#### No Linux/Mac:

1. Navegue até o diretório do projeto e crie o ambiente virtual:

\`\`\`
python3 -m venv myenv
\`\`\`

2. Ative o ambiente virtual:

\`\`\`
source myenv/bin/activate
\`\`\`

### 2. Instalar as Dependências

Com o ambiente virtual ativado, as bibliotecas do projeto devem ser instaladas **dentro do ambiente virtual**. Siga as instruções abaixo para garantir que isso aconteça corretamente.

1. Navegue até o diretório \`myenv\\Scripts\` (Windows) ou \`myenv/bin\` (Linux/Mac).

- **Windows**:
\`\`\`
cd myenv\\Scripts
\`\`\`

- **Linux/Mac**:
\`\`\`
cd myenv/bin
\`\`\`

2. Com o diretório acessado, execute o seguinte comando para instalar as dependências dentro do ambiente virtual:

\`\`\`
pip install -r requirements.txt
\`\`\`

3. Se você não tiver o arquivo \`requirements.txt\`, pode instalar manualmente as bibliotecas principais:

- Para MySQL com o conector \`mysqlclient\`:
\`\`\`
pip install mysqlclient
\`\`\`

- **OU**, se preferir evitar complicações, use o conector oficial da Oracle:
\`\`\`
pip install mysql-connector-python
\`\`\`

### 3. Configurar o Banco de Dados

No arquivo \`settings.py\`, configure o banco de dados MySQL com o nome do banco, usuário e senha apropriados. Exemplo de configuração:

\`\`\`python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',  # Ou 'django.db.backends.mysql' se estiver usando mysqlclient
        'NAME': 'meuprojeto',                # Nome do banco de dados
        'USER': 'novo_usuario',              # Nome do usuário criado no MySQL
        'PASSWORD': 'sua_senha_segura',      # Senha do usuário MySQL
        'HOST': 'localhost',                 # Host (localhost para local)
        'PORT': '3306',                      # Porta padrão do MySQL
    }
}
\`\`\`

### 4. Aplicar Migrações

Após configurar o banco de dados no \`settings.py\`, execute o seguinte comando para aplicar as migrações e criar as tabelas no banco de dados:

\`\`\`
python manage.py migrate
\`\`\`

### 5. Executar o Servidor de Desenvolvimento

Agora você pode rodar o servidor de desenvolvimento Django:

\`\`\`
python manage.py runserver
\`\`\`

Acesse o servidor local no navegador: \`http://127.0.0.1:8000/\`.

### 6. Gerar o \`requirements.txt\` (Opcional)

Se você adicionar mais dependências ao projeto ou precisar gerar um novo arquivo \`requirements.txt\`, siga estes passos:

1. Com o ambiente virtual ativado, execute o comando \`pip freeze\` para listar todas as dependências instaladas:

\`\`\`
pip freeze > requirements.txt
\`\`\`

2. Isso vai gerar um arquivo \`requirements.txt\` com todas as bibliotecas necessárias para o projeto.

## Problemas Comuns

### 1. Erro ao Compilar o \`mysqlclient\`

Se você estiver usando \`mysqlclient\` e receber um erro pedindo o **Microsoft Visual C++ Build Tools**, siga uma destas opções:

- Instale o \`Build Tools\` [neste link](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
- Alternativamente, use o \`mysql-connector-python\` que não exige compilação.

### 2. Conexão MySQL Não Funciona

Verifique se o MySQL está rodando corretamente e que o usuário e senha no arquivo \`settings.py\` estão corretos. Além disso, certifique-se de que o banco de dados foi criado e que o usuário tem permissões adequadas.

## Estrutura do Projeto

\`\`\`
myormproject/
│
├── myenv/                # Ambiente virtual do projeto
├── myapp/                # Aplicativo Django com os modelos
│   ├── migrations/       # Migrações do banco de dados
│   ├── models.py         # Definição dos modelos (tabelas)
│   └── ...
├── manage.py             # Script de gerenciamento do Django
├── requirements.txt      # Arquivo com as dependências do projeto
└── README.md             # Instruções e detalhes do projeto
\`\`\`