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

[SQL]

## Questão 6.2

Domingo. 3319503.57

## Questão 6.3

**1. Por que é necessário utilizar uma tabela de datas (calendário) em vez de agrupar diretamente a tabela de vendas?**

A tabela de vendas só contém registros nos dias em que houve transações — dias sem venda simplesmente não existem nela. Ao agrupar diretamente, o banco de dados considera apenas os dias com movimento, ignorando os dias em que a loja esteve aberta mas não vendeu nada. O calendário resolve isso gerando todas as datas do período, garantindo que cada dia — com ou sem venda — entre no cálculo. Sem ele, a média é calculada sobre uma base menor do que a real, produzindo resultados inflados.

**2. O que aconteceria com a média de vendas se um dia da semana tivesse muitos dias sem nenhuma venda registrada?**

Sem o calendário, esses dias seriam ignorados e a média ficaria artificialmente alta — exatamente o erro cometido pelo estagiário. Por exemplo: se das 8 terças-feiras do período, 4 não tiveram venda, o agrupamento direto calcularia a média sobre apenas 4 dias, não 8. Com o calendário e o `COALESCE`, os 4 dias sem venda entram com valor zero, dividindo o total por 8 e produzindo a média real. Quanto mais dias sem venda um dia da semana tiver, maior será a distorção causada pela ausência do calendário.

# Questão 7

## Questão 7.1

[CÓDIGO]

## Questão 7.2

0 vendas

## Questão 7.3

**1. Como o baseline foi construído?**

A previsão foi calculada como a média das vendas diárias dos 7 dias anteriores — sem incluir o próprio dia previsto. O histórico de vendas foi primeiro transformado em uma série diária completa, com zeros nos dias sem venda, garantindo que a média refletisse o comportamento real do produto. A janela desliza dia a dia: para prever o dia 8, usa os dias 1 a 7; para prever o dia 9, usa os dias 2 a 8, e assim por diante.

**2. Como evitou data leakage?**

O `shift(1)` foi aplicado antes do `rolling` — deslocando a série um dia para frente antes de calcular a média. Isso garante que a previsão de cada dia usa apenas os 7 dias estritamente anteriores, nunca o valor do próprio dia.

**3. Uma limitação do modelo proposto.**

A média móvel assume que o futuro se comporta como a média recente do passado — ignorando sazonalidade, tendências de longo prazo e eventos externos. Para um produto náutico como o Motor de Popa Yamaha, cuja demanda pode variar significativamente entre verão e inverno, esse modelo tende a reagir tarde às mudanças de padrão, suavizando picos e vales que seriam críticos para o planejamento de estoque.

# Questão 8

## Questão 8.1

[CÓDIGO]

## Questão 8.2

94

## Questão 8.3

**1. Como a matriz foi construída?**

As vendas foram agrupadas por cliente e produto, marcando com 1 cada combinação existente — independente de quantas vezes o cliente comprou aquele produto. Em seguida, os dados foram pivotados em uma grade onde cada linha representa um cliente e cada coluna representa um produto. Combinações onde o cliente nunca comprou o produto recebem valor 0. O resultado é uma matriz binária de presença e ausência que representa o comportamento de compra de toda a base de clientes.

**2. O que significa a similaridade de cosseno nesse contexto?**

Cada produto é representado como um vetor de clientes — onde cada posição indica se aquele cliente comprou ou não o produto. A similaridade de cosseno mede o ângulo entre dois vetores: quanto mais clientes em comum dois produtos tiverem, menor o ângulo e maior a similaridade. Um valor de 1.0 significa que os dois produtos foram comprados exatamente pelos mesmos clientes. Um valor de 0.0 significa que nenhum cliente comprou os dois produtos. No contexto da recomendação, um produto com alta similaridade ao GPS Garmin é aquele que tende a ser comprado pelo mesmo perfil de cliente — tornando-o um candidato natural para a vitrine "Quem comprou isso, também levou".

**3. Uma limitação desse método de recomendação.**

O método é baseado apenas em padrões históricos de co-ocorrência — ele não considera o contexto da compra, a ordem das transações, nem a relevância dos produtos entre si. Além disso, sofre do problema de cold start: produtos novos ou com poucas vendas têm vetores esparsos, o que distorce a similaridade e pode gerar recomendações pouco confiáveis. Para uma base pequena como a da LH Nautical, com apenas 49 clientes e 150 produtos, muitas combinações nunca ocorreram — o que limita a qualidade das recomendações.
