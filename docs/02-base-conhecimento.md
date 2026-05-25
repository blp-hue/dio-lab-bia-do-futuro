# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Como a Lyra utiliza? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_cliente.json` | JSON | Personalizar recomendações e orçamento de meses futuros |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente com histórico de compra de cada um |


## Adaptações nos Dados

> Os dados de produtos financeiros disponíveis não foi preciso, pois não faz parte do objetivo da Lyra

---

## Estratégia de Integração

### Como os dados são carregados?
> Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt


### Como os dados são usados no prompt?

``` text

PERFIL DO CLIENTE:
{
  "nome": "Julia Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "orçamento_mensal": 4000.00,
  "meta_de_reserva_mensal": 500.00,
  "metas": [
    {
      "meta": "Organizar orçamento mensal",
      "valor_necessario": 4000
    },
    {
      "meta": "Projeção de gastos com skincare",
      "valor_necessario": 300
    },
    {
      "meta": "Depósito mensal de reserva",
      "valor_necessário": 500
    }
  ]
}

TRANSAÇÕES DO CLIENTE: 
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

HITÓRICO DE ATENDIMENTO DO CLIENTE:
data,canal,tema,resumo,resolvido
2025-09-15,chat,Streamng,Cliente perguntou sobre gastos e prazos das assinaturas,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Reserva Mensal,Cliente pediu explicação sobre quanto deveria destinar à reserva mensal,sim
2025-10-12,chat,Reserva Mensal,Cliente acompanhou o progresso da reserva mensal,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim

```
---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: Julia Silva
- Saldo disponível: R$ 5.000
- Orçamento requerido: R$ 4.000
- Valor para reserva mensal: R$ 500

Serviços e produtos utilizados no mês:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
- 06/11: Protetor solar - R$ 45

Serviços e produtos recorrentes:
- Streaming
- Supermercado
- Protetor solar
- Passagem de ônibus
```
