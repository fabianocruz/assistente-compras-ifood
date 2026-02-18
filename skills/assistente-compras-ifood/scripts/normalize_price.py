#!/usr/bin/env python3
"""
Normaliza preços para comparação justa entre produtos de tamanhos diferentes.
Calcula preço por kg, litro ou unidade.

Uso:
  python3 normalize_price.py "Arroz 1Kg" 8.01
  python3 normalize_price.py "Leite 1L" 4.89
  python3 normalize_price.py "Detergente 500ml" 2.89
  python3 normalize_price.py --compare "Arroz 1Kg:8.01" "Arroz 5Kg:38.51"
"""

import re
import sys
import json


def parse_size(text: str) -> tuple[float, str]:
    """Extrai quantidade e unidade de um texto de tamanho.

    Retorna (quantidade_em_unidade_base, unidade_base).
    Unidades base: 'kg', 'l', 'un'
    """
    text = text.lower().strip()

    # Padrões: 1Kg, 500g, 900ml, 1L, 200g, 1 litro, 2 unidades
    patterns = [
        (r'(\d+(?:[.,]\d+)?)\s*kg', 'kg', 1.0),
        (r'(\d+(?:[.,]\d+)?)\s*g(?:r(?:amas?)?)?', 'kg', 0.001),
        (r'(\d+(?:[.,]\d+)?)\s*l(?:itro)?s?(?!\w)', 'l', 1.0),
        (r'(\d+(?:[.,]\d+)?)\s*ml', 'l', 0.001),
        (r'(\d+(?:[.,]\d+)?)\s*(?:un(?:id(?:ades?)?)?|rolos?|pacotes?|bandejas?)', 'un', 1.0),
    ]

    for pattern, base_unit, multiplier in patterns:
        match = re.search(pattern, text)
        if match:
            value = float(match.group(1).replace(',', '.'))
            return value * multiplier, base_unit

    # Se não encontrou unidade, assume 1 unidade
    return 1.0, 'un'


def normalize_price(product_desc: str, price_brl: float) -> dict:
    """Calcula preço normalizado por unidade base."""
    quantity, unit = parse_size(product_desc)

    price_per_unit = price_brl / quantity if quantity > 0 else price_brl

    unit_labels = {
        'kg': 'R$/kg',
        'l': 'R$/L',
        'un': 'R$/un'
    }

    return {
        'product': product_desc,
        'price_brl': price_brl,
        'quantity': quantity,
        'unit': unit,
        'price_per_unit': round(price_per_unit, 2),
        'unit_label': unit_labels.get(unit, 'R$/un'),
        'display': f"R$ {price_per_unit:.2f}/{unit_labels.get(unit, 'un').split('/')[1]}"
    }


def compare_products(products: list[tuple[str, float]]) -> list[dict]:
    """Compara múltiplos produtos normalizando preço por unidade."""
    results = []
    for desc, price in products:
        results.append(normalize_price(desc, price))

    # Ordena por preço por unidade
    results.sort(key=lambda x: x['price_per_unit'])

    # Adiciona ranking e economia
    if results:
        cheapest = results[0]['price_per_unit']
        for i, r in enumerate(results):
            r['rank'] = i + 1
            r['vs_cheapest_pct'] = round((r['price_per_unit'] - cheapest) / cheapest * 100, 1)

    return results


if __name__ == '__main__':
    if '--compare' in sys.argv:
        # Modo comparação: --compare "Arroz 1Kg:8.01" "Arroz 5Kg:38.51"
        idx = sys.argv.index('--compare')
        products = []
        for arg in sys.argv[idx + 1:]:
            parts = arg.rsplit(':', 1)
            if len(parts) == 2:
                products.append((parts[0], float(parts[1])))

        results = compare_products(products)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif len(sys.argv) >= 3:
        # Modo simples: "Arroz 1Kg" 8.01
        desc = sys.argv[1]
        price = float(sys.argv[2])
        result = normalize_price(desc, price)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(__doc__)
