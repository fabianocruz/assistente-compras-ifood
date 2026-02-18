#!/usr/bin/env python3
"""
Atualiza o USER_STATE de forma segura, preservando histórico existente.

Uso:
  # Adicionar compra ao histórico
  python3 update_user_state.py add-purchase --state user_state.json --purchase purchase.json

  # Registrar substituição
  python3 update_user_state.py add-substitution --state user_state.json --sub substitution.json

  # Atualizar preferências
  python3 update_user_state.py update-prefs --state user_state.json --key brands_loved --add "Camil"

  # Calcular recorrências (analisa histórico e sugere cadências)
  python3 update_user_state.py calc-recurrence --state user_state.json

  # Mostrar resumo do estado atual
  python3 update_user_state.py summary --state user_state.json
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from collections import defaultdict


def load_state(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_state(path: str, state: dict):
    state['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    print(f"Estado salvo em {path}")


def add_purchase(state: dict, purchase: dict) -> dict:
    """Adiciona uma compra ao histórico."""
    if 'purchases' not in state.get('history', {}):
        state.setdefault('history', {})['purchases'] = []
    state['history']['purchases'].append(purchase)
    print(f"Compra de {purchase.get('date', 'N/A')} adicionada. "
          f"Total: R$ {purchase.get('total_brl', 0):.2f}, "
          f"{len(purchase.get('items', []))} itens.")
    return state


def add_substitution(state: dict, sub: dict) -> dict:
    """Registra uma substituição."""
    if 'substitutions' not in state.get('history', {}):
        state.setdefault('history', {})['substitutions'] = []
    state['history']['substitutions'].append(sub)
    status = "aceita" if sub.get('accepted') else "rejeitada"
    print(f"Substituição {status}: {sub['original']['name']} → {sub['chosen']['name']}")
    return state


def update_preferences(state: dict, key: str, value: str, action: str = 'add') -> dict:
    """Adiciona ou remove item de uma lista de preferências."""
    prefs = state.setdefault('profile', {}).setdefault('preferences', {})
    if key not in prefs:
        prefs[key] = []

    if action == 'add' and value not in prefs[key]:
        prefs[key].append(value)
        print(f"Adicionado '{value}' em {key}")
    elif action == 'remove' and value in prefs[key]:
        prefs[key].remove(value)
        print(f"Removido '{value}' de {key}")
    return state


def calculate_recurrence(state: dict) -> dict:
    """Analisa histórico de compras e calcula padrões de recorrência."""
    purchases = state.get('history', {}).get('purchases', [])

    if len(purchases) < 2:
        print("Precisa de pelo menos 2 compras para calcular recorrência.")
        return state

    # Agrupa compras por item normalizado
    item_dates = defaultdict(list)
    item_info = {}

    for purchase in purchases:
        date = datetime.strptime(purchase['date'], '%Y-%m-%d')
        for item in purchase.get('items', []):
            # Normaliza nome para key
            key = item['name'].lower().replace(' ', '_')[:30]
            item_dates[key].append(date)
            item_info[key] = {
                'display_name': item['name'],
                'preferred_brand': item.get('brand', ''),
                'avg_qty': item.get('qty', 1)
            }

    # Calcula cadência para itens com 2+ compras
    recurrence = []
    for key, dates in item_dates.items():
        if len(dates) >= 2:
            dates.sort()
            intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
            avg_interval = sum(intervals) / len(intervals)

            recurrence.append({
                'item_key': key,
                'display_name': item_info[key]['display_name'],
                'preferred_brand': item_info[key]['preferred_brand'],
                'cadence_days': round(avg_interval),
                'last_bought': dates[-1].strftime('%Y-%m-%d'),
                'avg_qty': item_info[key]['avg_qty']
            })

    state['history']['recurrence'] = recurrence
    print(f"Calculada recorrência para {len(recurrence)} itens.")
    return state


def show_summary(state: dict):
    """Mostra resumo do estado atual."""
    profile = state.get('profile', {})
    history = state.get('history', {})

    print(f"\n{'='*50}")
    print(f"RESUMO DO ESTADO — {profile.get('nome', 'N/A')}")
    print(f"{'='*50}")
    print(f"Endereço: {profile.get('location', {}).get('endereco', 'N/A')}")
    print(f"Prioridade: {profile.get('preferences', {}).get('priority', 'N/A')}")
    print(f"Marcas preferidas: {', '.join(profile.get('preferences', {}).get('brands_loved', []))}")
    print(f"\nHistórico:")
    purchases = history.get('purchases', [])
    print(f"  Compras: {len(purchases)}")
    if purchases:
        total = sum(p.get('total_brl', 0) for p in purchases)
        print(f"  Total gasto: R$ {total:.2f}")
        print(f"  Última compra: {purchases[-1].get('date', 'N/A')}")
    print(f"  Substituições: {len(history.get('substitutions', []))}")
    print(f"  Itens recorrentes: {len(history.get('recurrence', []))}")
    print(f"\nAlertas de preço: {len(state.get('price_alerts', []))}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Atualiza USER_STATE')
    parser.add_argument('action', choices=['add-purchase', 'add-substitution', 'update-prefs', 'calc-recurrence', 'summary'])
    parser.add_argument('--state', required=True, help='Caminho do user_state.json')
    parser.add_argument('--purchase', help='JSON file com dados da compra')
    parser.add_argument('--sub', help='JSON file com dados da substituição')
    parser.add_argument('--key', help='Chave da preferência')
    parser.add_argument('--add', help='Valor para adicionar')
    parser.add_argument('--remove', help='Valor para remover')

    args = parser.parse_args()
    state = load_state(args.state)

    if args.action == 'add-purchase':
        with open(args.purchase, 'r') as f:
            purchase = json.load(f)
        state = add_purchase(state, purchase)
        save_state(args.state, state)

    elif args.action == 'add-substitution':
        with open(args.sub, 'r') as f:
            sub = json.load(f)
        state = add_substitution(state, sub)
        save_state(args.state, state)

    elif args.action == 'update-prefs':
        if args.add:
            state = update_preferences(state, args.key, args.add, 'add')
        elif args.remove:
            state = update_preferences(state, args.key, args.remove, 'remove')
        save_state(args.state, state)

    elif args.action == 'calc-recurrence':
        state = calculate_recurrence(state)
        save_state(args.state, state)

    elif args.action == 'summary':
        show_summary(state)
