"""Carrega o CSV num SQLite em memória, roda as consultas de queries.sql e gera reports/summary.md."""
import csv, re, sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE enrollments (id INTEGER, employee_id INTEGER, department TEXT, course TEXT, enrolled_at TEXT, status TEXT)")
with open("data/enrollments.csv", encoding="utf-8") as f:
    rows = list(csv.reader(f))[1:]
con.executemany("INSERT INTO enrollments VALUES (?,?,?,?,?,?)", rows)

blocks = re.split(r"-- name: (\w+)\n", open("queries.sql", encoding="utf-8").read())[1:]
out = ["# Resumo das inscrições (dados fictícios)\n"]
for name, sql in zip(blocks[::2], blocks[1::2]):
    cur = con.execute(sql.strip().rstrip(";"))
    cols = [c[0] for c in cur.description]
    out.append(f"\n## {name.replace('_', ' ')}\n")
    out.append("| " + " | ".join(cols) + " |")
    out.append("|" + "---|" * len(cols))
    for r in cur.fetchall():
        out.append("| " + " | ".join(str(x) for x in r) + " |")

open("reports/summary.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
