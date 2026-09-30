"""Gera dados FICTÍCIOS e propositalmente SUJOS de inscrições (nenhum dado real de empresa)."""
import csv, random, unicodedata
from datetime import date, timedelta

random.seed(42)
DEPTS = ["TI", "RH", "Financeiro", "Operações", "Comercial", "Logística"]
COURSES = ["Excel Avançado", "Power BI", "Inglês Corporativo", "Liderança", "Segurança da Informação", "Comunicação"]
STATUS = ["concluído"] * 6 + ["em andamento"] * 3 + ["desistiu"]

def plain(t): return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()

def mess(v):  # 20% dos valores chegam com caixa, acento ou espaços diferentes
    if random.random() < .8: return v
    return random.choice([v.lower(), v.upper(), f" {v} ", plain(v), plain(v).lower()])

rows = []
for i in range(1, 581):
    d = date(2025, 2, 1) + timedelta(days=random.randint(0, 180))
    ds, r = d.isoformat(), random.random()
    if r < .06: ds = d.strftime("%d/%m/%Y")                       # formato diferente
    elif r < .09: ds = random.choice(["31/02/2025", "", "2025-13-01"])  # data inválida
    emp = "" if random.random() < .03 else random.randint(1000, 1150)
    dep = random.choice(DEPTS)
    dep = "T.I." if dep == "TI" and random.random() < .2 else mess(dep)
    st = "" if random.random() < .02 else mess(random.choice(STATUS))
    rows.append([i, emp, dep, mess(random.choice(COURSES)), ds, st])
for k in range(40):                                                # duplicatas com id novo
    r = list(random.choice(rows)); r[0] = 581 + k; rows.append(r)

with open("raw_enrollments.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "employee_id", "department", "course", "enrolled_at", "status"]); w.writerows(rows)
print(f"raw_enrollments.csv gerado ({len(rows)} linhas, com sujeira de propósito)")
