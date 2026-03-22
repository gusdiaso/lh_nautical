# Questão 1

## Questão 1.1

[SQL]

## Questão 1.2

O valor máximo registrado na coluna `total` é **R$ 2.222.973,00**.

## Questão 1.3

O dataset possui 9.895 registros sem valores nulos — ponto positivo. Porém, dois problemas impedem seu uso direto:

**Inconsistência de datas:** a coluna `sale_date` mistura dois formatos (`YYYY-MM-DD` e `DD-MM-YYYY`), o que pode corromper análises temporais silenciosamente sem gerar erros visíveis.

**Outliers em `total`:** pelo método IQR, 1.018 registros (10,29%) estão acima de R$ 813.028. O valor R$ 2.222.973 aparece repetido diversas vezes — estatisticamente improvável em vendas orgânicas. Antes de qualquer tratamento, recomendo validar com o time de negócio se são contratos corporativos legítimos ou erros de importação.

**Conclusão:** o dataset exige dois tratamentos prévios — padronização do formato de datas e investigação dos outliers — antes de ser utilizado em análises ou modelos.

---

# Questão 2

## Questão 2.1

`02_etl_produtos.ipynb`

## Questão 2.2

Foram removidos **7 registros duplicados** pelo campo `code`, reduzindo o dataset de 157 para 150 linhas. A estratégia `keep='first'` foi utilizada — mantendo o primeiro registro de cada código duplicado.

---

# Questão 3

## Questão 3.1

`03_etl_custos_importacao.ipynb`

## Questão 3.2

Após a normalização do campo `historic_data` — expandindo cada entrada do histórico em uma linha individual — o dataset resultou em **1.260 registros**, com média de 8,4 entradas por produto.

---

# Questão 4

## Questão 4.1

[SQL]

## Questão 4.2

O produto com maior percentual de prejuízo sobre a receita foi o **ID 72**, com **63,15% de perda** — mais da metade do faturamento desse produto foi consumido pelo custo de importação.

## Questão 4.3

**Câmbio utilizado:**
Média da cotação de venda do dólar do dia da venda, via API PTAX do Banco Central (`CotacaoDolarDia`). Para feriados e fins de semana, foi utilizado o câmbio do último dia útil anterior. O câmbio foi cacheado por data única para evitar chamadas repetidas à API.

**Definição de prejuízo:**
`prejuízo = (usd_price_vigente × câmbio_do_dia × qtd) − total_venda`
Quando positivo, o custo de importação superou o valor recebido pela venda.

**Suposições relevantes:**

- Custo vigente = último `usd_price` com `start_date ≤ sale_date` — sem interpolação
- Produtos sem histórico anterior à data da venda foram desconsiderados
- Impostos e frete ignorados conforme premissa — o prejuízo real pode ser ainda maior

# Questão 5

## Questão 5.1

[SQL]

## Questão 5.2

propulsão

## Questão 5.3

**1. Como você realizou a limpeza das categorias?**

As categorias apresentavam 39 variações para apenas 3 categorias reais. Para normalizar, foram extraídos todos os valores únicos da coluna `actual_category` e criado um dicionário mapeando cada variação para sua categoria correta — por exemplo, `"Ancorajen"`, `"Encoragem"` e `"A N C O R A G E M"` foram todas mapeadas para `"ancoragem"`. O mapeamento foi assistido por IA para garantir que nenhuma variação fosse esquecida. Com o dicionário completo, o `map()` foi aplicado sobre a coluna, substituindo cada valor pela categoria padronizada correspondente.

**2. Qual lógica utilizou para filtrar os clientes com diversidade mínima?**

Após cruzar as vendas com o catálogo de produtos, foi contado o número de categorias distintas compradas por cada cliente. Somente clientes que compraram produtos de pelo menos 3 categorias diferentes foram considerados no ranking — garantindo que o critério de fidelidade reflita não apenas volume de gasto, mas também amplitude de consumo dentro da loja.

**3. Como garantiu que a contagem de itens refletisse apenas os Top 10?**

Após identificar os 10 clientes com maior ticket médio, as vendas foram filtradas para incluir exclusivamente as transações desse grupo. Somente então foi feita a agregação por categoria — garantindo que o resultado represente o comportamento de compra específico dos clientes elite, sem contaminação do restante da base.

# Questão 6

## Questão 6.1
