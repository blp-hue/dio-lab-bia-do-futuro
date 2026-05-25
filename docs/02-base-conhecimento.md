# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Como a Lyra utiliza? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações e orçamento de meses futuros |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente com histórico de compra de cada um |


## Adaptações nos Dados

> Os dados de produtos financeiros disponíveis não foi preciso, pois não faz parte do objetivo da Lyra

---

## Estratégia de Integração

### Como os dados são carregados?
> Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt


### Como os dados são usados no prompt?

``` text

DADOS DO CLIENTE:


PERFIL DO CLIENTE:


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
```
---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Serviços e produtos utilizados no mês:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55

Serviços e produtos recorrentes:
- Streaming
- Supermercado
- Protetor solar
- Passagem de ônibus
```
