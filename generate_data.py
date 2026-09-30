"""Gera dados FICTÍCIOS de inscrições em cursos (nenhum dado real de empresa)."""
import csv, random
from datetime import date, timedelta

random.seed(42)
COURSES = ["Excel Avançado", "Power BI", "Inglês Corporativo", "Liderança", "Segurança da Informação", "Comunicação"]
DEPTS = ["TI", "RH", "Financeiro", "Operações", "Comercial", "Logística"]
STATUS = ["concluído"] * 6 + ["em andamento"] * 3 + ["desistiu"]
START = date(2025, 2, 1)

with open("data/enrollments.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "employee_id", "department", "course", "enrolled_at", "status"])
    for i in range(1, 401):
        d = START + timedelta(days=random.randint(0, 180))
        w.writerow([i, random.randint(1000, 1150), random.choice(DEPTS),
                    random.choice(COURSES), d.isoformat(), random.choice(STATUS)])
print("data/enrollments.csv gerado (400 linhas)")
