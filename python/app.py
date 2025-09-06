#!/usr/bin/env python3
# ===========================================================
# FarmTech Solutions - CLI Python
# ===========================================================
# Requisitos atendidos:
# - 2 culturas: Soja e Milho
#   -> Soja: área calculada como retângulo
#   -> Milho: área calculada como círculo (pivô central)
#
# - Manejo de insumos:
#   1) Aplicação linear: dose em mL/m, número de ruas, comprimento → litros totais
#   2) Aplicação por área: dose em kg/ha ou L/ha → quantidade total (kg ou L)
#
# - Estrutura de dados: uso de vetores (listas de dicionários)
#
# - Funcionalidades do menu:
#   1) Inserir registro
#   2) Listar registros
#   3) Atualizar registro
#   4) Deletar registro
#   5) Exportar CSV (para análise em R)
#   0) Sair
#
# - Requisitos técnicos:
#   * Uso de loops (while, for)
#   * Decisões (if/elif/else)
#   * Persistência parcial via CSV
# ===========================================================

import math
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]  # .../farmtech_solutions
DATA_DIR = ROOT_DIR / "python" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = DATA_DIR / "plantio.csv"

registros = []


# =========================
# Utilidades
# =========================
def input_float(msg):
    while True:
        try:
            v = input(msg).strip().replace(",", ".")
            return float(v)
        except ValueError:
            print("⚠️ Valor inválido. Tente novamente.")


def input_int(msg):
    while True:
        try:
            v = input(msg).strip()
            return int(v)
        except ValueError:
            print("⚠️ Valor inválido. Digite um número inteiro.")


def calc_area_ha(cultura):
    c = cultura.strip().lower()
    if c == "soja":
        base = input_float("Base do talhão (m): ")
        altura = input_float("Altura do talhão (m): ")
        area_m2 = base * altura
    elif c == "milho":
        raio = input_float("Raio do pivô/área circular (m): ")
        area_m2 = math.pi * (raio ** 2)
    else:
        print("Cultura não mapeada — usando retângulo.")
        base = input_float("Base do talhão (m): ")
        altura = input_float("Altura do talhão (m): ")
        area_m2 = base * altura

    area_ha = area_m2 / 10_000.0
    print(f"Área calculada: {area_ha:.4f} ha")
    return area_ha


def inserir_registro():
    print("\n== Inserir registro ==")
    cultura = input("Cultura [Soja/Milho]: ").strip()
    area_ha = calc_area_ha(cultura)
    produto = input("Produto (ex.: fosfato, herbicida X, fertilizante sólido): ").strip()

    # Escolha do tipo de aplicação (com sugestão pelo produto)
    print("\nTipo de aplicação:")
    print("1) Linear: dose em mL/m + ruas/linhas")
    print("2) Por área: dose em kg/ha ou L/ha")

    produto_l = produto.lower()
    default_modo = "2" if "fertiliz" in produto_l else "1"
    modo = input(f"Escolha [1/2] (Enter = {default_modo}): ").strip() or default_modo

    registro = {
        "cultura": cultura.lower(),
        "area_ha": area_ha,
        "produto": produto,
        "aplicacao_tipo": None,
        "dose_ml_m": "",
        "ruas": "",
        "comprimento_m": "",
        "litros_necessarios": "",
        "dose_por_ha": "",
        "unidade_area": "",
        "quantidade_total": ""
    }

    if modo == "1":
        registro["aplicacao_tipo"] = "linear_ml_m"
        dose_ml_m = input_float("Dose (mL por metro): ")
        ruas = input_int("Número de ruas/linhas: ")
        comp = input_float("Comprimento médio de cada rua (m): ")
        total_ml = dose_ml_m * ruas * comp
        registro.update({
            "dose_ml_m": dose_ml_m,
            "ruas": ruas,
            "comprimento_m": comp,
            "litros_necessarios": round(total_ml / 1000.0, 3)
        })

    elif modo == "2":
        registro["aplicacao_tipo"] = "area_ha"
        unidade_sugerida = "kg/ha" if "fertiliz" in produto_l else "L/ha"
        u_in = input(f"Unidade [kg/ha ou L/ha] (Enter = {unidade_sugerida}): ").strip().lower()
        unidade = unidade_sugerida if not u_in else ("kg/ha" if "kg" in u_in else "L/ha")
        dose_ha = input_float(f"Dose ({unidade}): ")
        registro.update({
            "dose_por_ha": dose_ha,
            "unidade_area": unidade,
            "quantidade_total": round(dose_ha * area_ha, 3)
        })
    else:
        print("⚠️ Opção inválida. Cancelando inserção.")
        return

    registros.append(registro)
    print("✅ Registro inserido!")


def listar_registros():
    print("\n== Registros ==")
    if not registros:
        print("(vazio)")
        return
    for i, r in enumerate(registros):
        base = f"[{i}] cultura={r['cultura']}, área={r['area_ha']} ha, produto={r['produto']}"
        if r["aplicacao_tipo"] == "linear_ml_m":
            print(base + f", dose={r['dose_ml_m']} mL/m, ruas={r['ruas']}, comp={r['comprimento_m']} m, litros={r['litros_necessarios']} L")
        elif r["aplicacao_tipo"] == "area_ha":
            print(base + f", dose={r['dose_por_ha']} {r['unidade_area']}, total={r['quantidade_total']} {r['unidade_area'].split('/')[0]}")
        else:
            print(base + " (aplicação desconhecida)")


def atualizar_registro():
    print("\n== Atualizar registro ==")
    if not registros:
        print("(vazio)")
        return
    try:
        idx = int(input("Índice do registro: ").strip())
        r = registros[idx]
    except (ValueError, IndexError):
        print("⚠️ Índice inválido.")
        return

    print("1) Recalcular área")
    print("2) Recalcular insumos")
    print("3) Alterar cultura")
    print("4) Alterar produto")
    print("0) Cancelar")
    op = input("Escolha: ").strip()

    if op == "1":
        r["area_ha"] = calc_area_ha(r["cultura"])
        if r["aplicacao_tipo"] == "area_ha" and r["dose_por_ha"]:
            r["quantidade_total"] = round(r["dose_por_ha"] * r["area_ha"], 3)
        print("✅ Área recalculada.")
    elif op == "2":
        if r["aplicacao_tipo"] == "linear_ml_m":
            dose_ml_m = input_float("Dose (mL por metro): ")
            ruas = input_int("Número de ruas/linhas: ")
            comp = input_float("Comprimento médio de cada rua (m): ")
            total_ml = dose_ml_m * ruas * comp
            r.update({
                "dose_ml_m": dose_ml_m,
                "ruas": ruas,
                "comprimento_m": comp,
                "litros_necessarios": round(total_ml / 1000.0, 3)
            })
        elif r["aplicacao_tipo"] == "area_ha":
            unidade = input("Unidade [kg/ha ou L/ha]: ").strip().lower()
            unidade = "kg/ha" if "kg" in unidade else "L/ha"
            dose_ha = input_float(f"Dose ({unidade}): ")
            r.update({
                "unidade_area": unidade,
                "dose_por_ha": dose_ha,
                "quantidade_total": round(dose_ha * r["area_ha"], 3)
            })
        print("✅ Insumos recalculados.")
    elif op == "3":
        r["cultura"] = input("Nova cultura: ").strip().lower()
    elif op == "4":
        r["produto"] = input("Novo produto: ").strip()
    elif op == "0":
        print("Cancelado.")
    else:
        print("⚠️ Opção inválida.")


def deletar_registro():
    print("\n== Deletar registro ==")
    if not registros:
        print("(vazio)")
        return
    try:
        idx = int(input("Índice do registro: ").strip())
        conf = input(f"Confirma deletar {idx}? [s/N]: ").strip().lower()
        if conf == "s":
            registros.pop(idx)
            print("🗑️ Removido.")
    except (ValueError, IndexError):
        print("⚠️ Índice inválido.")


def exportar_csv(caminho=CSV_PATH):
    import csv
    campos = [
        "cultura", "area_ha", "produto", "aplicacao_tipo",
        "dose_ml_m", "ruas", "comprimento_m", "litros_necessarios",
        "dose_por_ha", "unidade_area", "quantidade_total"
    ]
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for r in registros:
            w.writerow(r)
    print(f"✅ CSV exportado em: {caminho}")


def menu():
    while True:
        print("\n=== FarmTech Solutions (Python) ===")
        print("1) Entrada de dados (inserir registro)")
        print("2) Saída de dados (listar)")
        print("3) Atualização de dados (por índice)")
        print("4) Deleção de dados (por índice)")
        print("5) Exportar CSV para R")
        print("0) Sair")
        op = input("Escolha: ").strip()
        if op == "1": inserir_registro()
        elif op == "2": listar_registros()
        elif op == "3": atualizar_registro()
        elif op == "4": deletar_registro()
        elif op == "5": exportar_csv()
        elif op == "0":
            print("Até mais!")
            break
        else: print("⚠️ Opção inválida.")


if __name__ == "__main__":
    menu()
