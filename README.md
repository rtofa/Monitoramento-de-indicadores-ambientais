
# 🌍 Projeto de Monitoramento da Qualidade do Ar

## Descrição

Este projeto foi desenvolvido para monitorar a qualidade do ar em diversas localidades ao redor do mundo, emitindo alertas e recomendações especialmente voltados para pessoas com problemas respiratórios. Ele coleta dados de qualidade do ar (AQI - Índice de Qualidade do Ar) em tempo real, com informações baseadas em localização (país, estado e cidade), e oferece sugestões para reduzir os impactos à saúde em ambientes poluídos.

Este projeto está em fase de expansão para uma aplicação web e futura versão móvel, permitindo que o usuário acesse informações e receba notificações onde estiver!

---

## 🚀 Recursos e Funcionalidades

- **Monitoramento de Qualidade do Ar**: Obtenção de dados de AQI de diversas localidades.
- **Alerta de Qualidade do Ar**: Notificação quando o AQI ultrapassa limites seguros.
- **Sugestões de Localidade Próxima**: Para localidades onde a qualidade do ar não está disponível, o sistema sugere uma localização próxima.
- **Recomendações Personalizadas**: Orientações para pessoas com problemas respiratórios, com níveis de AQI recomendados.

---

## 📦 Estrutura do Projeto

```
Projeto-monitoramento/
│
├── src/
│   ├── main.py               # Arquivo principal
│   ├── scraping.py           # Coleta de dados da API de qualidade do ar
│   ├── db_connection.py      # Conexão e manipulação com banco de dados
│   ├── exceptions.py         # Definições de exceções personalizadas
│   └── utils.py              # Funções auxiliares e validações
│
├── requirements.txt          # Dependências do projeto
├── README.md                 # Documentação do projeto
└── database/
    └── setup.sql             # Script para criação das tabelas no banco de dados
```

---

## 🛠️ Configuração e Execução

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/projeto-monitoramento.git
cd projeto-monitoramento
```

### 2. Instale as Dependências

Instale as bibliotecas listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

Para armazenar dados de qualidade do ar, configure um banco de dados MySQL:

1. Crie um banco de dados chamado `ar_saude`.
2. Execute o script `setup.sql` localizado em `database/` para configurar as tabelas.

### 4. Configuração da API

Substitua a chave da API `API_KEY` em `scraping.py` com sua chave pessoal da [AirVisual API](https://www.iqair.com/).

### 5. Executando a API localmente

Para rodar a API localmente, execute o seguinte comando no terminal:

```bash
uvicorn src.main:app --reload
```
A API estará disponível em http://localhost:8000. Você pode testar os endpoints utilizando o Postman ou integrando a uma aplicação front-end em Angular, conforme instruções mais detalhadas na seção de uso.
 
---
## 🌐 Uso

### Endpoints Disponíveis

1. Consulta de Qualidade do Ar: Retorna o AQI da localidade selecionada e recomendações de segurança.

2. Cadastro de Usuário: Endpoint para criação de novos usuários.
3. Login de Usuário: Endpoint para autenticação de usuários.

---

## 🚨 Alertas e Recomendações

A aplicação classifica o AQI em diferentes níveis de segurança, como:

- **Boa (0-50)**: Qualidade do ar excelente; seguro para atividades ao ar livre.
- **Moderada (51-100)**: Pessoas sensíveis devem considerar reduzir atividades ao ar livre.
- **Ruim (>100)**: Qualidade do ar perigosa; recomenda-se evitar atividades externas.

---

## 🌈 Expansão do Projeto

### Web e Mobile

Este projeto será expandido com um front-end web e, futuramente, uma aplicação móvel.

- **Web**: Utilização de **Angular** ou **React** para fornecer uma interface de fácil acesso.
- **Mobile**: Planejado para desenvolvimento em **React Native** ou **Flutter**, oferecendo acesso contínuo aos dados de qualidade do ar.

---

## 🧩 Exceções e Tratamento de Erros

Para garantir robustez, o projeto conta com tratamentos de exceções personalizados em `exceptions.py`. Alguns dos tratamentos incluem:

- **Localidade sem Monitoramento**: Se uma cidade, estado ou país não tiver dados disponíveis, uma mensagem informativa é exibida.
- **Erro de Conexão**: Caso a API ou banco de dados estejam indisponíveis, o sistema lida com esses erros e notifica o usuário.
- **Sugestões para Localidades Próximas**: O sistema tenta sugerir cidades próximas com dados disponíveis.

---

## 📈 Futuro do Projeto

- **Monitoramento de Longo Prazo**: Análise de dados históricos de qualidade do ar.
- **Notificações em Tempo Real**: Alertas por e-mail ou notificações push para usuários registrados.
- **Dashboard Interativo**: Para visualização de dados e histórico da qualidade do ar.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests para aprimorar o projeto.

1. **Fork** o projeto
2. Crie sua **branch** para a nova feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adicionei MinhaFeature'`)
4. Faça o **push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

---

## 📜 Licença

Este projeto está licenciado sob a [Licença Apache 2.0](LICENSE).

---

**Desenvolvido com paixão para proteger nossa saúde e planeta.** 🌍💚
