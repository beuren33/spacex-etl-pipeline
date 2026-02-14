# SpaceX ETL Pipeline

**Autor:** Matheus Beuren**Versão:** 2.0.0**Data:** 2026-02-14

---

## 1. Visão Geral do Projeto

Este repositório contém um pipeline de ETL (Extract, Transform, Load) projetado para extrair dados da API pública da SpaceX, realizar transformações para análise e carregar os dados resultantes em um banco de dados PostgreSQL. O processo é orquestrado pelo Apache Airflow e totalmente containerizado com Docker, garantindo portabilidade e consistência entre ambientes.

O objetivo principal é demonstrar uma arquitetura de engenharia de dados robusta, escalável e pronta para produção, utilizando ferramentas e práticas modernas. O projeto inclui automação de CI/CD para validação de código e distribuição de imagens Docker.

---

## 2. Arquitetura e Decisões Técnicas

A arquitetura foi projetada para ser modular, escalável e alinhada com as melhores práticas de MLOps e DataOps. Abaixo estão detalhadas as principais decisões técnicas e suas justificativas.

### 2.1. Orquestração com Apache Airflow e Astro CLI

**Decisão:** Utilizar o **Astro CLI** da Astronomer para gerenciamento do ambiente de desenvolvimento local do Apache Airflow, em vez de uma configuração manual com `docker-compose`.

**Justificativa Técnica:**

- **Ambiente de Produção Simulado:** O Astro CLI provisiona um ambiente multi-container (webserver, scheduler, triggerer, postgres) que espelha fielmente uma arquitetura de produção do Airflow. Uma configuração manual com `docker-compose` frequentemente resulta em um ambiente monolítico (`airflow standalone`) que não é representativo e pode ocultar problemas de integração.

- **Validação e Testes Integrados:** Ferramentas como `astro dev parse` e `astro dev pytest` permitem a validação da integridade dos DAGs e a execução de testes unitários dentro do contexto do container Airflow, garantindo que as dependências e configurações sejam as mesmas do ambiente de execução. Isso reduz drasticamente a probabilidade de erros em produção que não foram detectados localmente.

- **Gerenciamento de Dependências:** O Astro Runtime, imagem base utilizada, vem com a maioria dos providers comuns pré-instalados e otimizados, simplificando o gerenciamento de dependências e garantindo compatibilidade. A adição de pacotes de sistema operacional (`packages.txt`) e Python (`requirements.txt`) é gerenciada de forma padronizada.

### 2.2. Containerização com Docker

**Decisão:** Containerizar todos os componentes da aplicação (Airflow, PostgreSQL,) utilizando Docker.

**Justificativa Técnica:**

- **Reprodutibilidade e Consistência:** O Docker garante que o ambiente de desenvolvimento seja idêntico ao ambiente de produção, eliminando o clássico problema "funciona na minha máquina". Todas as dependências, configurações e versões de software são encapsuladas na imagem Docker.

- **Portabilidade:** O projeto pode ser executado em qualquer sistema que suporte Docker (Windows, macOS, Linux) sem a necessidade de instalar e configurar manualmente cada componente (Python, PostgreSQL, etc.).

- **Isolamento:** Cada serviço roda em seu próprio container, com suas próprias dependências e rede, prevenindo conflitos e garantindo a segurança entre os componentes.

### 2.3. Pipeline de CI/CD com GitHub Actions

**Decisão:** Implementar um pipeline de CI/CD automatizado utilizando GitHub Actions.

**Justificativa Técnica:**

- **Continuous Integration (CI):** O workflow de CI é acionado a cada `push` ou `pull request`, executando uma série de validações críticas:
    1. **Análise Estática de Código:** Ferramentas como `flake8` e `black` garantem a qualidade e o padrão do código.
    1. **Validação de DAGs:** `astro dev parse` verifica a sintaxe e a integridade dos DAGs, prevenindo a introdução de DAGs quebrados na base de código.
    1. **Testes Unitários:** `astro dev pytest` executa testes para a lógica de negócio (extração, transformação), garantindo que as funções se comportem como esperado.

- **Continuous Deployment (CD):** Após a validação do CI, o workflow de CD é acionado em merges para a branch `main`:
    1. **Build da Imagem Docker:** Constrói a imagem da aplicação com todas as dependências.
    1. **Publicação no Docker Hub:** Envia a imagem para um registro público (Docker Hub), tornando-a disponível para distribuição.
    1. **Versionamento:** A imagem é tagueada com o SHA do commit e a tag `latest`, permitindo o uso de versões específicas e facilitando rollbacks.

### 2.4. Estrutura de Diretórios Padronizada

**Decisão:** Adotar a estrutura de diretórios recomendada pelo Astro CLI.

**Justificativa Técnica:**

- **Clareza e Manutenibilidade:** A separação de responsabilidades (`dags/`, `include/`, `plugins/`, `tests/`) torna o projeto mais fácil de navegar e manter. O código fonte da aplicação reside em `include/src`, que é adicionado ao `PYTHONPATH` do Airflow, permitindo importações modulares e limpas dentro dos DAGs.

- **Padrão de Mercado:** Esta estrutura é um padrão de fato em projetos Airflow profissionais, facilitando a colaboração e a integração de novos desenvolvedores.

---

## 3. Estrutura do Projeto

```
spacex-etl-pipeline/
├── .github/workflows/      
│   ├── ci.yml
│   └── cd.yml
├── dags/                   
│   └── spacex_etl_dag.py
├── include/                
│   ├── config/             
│   └── src/                
├── tests/                  
├── .dockerignore           
├── .gitignore              
├── Dockerfile              
├── docker-compose.yml      
├── airflow_settings.yaml   
└── requirements.txt        
```

---

## 4. Instruções de Execução

Existem duas maneiras de executar este projeto: para desenvolvimento local ou para execução a partir da imagem distribuída.

### 4.1. Desenvolvimento Local (Recomendado)

Este modo é ideal para desenvolver e testar DAGs.

**Pré-requisitos:**

- Docker Desktop

- Astro CLI (`curl -sSL install.astronomer.io | sudo bash -s`)

**Passos:**

1. Clone o repositório:

   ```bash
   git clone https://github.com/beuren33/spacex-etl-pipeline.git
   cd spacex-etl-pipeline
   ```

1. Inicie o ambiente Airflow:

   ```bash
   astro dev start
   ```

1. Acesse a UI do Airflow em `http://localhost:8080` (login: `admin`/`admin` ).

1. Para parar o ambiente, execute `astro dev stop`.

### 4.2. Execução via Docker Hub (Distribuição)

Este modo utiliza a imagem pré-construída do Docker Hub e é ideal para executar o projeto sem a necessidade de um ambiente de desenvolvimento.

**Pré-requisitos:**

- Docker Desktop

- Docker Compose

**Passos:**

1. Crie um diretório e baixe o arquivo `docker-compose.yml`:

   ```bash
   mkdir spacex-production && cd spacex-production
   curl -O https://raw.githubusercontent.com/beuren33/spacex-etl-pipeline/main/docker-compose.yml
   ```

1. Inicie os serviços:

   ```bash
   docker-compose up -d
   ```

1. Acesse a UI do Airflow em `http://localhost:8080` (login: `admin`/`admin` ).

---

## 5. Tecnologia Utilizadas

| Categoria | Tecnologia | Justificativa |
| --- | --- | --- |
| **Orquestração** | Apache Airflow 2.8+ | Padrão de mercado para orquestração de workflows de dados. |
| **Desenvolvimento** | Astro CLI | Abstrai a complexidade do Docker e simula um ambiente de produção. |
| **Containerização** | Docker, Docker Compose | Garante reprodutibilidade e portabilidade. |
| **CI/CD** | GitHub Actions | Integração nativa com o GitHub, automação de testes e deploy. |
| **Linguagem** | Python 3.11 | Linguagem principal para scripting de dados e desenvolvimento de DAGs. |
| **Banco de Dados** | PostgreSQL 13 | Banco de dados relacional robusto e amplamente utilizado. |
|  |
| **Registro** | Docker Hub | Registro público para distribuição de imagens Docker. |

