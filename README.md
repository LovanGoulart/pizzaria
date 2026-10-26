# 🍽️ Restaurante Manager — Pedidos, Cozinha e Caixa

Aplicação web em desenvolvimento para apoiar a operação de restaurantes, com perfis de administrador, garçom e cozinha.

O sistema organiza o fluxo entre registro do pedido, preparação, entrega e recebimento do pagamento, reunindo também cadastro de produtos, categorias, equipe e controle de caixa.

## Contexto e objetivo

Desenvolvi este projeto para organizar o atendimento em restaurantes e facilitar a comunicação entre salão, cozinha e administração.

O garçom registra os pedidos pelo PDV e acompanha seu andamento. A cozinha recebe as solicitações e atualiza a preparação. Quando um pedido é marcado como pronto, o garçom é notificado para buscá-lo.

O administrador gerencia o sistema, acompanha os pedidos, administra a equipe e registra os pagamentos dos clientes.

## Situação do projeto

**Em desenvolvimento.**

O projeto ainda não está concluído. As telas apresentadas demonstram os fluxos disponíveis na versão atual, que continuam passando por ajustes e validação.

## Principais funcionalidades

- Autenticação e controle de acesso por perfil.
- Perfis de administrador, garçom e cozinha.
- Gerenciamento da equipe.
- Cadastro e edição de produtos.
- Organização do cardápio por categorias.
- PDV para montagem de pedidos.
- Identificação da mesa.
- Inclusão de produtos, quantidades e observações.
- Consulta dos pedidos e de seus detalhes.
- Acompanhamento por status.
- Fila de pedidos para a cozinha.
- Atualização para em preparo e pronto.
- Notificação ao garçom quando o pedido estiver pronto.
- Registro da entrega.
- Registro do pagamento dos clientes.
- Abertura e acompanhamento do caixa.
- Dashboard com resumo do dia.

## Perfis de acesso

| Perfil | Responsabilidades |
|---|---|
| Administrador | Gerenciar equipe, produtos, categorias, pedidos, caixa e recebimentos. |
| Garçom | Registrar pedidos no PDV, consultar seu andamento e acompanhar a entrega. |
| Cozinha | Consultar os pedidos recebidos e atualizar os status de preparação. |

O acesso às telas e operações é organizado conforme a função de cada usuário.

## Fluxo de atendimento

1. O garçom registra o pedido no PDV.
2. O pedido fica disponível para a cozinha.
3. A cozinha inicia o atendimento e marca o pedido como em preparo.
4. Ao finalizar, a cozinha altera o status para pronto.
5. O garçom é notificado para buscar o pedido.
6. O pedido é servido e sua entrega é registrada.
7. O administrador registra o pagamento do cliente.

O andamento do preparo e a situação do pagamento são informações distintas, permitindo acompanhar pedidos ainda não pagos.

## Status dos pedidos

| Status | Significado |
|---|---|
| Aberto | Pedido registrado e aguardando preparação. |
| Em preparo | Pedido em preparação pela cozinha. |
| Pronto | Preparação concluída, aguardando retirada e entrega. |
| Entregue | Pedido servido ao cliente. |

## 📸 Demonstração do sistema

As capturas são exibidas com largura limitada, preservando a proporção. Clique nas imagens para consultar os arquivos originais.

### PDV — montagem dos pedidos

Seleção de produtos por categoria, busca no cardápio e montagem do pedido com identificação da mesa, valores e observações.

<a href="tela%20adm%20-%20pdv.png">
  <img src="tela%20adm%20-%20pdv.png" alt="PDV para montagem de pedidos" width="900">
</a>

### Garçom — registro de pedidos

Interface utilizada pelo garçom para registrar o atendimento.

<a href="tela%20gar%C3%A7om%20-%20fazendo%20pedidos.png">
  <img src="tela%20gar%C3%A7om%20-%20fazendo%20pedidos.png" alt="Garçom registrando um pedido" width="900">
</a>

### Garçom — inclusão de itens

Adição de produtos ao pedido durante o atendimento.

<a href="tela%20gar%C3%A7om%20-%20adicionando%20pedidos.png">
  <img src="tela%20gar%C3%A7om%20-%20adicionando%20pedidos.png" alt="Garçom adicionando itens ao pedido" width="900">
</a>

### Cozinha — recebimento de pedidos

Tela de acompanhamento dos pedidos encaminhados para preparação.

<a href="tela%20cozinha%20-%20recebendo%20pedido.png">
  <img src="tela%20cozinha%20-%20recebendo%20pedido.png" alt="Cozinha recebendo pedidos" width="900">
</a>

### Cozinha — pedidos em aberto

Fila de atendimento com os pedidos que aguardam preparação.

<a href="tela%20cozinha%20-%20pedidos%20em%20aberto.png">
  <img src="tela%20cozinha%20-%20pedidos%20em%20aberto.png" alt="Fila de pedidos em aberto na cozinha" width="900">
</a>

### Cozinha — detalhes do pedido

Consulta da mesa, itens, quantidades, total e situação do pedido.

<a href="tela%20cozinha%20-%20detalhes%20do%20pedido.png">
  <img src="tela%20cozinha%20-%20detalhes%20do%20pedido.png" alt="Detalhes de um pedido na cozinha" width="900">
</a>

### Garçom — pedido pronto

Acompanhamento do pedido após a conclusão pela cozinha, permitindo organizar a retirada e a entrega ao cliente.

<a href="tela%20gar%C3%A7om%20-%20notifica%C3%A7%C3%A3o%20do%20pedido%20pronto.png">
  <img src="tela%20gar%C3%A7om%20-%20notifica%C3%A7%C3%A3o%20do%20pedido%20pronto.png" alt="Pedido pronto para retirada pelo garçom" width="900">
</a>

### Administração — produtos

Gerenciamento dos produtos disponíveis no cardápio.

<a href="tela%20adm%20-%20produtos.png">
  <img src="tela%20adm%20-%20produtos.png" alt="Gerenciamento de produtos" width="900">
</a>

### Administração — categorias

Organização das categorias utilizadas no cardápio.

<a href="tela%20adm%20-%20categorias.png">
  <img src="tela%20adm%20-%20categorias.png" alt="Gerenciamento de categorias" width="900">
</a>

### Administração — equipe

Consulta e gerenciamento dos integrantes da equipe.

<a href="tela%20adm%20-%20gerenciamento%20da%20equipe.png">
  <img src="tela%20adm%20-%20gerenciamento%20da%20equipe.png" alt="Gerenciamento da equipe do restaurante" width="900">
</a>

### Administração — novo integrante

Cadastro de membros para utilização do sistema.

<a href="tela%20adm%20-%20novo%20membro.png">
  <img src="tela%20adm%20-%20novo%20membro.png" alt="Cadastro de novo integrante da equipe" width="900">
</a>

### Caixa — abertura

Tela para iniciar a operação do caixa.

<a href="tela%20adm%20-%20abrir%20o%20caixa.png">
  <img src="tela%20adm%20-%20abrir%20o%20caixa.png" alt="Abertura do caixa" width="900">
</a>

### Caixa — acompanhamento

Consulta da operação com o caixa aberto.

<a href="tela%20adm%20-%20caixa%20aberto.png">
  <img src="tela%20adm%20-%20caixa%20aberto.png" alt="Acompanhamento do caixa aberto" width="900">
</a>

### Pagamento — recebimento da conta

Registro do recebimento do valor referente ao pedido do cliente.

<a href="tela%20adm%20-%20receber%20do%20cliente%20o%20valor%20da%20conta.png">
  <img src="tela%20adm%20-%20receber%20do%20cliente%20o%20valor%20da%20conta.png" alt="Recebimento do pagamento do cliente" width="900">
</a>

### Pagamento — forma de pagamento

Seleção da forma de pagamento para registro do recebimento.

<a href="tela%20adm%20-%20forma%20de%20pagamento.png">
  <img src="tela%20adm%20-%20forma%20de%20pagamento.png" alt="Seleção da forma de pagamento" width="900">
</a>

### Dashboard — resumo do dia

Indicadores de faturamento, pedidos entregues, pedidos em andamento, ticket médio e produtos mais vendidos.

<a href="tela%20adm%20-%20resumo%20do%20dia.png">
  <img src="tela%20adm%20-%20resumo%20do%20dia.png" alt="Dashboard com resumo do dia" width="900">
</a>

## Organização do atendimento

O projeto conecta três áreas da operação:

- **Salão:** registro dos pedidos e acompanhamento pelo garçom.
- **Cozinha:** consulta dos itens e atualização da preparação.
- **Administração:** gerenciamento do cardápio, equipe, caixa e recebimentos.

Essa separação permite que cada perfil tenha uma interface voltada às suas atividades.

## Produtos e categorias

O cardápio é organizado por categorias para facilitar a localização dos produtos no PDV.

O administrador gerencia os cadastros, enquanto o garçom utiliza os itens disponíveis para montar os pedidos.

## Caixa e pagamentos

O módulo de caixa apoia a abertura e o acompanhamento da operação e o registro dos recebimentos.

As formas de pagamento são registradas no sistema. Esse registro não representa integração automática com bancos, Pix ou operadoras de cartão.

## Tecnologias

| Camada | Tecnologias |
|---|---|
| Backend | Python e Flask |
| Persistência | SQLAlchemy e Flask-SQLAlchemy |
| Banco de dados | SQLite |
| Autenticação | Sessões do Flask e hash de senhas com Werkzeug |
| Interface | HTML, CSS e JavaScript |
| Templates | Jinja2 |
| Comunicação com o backend | Endpoints HTTP com dados JSON |
| Versionamento | Git e GitHub |

## Organização do código

O projeto separa os modelos, a configuração e os recursos da interface.

```text
app.py
config.py
models.py
init_db.py
requirements.txt

templates/
├── base.html
├── login.html
├── pdv.html
├── pedidos.html
├── produtos.html
├── categorias.html
├── caixa.html
├── dashboard.html
└── usuarios.html

static/
├── css/
│   └── style.css
└── js/
    ├── app.js
    └── pdv.js
```

- **app.py:** configuração da aplicação, rotas e controle das operações.
- **config.py:** configurações de sessão e banco de dados.
- **models.py:** modelos de usuários, produtos, categorias, pedidos e caixa.
- **init_db.py:** script auxiliar de inicialização do banco.
- **templates:** páginas da interface.
- **static/css:** estilos da aplicação.
- **static/js:** interações da interface e comportamento do PDV.
- **requirements.txt:** dependências Python.

## Aspectos técnicos do projeto

- Modelagem de usuários, categorias, produtos, pedidos e itens.
- Controle de acesso por perfil.
- Separação das interfaces de administração, garçom e cozinha.
- Atualização do status dos pedidos durante o atendimento.
- Associação dos itens ao pedido.
- Registro da situação de pagamento.
- Persistência dos dados em SQLite.
- Operações de caixa e movimentações.
- Indicadores para acompanhamento da operação.

## Próximas etapas

- Concluir os fluxos ainda em desenvolvimento.
- Validar as permissões dos três perfis.
- Testar o ciclo completo de pedido, preparo, entrega e pagamento.
- Validar as notificações de pedidos prontos.
- Revisar as operações de abertura e fechamento de caixa.
- Melhorar o tratamento de erros e a experiência de utilização.

## Execução local

### 1. Clonar o repositório

```bash
git clone https://github.com/LovanGoulart/pizzaria.git
cd pizzaria
```

### 2. Criar um ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual

**Windows — Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows — Prompt de Comando:**

```bat
.venv\Scripts\activate.bat
```

**Linux ou macOS:**

```bash
source .venv/bin/activate
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Iniciar a aplicação

```bash
python app.py
```

### 6. Acessar no navegador

```text
http://localhost:5000
```

O projeto utiliza SQLite. A execução direta possui inicialização das tabelas no código.

### Ambiente de desenvolvimento

A execução direta inicia o servidor de desenvolvimento com depuração habilitada.

Antes de uma publicação em produção, é necessário revisar configurações, chave de sessão, permissões e operações, além de desativar a depuração.

## Autor

Desenvolvido por **Lovan Goulart** como projeto de gestão de atendimento e operação de restaurantes.

[Perfil no GitHub](https://github.com/LovanGoulart)
