# Regras de Substituição por Categoria

Quando um item não está disponível, use estas regras específicas por categoria para encontrar o melhor substituto.

## Busca Progressiva (Antes de Substituir)

Antes de declarar um item "indisponível" e acionar substituição, execute busca em 3 etapas:

```
Etapa 1 — Nome completo:
  "Feijão Preto Super Máximo 2Kg" → 0 resultados?

Etapa 2 — Marca + categoria (sem tamanho):
  "Feijão Preto Super Máximo" → 0 resultados?

Etapa 3 — Só categoria:
  "Feijão Preto" → resultados encontrados ✓
```

**Dica:** Remova acentos se necessário ("Feijao" = "Feijão" no iFood). Só acione a substituição se a Etapa 3 não retornar o item desejado ou equivalente.

## Mismatch de Tamanho (Item Existe mas Tamanho Diferente)

Quando o tamanho pedido não existe mas o item existe em outro tamanho:

```
Usuário quer: Feijão Preto 2Kg
Disponível: Feijão Preto 1Kg (R$ 7,37)

Calcule:
  - 2x 1Kg = R$ 14,74 (equivalente a 2Kg)
  - 5Kg disponível? Compare R$/kg: R$ 7,37/kg vs. R$ XX,XX/kg
```

**Regra:** Sempre informe e normalize preço/kg ou preço/L antes de sugerir. Mostre a diferença de custo. Não substitua silenciosamente.

Exemplo de apresentação:
```
Item pedido: Feijão Preto Super Máximo 2Kg — não encontrado
Alternativa A: 2x Feijão Preto Combrasil 1Kg = R$ 14,74 (R$ 7,37/kg)
Alternativa B: Feijão Preto Camil 5Kg = R$ 32,00 (R$ 6,40/kg, -13% por kg, vale a pena?)
```

## Princípio Geral

A hierarquia de substituição é:
1. Mesma marca + mesma categoria (tamanho diferente é OK — calcule equivalência)
2. Mesma especificação nutricional + marca similar
3. Mesmo tamanho/unidade + preço similar
4. Alternativa mais barata compatível

Sempre ofereça 2-3 opções com trade-offs e registre a decisão no USER_STATE.

## Categorias

### Arroz e Grãos
- Priorize o mesmo tipo (Tipo 1, parboilizado, integral)
- Marcas intercambiáveis: Tio João ↔ Camil ↔ Combrasil
- Se não tem 2Kg, use 2x 1Kg (calcule se compensa vs 5Kg)
- Arroz integral NÃO substitui branco sem perguntar

### Feijão
- Priorize o mesmo tipo (preto, carioca, fradinho)
- Marcas intercambiáveis: Super Máximo ↔ Combrasil ↔ Camil ↔ Kicaldo
- Feijão carioca NÃO substitui preto sem perguntar
- Feijão pronto/temperado NÃO é substituto de feijão cru

### Óleos e Azeites
- Óleo de girassol ↔ óleo de soja (perguntar, sabor diferente)
- Azeite extra virgem: marcas intercambiáveis por faixa de preço
- NUNCA substitua azeite por óleo ou vice-versa
- Considere tamanho: 500ml vs 900ml (normalizar preço/L)

### Laticínios — Leite
- Integral ↔ semidesnatado: perguntar (composição nutricional diferente)
- Zero lactose: APENAS substitua por outro zero lactose
- Marcas intercambiáveis: Elegê ↔ Itambé ↔ Parmalat
- UHT (caixinha) ≠ fresco (geladeira) — não misturar

### Laticínios — Iogurte
- Zero lactose: APENAS por outro zero lactose
- Desnatado ↔ integral: perguntar
- Batavo Pense ↔ Nestlé Molico (ambos light/zero lactose)
- Iogurte grego NÃO substitui iogurte natural sem perguntar

### Laticínios — Manteiga/Cream Cheese
- Com sal ↔ sem sal: perguntar (uso culinário diferente)
- Manteiga: Itambé ↔ Aviação ↔ Presidente
- Cream cheese zero lactose: apenas por outro zero lactose
- Margarina NÃO substitui manteiga sem perguntar

### Carnes
- Mesmo corte é prioridade (alcatra por alcatra, patinho por patinho)
- Congelado ↔ resfriado: perguntar (preço e textura diferentes)
- Frango: peito ↔ filé de peito (mesmo corte, apresentação diferente)
- Sadia ↔ Seara ↔ Perdigão (marcas intercambiáveis)
- Carne bovina: peso pode variar (bandeja) — avise sobre diferença de peso

### Peixes
- Tilápia: congelada ↔ fresca (perguntar)
- Filé ↔ posta: apresentações diferentes, perguntar
- NUNCA substitua tipo de peixe sem perguntar (sabor muito diferente)

### Limpeza
- Detergente: Ypê ↔ Limpol ↔ Minuano (intercambiáveis)
- Desinfetante: Vim ↔ Pato ↔ Veja (mesmo princípio ativo = OK)
- Tira-limo: Veja X14 ↔ qualquer "tira-limo" (função específica)
- Amaciante e desengordurante: manter a categoria, marca flexível

### Papel e Higiene
- Papel higiênico: respeitar folha simples/dupla/tripla (qualidade percebida)
- Neve ↔ Personal ↔ Dualette (folha tripla intercambiável)
- Papel toalha: Scala ↔ Snob ↔ Kitchen (intercambiáveis)
- Guardanapo: folha simples ↔ dupla (perguntar)

### Padaria e Biscoitos
- Pão francês congelado: marcas intercambiáveis
- Bisnaguinha: Plusvita ↔ Pullman ↔ Wickbold
- Biscoito Maizena: Piraquê ↔ Mabel ↔ Vitarella

## Formato de Registro

Quando registrar uma substituição no USER_STATE:

```json
{
  "date": "2026-02-18",
  "original": {"name": "Feijão Preto Super Máximo", "brand": "Super Máximo", "size": "1Kg"},
  "chosen": {"name": "Feijão Preto Combrasil", "brand": "Combrasil", "size": "1Kg", "price_brl": 7.37},
  "accepted": true,
  "reason": "indisponível na loja"
}
```

## Aprendizado

Após 3+ substituições do mesmo item:
- Se o usuário aceitou a mesma marca substituta 3+ vezes → promova para `brands_loved`
- Se o usuário rejeitou a mesma marca 2+ vezes → pare de sugerir essa marca
- Se o item original nunca está disponível → sugira proativamente que o usuário mude a preferência
