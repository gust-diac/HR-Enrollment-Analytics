"""Pipeline: CSV bruto -> limpeza (com log) -> SQLite -> consultas SQL -> summary.md + dashboard_data.json"""
import csv, json, re, sqlite3, unicodedata
from datetime import datetime

def norm(t): return re.sub(r"[^a-z0-9 ]", "", unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()).strip()
DEPT = {norm(x): x for x in ["TI", "RH", "Financeiro", "Operações", "Comercial", "Logística"]}
COURSE = {norm(x): x for x in ["Excel Avançado", "Power BI", "Inglês Corporativo", "Liderança", "Segurança da Informação", "Comunicação"]}
STATUS = {norm(x): x for x in ["concluído", "em andamento", "desistiu"]}

def parse(s):
    for f in ("%Y-%m-%d", "%d/%m/%Y"):
        try: return datetime.strptime(s.strip(), f).date().isoformat()
        except ValueError: pass

# 1) limpeza: cada regra conta o que descartou ou corrigiu
raw = sorted(list(csv.reader(open("raw_enrollments.csv", encoding="utf-8")))[1:], key=lambda r: int(r[0]))
log = dict(raw=len(raw), miss=0, date=0, unk=0, dup=0, fixed=0)
clean, seen = [], set()
for i, e, d, c, dt, s in raw:
    if not e.strip(): log["miss"] += 1; continue
    day = parse(dt)
    if not day: log["date"] += 1; continue
    D, C, S = DEPT.get(norm(d)), COURSE.get(norm(c)), STATUS.get(norm(s))
    if not (D and C and S): log["unk"] += 1; continue
    if (e, C, day) in seen: log["dup"] += 1; continue
    seen.add((e, C, day))
    log["fixed"] += (D, C, S, day) != (d, c, s, dt)
    clean.append((int(i), int(e), D, C, day, S))
log["clean"] = len(clean)

# 2) banco: tabela bruta e tabela tratada
con = sqlite3.connect("enrollments.db")
con.executescript("DROP TABLE IF EXISTS raw_enrollments; DROP TABLE IF EXISTS enrollments;"
                  "CREATE TABLE raw_enrollments(id, employee_id, department, course, enrolled_at, status);"
                  "CREATE TABLE enrollments(id INTEGER PRIMARY KEY, employee_id INTEGER, department TEXT, course TEXT, enrolled_at TEXT, status TEXT);")
con.executemany("INSERT INTO raw_enrollments VALUES (?,?,?,?,?,?)", raw)
con.executemany("INSERT INTO enrollments VALUES (?,?,?,?,?,?)", clean); con.commit()

# 3) consultas -> summary.md
out = ["# Resumo das inscrições (dados fictícios)\n", "\n## qualidade dos dados\n", "| etapa | linhas |", "|---|---|",
       f"| linhas brutas | {log['raw']} |", f"| sem employee_id | -{log['miss']} |", f"| datas inválidas | -{log['date']} |",
       f"| valores não reconhecidos | -{log['unk']} |", f"| duplicatas | -{log['dup']} |", f"| linhas limpas | {log['clean']} |",
       f"| valores normalizados (caixa, acento, formato de data) | {log['fixed']} |"]
blocks = re.split(r"-- name: (\w+)\n", open("queries.sql", encoding="utf-8").read())[1:]
for name, sql in zip(blocks[::2], blocks[1::2]):
    cur = con.execute(sql.strip().rstrip(";")); cols = [c[0] for c in cur.description]
    out += [f"\n## {name.replace('_', ' ')}\n", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in cur.fetchall()]
open("summary.md", "w", encoding="utf-8").write("\n".join(out) + "\n")

# 4) dados agregados que alimentam o dashboard (departamento x curso x mês)
DP, CS, MS = list(DEPT.values()), list(COURSE.values()), ["2025-0%d" % i for i in range(2, 8)]
T, Dn, X = [0] * 216, [0] * 216, [0] * 216
for _, _, d, c, day, s in clean:
    k = DP.index(d) * 36 + CS.index(c) * 6 + MS.index(day[:7]); T[k] += 1; Dn[k] += s == "concluído"; X[k] += s == "desistiu"
json.dump({"T": T, "D": Dn, "X": X, "log": log}, open("dashboard_data.json", "w"), separators=(",", ":"))
print("\n".join(out))
