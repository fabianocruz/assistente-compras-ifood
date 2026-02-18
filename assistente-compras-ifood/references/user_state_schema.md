# USER_STATE Schema

Estrutura completa do estado persistente do usuário. Este arquivo é a fonte de verdade sobre o formato do JSON de memória.

## Estrutura Principal

```json
{
  "versao": "2.2",
  "ultima_atualizacao": "YYYY-MM-DD HH:MM",

  "profile": {
    "nome": "string",
    "email": "string",
    "location": {
      "endereco": "string — endereço completo de entrega",
      "city": "string",
      "neighborhood": "string",
      "radius_km": "number — raio máximo para buscar lojas"
    },
    "household": {
      "people": "number — total de moradores",
      "pets": ["string — ex: 'gato', 'cachorro grande'"],
      "baby": "boolean"
    },
    "preferences": {
      "priority": "'economy' | 'balance' | 'quality'",
      "brands_loved": ["string — marcas preferidas, ex: 'Tio João', 'Elegê'"],
      "brands_avoid": ["string — marcas a evitar"],
      "health_filters": ["string — ex: 'sem_lactose', 'integral', 'sem_gluten'"],
      "sustainability_filters": ["string — ex: 'organico', 'menos_embalagem'"]
    },
    "restrictions": {
      "allergies": ["string — ex: 'amendoim', 'frutos_do_mar'"],
      "diet": ["string — ex: 'low_carb', 'vegetariano'"]
    },
    "budget": {
      "weekly_target_brl": "number | null — meta semanal em R$",
      "strict": "boolean — se true, nunca ultrapasse; se false, é sugestão"
    }
  },

  "history": {
    "purchases": [
      {
        "date": "YYYY-MM-DD",
        "store": "string — ex: 'Prezunic Barra Marapendi'",
        "platform": "'ifood' | 'prezunic' | 'outro'",
        "items": [
          {
            "name": "string — nome do produto como encontrado",
            "brand": "string",
            "size": "string — ex: '1Kg', '500ml', '200g'",
            "qty": "number",
            "price_unit_brl": "number — preço unitário",
            "price_total_brl": "number — preço x quantidade",
            "category": "string — ex: 'mercearia', 'laticinios', 'carnes'",
            "substitution_of": "string | null — nome do item original se foi substituição"
          }
        ],
        "total_brl": "number",
        "delivery_fee_brl": "number",
        "notes": "string | null"
      }
    ],

    "substitutions": [
      {
        "date": "YYYY-MM-DD",
        "original": {
          "name": "string",
          "brand": "string",
          "size": "string"
        },
        "chosen": {
          "name": "string",
          "brand": "string",
          "size": "string",
          "price_brl": "number"
        },
        "accepted": "boolean — se o usuário aceitou a substituição",
        "reason": "string — ex: 'indisponível', 'preço melhor', 'preferência'"
      }
    ],

    "recurrence": [
      {
        "item_key": "string — identificador normalizado, ex: 'leite_integral_1l'",
        "display_name": "string — nome legível, ex: 'Leite Integral 1L'",
        "preferred_brand": "string",
        "cadence_days": "number — frequência em dias (ex: 7 = semanal)",
        "last_bought": "YYYY-MM-DD",
        "avg_qty": "number — quantidade média por compra"
      }
    ]
  },

  "context_lists": {
    "cafe_da_manha": ["string — itens típicos"],
    "marmitas": ["string"],
    "churrasco": ["string"],
    "limpeza": ["string"],
    "bebe": ["string"],
    "pet": ["string"]
  },

  "stores": {
    "preferred_stores": [
      {
        "platform": "'ifood' | 'prezunic' | 'carrefour' | 'outro'",
        "store_name": "string — ex: 'Prezunic - Barra Marapendi'",
        "store_id": "string | null — ID interno da plataforma (slug da URL no iFood)",
        "rating": "number — avaliação (ex: 4.8)",
        "distance_km": "number",
        "delivery_time_min": "string — ex: '36-56'",
        "delivery_fee_brl": "number — 0 se grátis",
        "min_order_brl": "number — pedido mínimo",
        "chosen_on": "YYYY-MM-DD — data em que foi escolhido",
        "is_default": "boolean — se é o mercado padrão para compras rápidas"
      }
    ],
    "purchase_count_since_comparison": "number — contador de compras desde última comparação multi-loja",
    "comparison_interval": "number — a cada quantas compras sugerir recomparação (padrão: 4)",
    "store_comparisons": [
      {
        "date": "YYYY-MM-DD",
        "stores_compared": ["string — nomes dos mercados comparados"],
        "sample_items": [
          {
            "item_name": "string",
            "prices": {
              "nome_loja_1": "number",
              "nome_loja_2": "number"
            }
          }
        ],
        "totals": {
          "nome_loja_1": {"subtotal_brl": "number", "delivery_fee_brl": "number", "total_brl": "number"},
          "nome_loja_2": {"subtotal_brl": "number", "delivery_fee_brl": "number", "total_brl": "number"}
        },
        "winner": "string — nome da loja com melhor custo-benefício",
        "chosen_by_user": "string — qual loja o usuário escolheu (pode diferir do winner)",
        "reason": "string | null — motivo se o usuário não escolheu o winner"
      }
    ]
  },

  "price_alerts": [
    {
      "id": "string — UUID",
      "item": {
        "name": "string",
        "brand": "string | null",
        "size": "string | null"
      },
      "target_brl": "number — preço alvo",
      "radius_km": "number",
      "expires_on": "YYYY-MM-DD",
      "enabled": "boolean",
      "triggered": "boolean",
      "last_checked": "YYYY-MM-DD | null"
    }
  ]
}
```

## Regras de Atualização

1. **Nunca sobrescreva histórico** — sempre faça append em `purchases` e `substitutions`
2. **Recorrência é calculada** — após 3+ compras do mesmo item, calcule `cadence_days` como média de intervalo entre compras
3. **Preferências são inferidas** — se o usuário escolher a mesma marca 3+ vezes, adicione em `brands_loved`
4. **Substituições rejeitadas** — se o usuário rejeitar a mesma substituição 2+ vezes, evite sugerir novamente
5. **Orçamento** — atualize `weekly_target_brl` apenas quando o usuário solicitar explicitamente

## Exemplo (Usuário Fictício)

```json
{
  "profile": {
    "nome": "Maria Silva",
    "email": "maria@email.com",
    "location": {
      "endereco": "Rua das Flores, 200, Copacabana, Rio de Janeiro - RJ 22000-000",
      "city": "Rio de Janeiro",
      "neighborhood": "Copacabana",
      "radius_km": 5
    },
    "preferences": {
      "priority": "balance",
      "brands_loved": ["Camil", "Parmalat"],
      "brands_avoid": [],
      "health_filters": ["sem_gluten"],
      "sustainability_filters": ["organico"]
    }
  },
  "stores": {
    "preferred_stores": [
      {
        "platform": "ifood",
        "store_name": "Extra - Copacabana",
        "store_id": "extra-copacabana-abc123",
        "rating": 4.6,
        "distance_km": 1.2,
        "delivery_time_min": "30-50",
        "delivery_fee_brl": 0,
        "min_order_brl": 80,
        "chosen_on": "2026-02-10",
        "is_default": true
      }
    ],
    "purchase_count_since_comparison": 2,
    "comparison_interval": 4,
    "store_comparisons": []
  }
}
```
