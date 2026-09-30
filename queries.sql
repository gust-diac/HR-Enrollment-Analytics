-- name: inscricoes_por_curso
SELECT course AS curso, COUNT(*) AS inscricoes
FROM enrollments GROUP BY course ORDER BY inscricoes DESC;

-- name: conclusao_por_departamento
SELECT department AS departamento,
       COUNT(*) AS total,
       ROUND(100.0 * SUM(status = 'concluído') / COUNT(*), 1) AS pct_concluido
FROM enrollments GROUP BY department ORDER BY pct_concluido DESC;

-- name: inscricoes_por_mes
SELECT substr(enrolled_at, 1, 7) AS mes, COUNT(*) AS inscricoes
FROM enrollments GROUP BY mes ORDER BY mes;

-- name: colaboradores_mais_ativos
SELECT employee_id AS colaborador, COUNT(*) AS cursos
FROM enrollments GROUP BY employee_id ORDER BY cursos DESC, colaborador LIMIT 5;
