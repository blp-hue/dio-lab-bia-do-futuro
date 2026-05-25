# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

## Estrutura Sugerida

```
src/
├── app.py                    # Interface Streamlit (chat + sidebar)
├── agente.py                 # Carregamento de dados + system prompt + Ollama
├── config.py                 # URL, modelo e caminhos configuráveis
├── requirements.txt          # streamlit, pandas, requests

```

## Exemplo de requirements.txt

```
streamlit
pandas
requests
```

## Como Rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Garantir que o Ollama está rodando
ollama serve
ollama pull llama3   # só na primeira vez

# 3. Entrar na pasta e rodar
cd src
streamlit run app.py
```
