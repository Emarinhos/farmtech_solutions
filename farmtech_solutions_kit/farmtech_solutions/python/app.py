#!/usr/bin/env python3
# FarmTech Solutions - CLI Python
# Requisitos atendidos:
# - 2 culturas (Soja e Milho)
# - Área: Soja=retângulo; Milho=círculo (pivô)
# - Manejo de insumos: mL/m, nº de ruas, comprimento -> litros totais
# - Vetores (listas)
# - Menu: inserir/listar/atualizar/deletar/exportar/sair
# - Loops e decisões

import math
import csv
from typing import List, Dict
from pathlib import Path
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


registros: List[Dict] = []

def calc_area_hectares(cultura: str) -> float:
    if cultura.lower() == "soja":
        while True:
            try:
                base = float(input("Base do talhão (m): ").replace(",", "."))
                altura = float(input("Altura do talhão (m): ").replace(",", "."))
                area_m2 = base * altura
                return area_m2 / 10_000.0
            except ValueError:
                print("⚠️ Valores inválidos. Tente novamente.")
    elif cultura.lower() == "milho":
        while True:
            try:
                raio = float(input("Raio do pivô/área circular (m): ").replace(",", "."))
                area_m2 = math.pi * (raio ** 2)
                return area_m2 / 10_000.0
            except ValueError:
                print("⚠️ Valores inválidos. Tente novamente.")
    else:
        print("Cultura desconhecida, usando retângulo.")
        while True:
            try:
                base = float(input("Base do talhão (m): ").replace(",", "."))
                altura = float(input("Altura do talhão (m): ").replace(",", "."))
                area_m2 = base * altura
                return area_m2 / 10_000.0
            except ValueError:
                print("⚠️ Valores inválidos. Tente novamente.")

def calc_insumos() -> Dict[str, float]:
    produto = input("Produto (ex.: fosfato, herbicida X): ").strip()
    while True:
        try:
            dose_ml_m = float(input("Dose (mL por metro): ").replace(",", "."))
            ruas = int(input("Número de ruas/linhas: "))
            comp_m = float(input("Comprimento médio de cada rua (m): ").replace(",", "."))
            total_ml = dose_ml_m * ruas * comp_m
            total_l = total_ml / 1000.0
            return {
                "produto": produto,
                "dose_ml_m": dose_ml_m,
                "ruas": ruas,
                "comp_m": comp_m,
                "litros_necessarios": total_l,
            }
        except ValueError:
            print("⚠️ Valores inválidos. Tente novamente.")

def inserir_registro():
    print("\n== Inserir registro ==")
    while True:
        cultura = input("Cultura [Soja/Milho]: ").strip().lower()
        if cultura in ("soja", "milho"):
            break
        print("⚠️ Opção inválida. Digite 'Soja' ou 'Milho'.")
    area_ha = calc_area_hectares(cultura)
    print(f"Área calculada: {area_ha:.4f} ha")
    ins = calc_insumos()
    registro = {"cultura": cultura, "area_ha": round(area_ha, 6), **ins}
    registros.append(registro)
    print("✅ Registro inserido!")

def listar_registros():
    print("\n== Registros ==")
    if not registros:
        print("(vazio)")
        return
    for i, r in enumerate(registros):
        print(f"[{i}] cultura={r['cultura']}, área={r['area_ha']} ha, "
              f"produto={r['produto']}, dose={r['dose_ml_m']} mL/m, "
              f"ruas={r['ruas']}, comp={r['comp_m']} m, "
              f"litros={r['litros_necessarios']:.3f} L")

def atualizar_registro():
    print("\n== Atualizar registro ==")
    if not registros:
        print("(vazio)")
        return
    try:
        idx = int(input("Índice do registro: "))
        _ = registros[idx]
    except (ValueError, IndexError):
        print("⚠️ Índice inválido.")
        return

    print("1) Recalcular área")
    print("2) Recalcular insumos")
    print("3) Alterar cultura")
    print("4) Alterar produto (texto)")
    print("0) Cancelar")
    op = input("Escolha: ").strip()
    if op == "1":
        area_ha = calc_area_hectares(registros[idx]["cultura"])
        registros[idx]["area_ha"] = round(area_ha, 6)
        print("✅ Área atualizada.")
    elif op == "2":
        ins = calc_insumos()
        registros[idx].update(ins)
        print("✅ Insumos atualizados.")
    elif op == "3":
        while True:
            cultura = input("Nova cultura [Soja/Milho]: ").strip().lower()
            if cultura in ("soja", "milho"):
                break
            print("⚠️ Opção inválida.")
        registros[idx]["cultura"] = cultura
        print("ℹ️ Se mudou formato, recalcule a área (opção 1).")
    elif op == "4":
        registros[idx]["produto"] = input("Novo produto: ").strip()
        print("✅ Produto atualizado.")
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
        idx = int(input("Índice do registro: "))
        _ = registros[idx]
    except (ValueError, IndexError):
        print("⚠️ Índice inválido.")
        return
    confirm = input(f"Confirma deletar o registro {idx}? [s/N]: ").strip().lower()
    if confirm == "s":
        registros.pop(idx)
        print("🗑️ Registro removido.")
    else:
        print("Cancelado.")

def exportar_csv(caminho: str = None):
    if not registros:
        print("⚠️  Nada para exportar.")
        return
    if caminho is None:
        caminho = DATA_DIR / "plantio.csv"
    else:
        caminho = (BASE_DIR / caminho).resolve()

    campos = ["cultura","area_ha","produto","dose_ml_m","ruas","comp_m","litros_necessarios"]
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
        if op == "1":
            inserir_registro()
        elif op == "2":
            listar_registros()
        elif op == "3":
            atualizar_registro()
        elif op == "4":
            deletar_registro()
        elif op == "5":
            exportar_csv()
        elif op == "0":
            print("Até mais!")
            break
        else:
            print("⚠️ Opção inválida.")

if __name__ == "__main__":
    menu()
