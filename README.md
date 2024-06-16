# CineMatch - Back

Este projeto consiste no back-end do CineMatch, uma aplicação de recomendação de filmes e séries.

## Pré-Requisitos

É recomendado (talvez obrigatório rs) que você tenha instalado em sua máquina:

-   Python (>= 3.12.3)
-   PyEnv (para gerenciar diferentes versões python)
-   Poetry (gerenciamento de pacotes)
-   Pip
-   Docker e docker compose(Opcional porem recomendado)

## Como rodar o projeto

1. Caso não tenha a versão certa do Python, instalar o pyenv

```bash
curl https://pyenv.run | bash
```

2. Instalar o poetry

```bash
pip install poetry
```

3. Instalar as dependencias do projeto

```bash
poetry install
```

4. Rodar o projeto
   É possível rodar direto com um comando do poetry:

```bash
poetry run uvicorn --host 0.0.0.0 cinematch_back.app:app
```

Ou com a seguinte combinação:

-   Entrando no shell do ambiente virtual do poetry

```bash
poetry shell
```

-   Rodando o comando simplificado:

```bash
task run
```

5. Acesse a documentação interativo do Swagger no link [http://127.0.0.1:8000/docs]

## Observações

O projeto foi configurado para rodar com Docker. Você pode simplesmente usar um container docker para facilitar o processo.

```bash
docker compose up --build
```

E ser feliz testando a documentação.
