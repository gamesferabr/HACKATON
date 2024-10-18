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

### 7. Criar Superusuário e Usar o Admin do Django

Django inclui uma interface de administração para gerenciar o banco de dados. Para acessá-la, siga os passos abaixo.

1. **Criar um superusuário**:

\`\`\`
python manage.py createsuperuser
\`\`\`

Digite as credenciais para o superusuário, como nome de usuário, e-mail e senha.

2. **Registrar modelos no admin**:

No arquivo \`admin.py\` do seu app, registre os modelos para que eles apareçam na interface de administração.

Exemplo:

\`\`\`python
from django.contrib import admin
from .models import Evento  # Substitua pelo nome do seu modelo

admin.site.register(Evento)
\`\`\`

3. **Acessar a interface de administração**:

Inicie o servidor de desenvolvimento:

\`\`\`
python manage.py runserver
\`\`\`

Acesse a interface de administração no navegador:

\`http://127.0.0.1:8000/admin/\`

Faça login com o superusuário criado e você poderá gerenciar seus dados no banco de dados a partir da interface de administração.

### 8. Instalar o Elasticsearch

Para instalar o Elasticsearch em sua máquina, siga os passos abaixo:

1. **Baixar o Elasticsearch**:
   - Acesse a página oficial de downloads do Elasticsearch: [https://www.elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch).
   - Escolha a versão adequada para o seu sistema operacional (Windows, macOS, ou Linux).

2. **Instalar no Windows**:
   - Extraia o conteúdo do arquivo baixado.
   - Navegue até o diretório extraído e execute o seguinte comando no PowerShell:
     \`\`\`bash
     .\\bin\\elasticsearch.bat
     \`\`\`
   - Certifique-se de que o Java esteja instalado corretamente no sistema, pois ele é necessário para rodar o Elasticsearch.

3. **Instalar no macOS usando Homebrew**:
   - Caso você utilize o Homebrew, pode instalar o Elasticsearch facilmente com:
     \`\`\`bash
     brew tap elastic/tap
     brew install elasticsearch
     \`\`\`
   - Depois, inicie o serviço com:
     \`\`\`bash
     elasticsearch
     \`\`\`

4. **Instalar no Linux**:
   - Para distribuições baseadas em Debian/Ubuntu:
     \`\`\`bash
     wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.x.x-amd64.deb
     sudo dpkg -i elasticsearch-8.x.x-amd64.deb
     sudo systemctl enable elasticsearch
     sudo systemctl start elasticsearch
     \`\`\`
   - Certifique-se de substituir \`8.x.x\` pela versão específica que você baixou.

5. **Verificar a Instalação**:
   - Após iniciar o Elasticsearch, verifique se ele está funcionando corretamente acessando no seu navegador:
     \`\`\`
     http://localhost:9200
     \`\`\`
   - Você deverá ver uma resposta JSON indicando que o Elasticsearch está ativo.

6. **Configurações Adicionais**:
   - Configure o arquivo \`elasticsearch.yml\` para ajustar parâmetros como host, portas e permissões de acesso.
   - Este arquivo está localizado dentro da pasta \`config\` no diretório do Elasticsearch.

7. **Integrar com o Django**:
   - Para usar o Elasticsearch com o Django, você pode instalar a biblioteca \`django-elasticsearch-dsl\`:
     \`\`\`
     pip install django-elasticsearch-dsl
     \`\`\`
   - Consulte a documentação oficial para mais detalhes sobre a integração: [https://django-elasticsearch-dsl.readthedocs.io/en/latest/](https://django-elasticsearch-dsl.readthedocs.io/en/latest/)
  
   - Para lidar com a conexão do Django com o Elasticsearch, você pode usar o arquivo \`elastic.py\` para definir os índices de pesquisa e mapear os modelos do Django para o Elasticsearch. E 
   Para se conectar também ! Só ter certeza de sua porta local que por padrão é 9200. Além disso
   a pasta está localizada em /app/services/utils/elastic.py

Agora, o Elasticsearch deve estar rodando na sua máquina, pronto para ser usado com seu projeto Django!

## Problemas Comuns

### 1. Erro ao Compilar o \`mysqlclient\`

Se você estiver usando \`mysqlclient\` e receber um erro pedindo o **Microsoft Visual C++ Build Tools**, siga uma destas opções:

- Instale o \`Build Tools\` [neste link](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
- Alternativamente, use o \`mysql-connector-python\` que não exige compilação.

### 2. Conexão MySQL Não Funciona

Verifique se o MySQL está rodando corretamente e que o usuário e senha no arquivo \`settings.py\` estão corretos. Além disso, certifique-se de que o banco de dados foi criado e que o usuário tem permissões adequadas.
