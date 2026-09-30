# HR Enrollment Analytics (Python + SQL)

Pipeline de dados de ponta a ponta sobre inscrições em cursos corporativos, inspirado no problema que resolvi com automação no RH: sair de planilhas manuais e chegar a números confiáveis para decisão.

> **Todos os dados são fictícios**, gerados por `generate_data.py`, e propositalmente sujos. Nenhuma informação real de empresa foi usada.

## O pipeline
1. `generate_data.py` gera 620 inscrições brutas em `raw_enrollments.csv`, com nomes escritos de formas diferentes, datas inválidas, campos vazios e duplicatas.
2. `analyze.py` limpa os dados e registra cada regra aplicada (o que foi descartado e o que foi corrigido), grava tudo em `enrollments.db` (tabelas `raw_enrollments` e `enrollments`) e executa `queries.sql`.
3. Saídas: `summary.md` (consultas e relatório de qualidade) e `dashboard_data.json`, que alimenta o dashboard do meu portfólio.

## Resultados (dados fictícios)
- 620 linhas brutas viram 547 limpas: 39 duplicatas, 16 sem colaborador, 9 datas inválidas e 9 valores não reconhecidos foram descartados, e 259 valores foram normalizados.
- Operações tem a maior taxa de conclusão (69,4%) e Financeiro a menor (55,9%).
- Inglês Corporativo é o curso com mais inscrições (109).

## Como rodar
Requer apenas Python 3.9+ (biblioteca padrão). Todos os arquivos ficam na mesma pasta:

```bash
python generate_data.py
python analyze.py
```

## Tecnologias
Python (csv, sqlite3, re, unicodedata), SQL (GROUP BY, agregações, ORDER BY, LIMIT), tratamento e qualidade de dados.

## Próximos passos
- Dashboard no Power BI usando o mesmo banco
- Testes automatizados das regras de limpeza
