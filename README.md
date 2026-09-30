# HR Enrollment Analytics (Python + SQL)

Mini-projeto de análise de inscrições em cursos corporativos, inspirado no problema que resolvi com automação no RH: sair de planilhas manuais e passar a ter números confiáveis para decisão.

> **Todos os dados são fictícios**, gerados por `generate_data.py`. Nenhuma informação real de empresa foi usada.

## O que faz
1. `generate_data.py` gera 400 inscrições fictícias em `data/enrollments.csv`.
2. `analyze.py` carrega o CSV em um SQLite (em memória) e executa as consultas de `queries.sql`.
3. O resultado sai no terminal e em `reports/summary.md`.

## Perguntas respondidas
- Quais cursos têm mais inscrições?
- Qual a taxa de conclusão por departamento?
- Como as inscrições evoluem mês a mês?
- Quem são os colaboradores mais ativos?

## Como rodar
Requer apenas Python 3.9+ (biblioteca padrão, sem instalar nada):

```bash
python generate_data.py
python analyze.py
```

## Tecnologias
Python (csv, sqlite3, re), SQL (GROUP BY, agregações, ORDER BY, LIMIT).

## Próximos passos
- Gráficos com matplotlib
- Dashboard no Power BI usando o mesmo CSV
- Testes automatizados
