#!/usr/bin/env python3
"""
Inicializa um user_state.json vazio no workspace do usuário.
Copia o template da skill e preenche com dados básicos se fornecidos.

Uso:
  # Criar estado vazio
  python3 init_user_state.py /caminho/do/workspace/user_state.json

  # Criar com dados básicos via argumentos
  python3 init_user_state.py /caminho/do/workspace/user_state.json \
    --nome "Maria Silva" \
    --email "maria@email.com" \
    --endereco "Rua das Flores, 100, Centro, São Paulo - SP 01000-000" \
    --city "São Paulo" \
    --neighborhood "Centro" \
    --people 3 \
    --priority balance

  # Criar com dados via JSON string
  python3 init_user_state.py /caminho/do/workspace/user_state.json \
    --profile '{"nome": "Maria", "location": {"city": "São Paulo"}}'
"""

import json
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path


def get_template() -> dict:
    """Retorna o template vazio do user_state."""
    return {
        "versao": "2.1",
        "ultima_atualizacao": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "profile": {
            "nome": "",
            "email": "",
            "location": {
                "endereco": "",
                "city": "",
                "neighborhood": "",
                "radius_km": 5
            },
            "household": {
                "people": 0,
                "pets": [],
                "baby": False
            },
            "preferences": {
                "priority": "balance",
                "brands_loved": [],
                "brands_avoid": [],
                "health_filters": [],
                "sustainability_filters": []
            },
            "restrictions": {
                "allergies": [],
                "diet": []
            },
            "budget": {
                "weekly_target_brl": None,
                "strict": False
            }
        },
        "stores": {
            "preferred_stores": [],
            "purchase_count_since_comparison": 0,
            "comparison_interval": 4,
            "store_comparisons": []
        },
        "history": {
            "purchases": [],
            "substitutions": [],
            "recurrence": []
        },
        "context_lists": {
            "cafe_da_manha": [],
            "marmitas": [],
            "churrasco": [],
            "limpeza": [],
            "bebe": [],
            "pet": []
        },
        "price_alerts": []
    }


def deep_update(base: dict, updates: dict) -> dict:
    """Atualiza dict recursivamente sem sobrescrever sub-dicts inteiros."""
    for key, value in updates.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_update(base[key], value)
        else:
            base[key] = value
    return base


def main():
    parser = argparse.ArgumentParser(description='Inicializa user_state.json para novo usuário')
    parser.add_argument('output_path', help='Caminho onde criar o user_state.json')
    parser.add_argument('--nome', help='Nome do usuário')
    parser.add_argument('--email', help='Email do usuário')
    parser.add_argument('--endereco', help='Endereço completo de entrega')
    parser.add_argument('--city', help='Cidade')
    parser.add_argument('--neighborhood', help='Bairro')
    parser.add_argument('--people', type=int, help='Número de pessoas na casa')
    parser.add_argument('--priority', choices=['economy', 'balance', 'quality'], help='Prioridade de compras')
    parser.add_argument('--profile', help='JSON string com dados do perfil para merge')
    parser.add_argument('--force', action='store_true', help='Sobrescrever se já existir')

    args = parser.parse_args()

    # Verificar se já existe
    if os.path.exists(args.output_path) and not args.force:
        print(f"Arquivo já existe: {args.output_path}")
        print("Use --force para sobrescrever.")
        sys.exit(1)

    # Criar template
    state = get_template()

    # Preencher com argumentos CLI
    if args.nome:
        state['profile']['nome'] = args.nome
    if args.email:
        state['profile']['email'] = args.email
    if args.endereco:
        state['profile']['location']['endereco'] = args.endereco
    if args.city:
        state['profile']['location']['city'] = args.city
    if args.neighborhood:
        state['profile']['location']['neighborhood'] = args.neighborhood
    if args.people:
        state['profile']['household']['people'] = args.people
    if args.priority:
        state['profile']['preferences']['priority'] = args.priority

    # Merge com JSON do argumento --profile
    if args.profile:
        try:
            profile_data = json.loads(args.profile)
            deep_update(state['profile'], profile_data)
        except json.JSONDecodeError as e:
            print(f"Erro no JSON do --profile: {e}")
            sys.exit(1)

    # Criar diretório se necessário
    os.makedirs(os.path.dirname(os.path.abspath(args.output_path)), exist_ok=True)

    # Salvar
    with open(args.output_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f"user_state.json criado em: {args.output_path}")
    if state['profile']['nome']:
        print(f"  Usuário: {state['profile']['nome']}")
    if state['profile']['location']['city']:
        print(f"  Cidade: {state['profile']['location']['city']}")
    print(f"  Prioridade: {state['profile']['preferences']['priority']}")
    print("\nPróximo passo: preencha o perfil completo via conversa ou scripts/update_user_state.py")


if __name__ == '__main__':
    main()
