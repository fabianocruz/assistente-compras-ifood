# 🛒 Assistente de Compras – iFood Mercado

> **Claude Cowork Skill** — Automação inteligente de compras de supermercado via iFood Mercado e Prezunic, com memória de preferências, substituições automáticas e comparação de preços entre lojas.

---

## O que é

Um skill para o [Claude Cowork](https://claude.ai) que transforma o processo de fazer mercado online em algo rápido e inteligente. Em vez de navegar manualmente pelo iFood, você descreve o que precisa e o assistente monta o carrinho, compara preços, sugere substituições e aprende com suas preferências ao longo do tempo.

**Capacidades principais:**

- **Carrinho recorrente** — repete compras anteriores respeitando marcas e quantidades preferidas
- **Substituições inteligentes** — quando um item não está disponível, sugere alternativas com trade-offs claros (preço, marca, tamanho)
- **Busca progressiva** — tenta variações do termo antes de declarar um item indisponível
- **Seleção híbrida de mercado** — compara lojas na primeira compra, lembra a preferência, recompara periodicamente
- **Controle de orçamento** — acompanha o subtotal + taxa de entrega em relação à meta semanal
- **Monitoramento de pedido mínimo** — avisa quando o carrinho está abaixo do mínimo da loja
- **Listas por contexto** — café da manhã, marmitas, churrasco, limpeza, bebê, pet
- **Planejamento semanal** — cardápio de 7 dias convertido em lista de compras

**Nunca finaliza o pagamento** — o assistente monta o carrinho e confirma com você, mas o checkout é sempre feito por você.

---

## Requisitos

- [Claude Cowork](https://claude.ai) com modo browser (Claude in Chrome) ativado
- Conta no [iFood](https://ifood.com.br) (ou [Prezunic](https://prezunic.com.br))
- Python 3.8+ (para os scripts auxiliares)

---

## Instalação

### Opção A — npx (recomendada)

```bash
npx skills add fabianocruz/assistente-compras-ifood --skill assistente-compras-ifood
```

Para instalar globalmente:

```bash
npx skills add fabianocruz/assistente-compras-ifood --skill assistente-compras-ifood -g
```

### Opção B — Manual

```bash
git clone https://github.com/fabianocruz/assistente-compras-ifood.git
cp -r assistente-compras-ifood/skills/assistente-compras-ifood ~/.claude/skills/
```

### Opção C — Arquivo `.skill`

1. Baixe [`assistente-compras-ifood.skill`](./assistente-compras-ifood.skill) da seção [Releases](../../releases)
2. No Cowork, abra as configurações de Skills e importe o arquivo

---

## Primeiro Uso (Onboarding)

Na primeira sessão, o assistente vai pedir até **6 informações** para criar seu perfil:

1. **Endereço de entrega** — rua, número, bairro, cidade, CEP
2. **Moradores** — quantas pessoas, tem bebê ou pet?
3. **Prioridade** — economia, equilíbrio ou qualidade?
4. **Restrições alimentares** — alergias, dieta especial?
5. **Marcas preferidas** — tem marcas que sempre compra ou evita?
6. **Orçamento semanal** — quer definir uma meta? (opcional)

Esses dados são salvos em `user_state.json` **no seu workspace**, nunca na skill em si. Você controla e pode editar o arquivo a qualquer momento.

---

## Uso

Com o skill instalado, basta conversar naturalmente no Cowork:

```
"Quero fazer mercado"
"Repete a última compra"
"Monta um carrinho para churrasco de 10 pessoas"
"Planeja as refeições da semana"
"Qual mercado tem o melhor preço pra minha lista?"
"Me avisa quando o café cair abaixo de R$ 18"
```

---

## Estrutura do Projeto

```
assistente-compras-ifood/
├── assistente-compras-ifood.skill      # Skill empacotada (instalável)
├── README.md
├── LICENSE
└── skills/
    └── assistente-compras-ifood/       # Código-fonte da skill
        ├── SKILL.md                    # Documento principal (instruções para o Claude)
        ├── references/
        │   ├── user_state_schema.md    # Schema completo do JSON de memória
        │   ├── substitution_rules.md   # Regras de substituição por categoria
        │   ├── browser_patterns.md     # Padrões de automação (iFood e Prezunic)
        │   └── user_state.json         # Template vazio para novos usuários
        ├── scripts/
        │   ├── init_user_state.py      # Cria user_state.json para novo usuário
        │   ├── update_user_state.py    # Atualiza histórico de forma segura
        │   └── normalize_price.py      # Normalização de preços (R$/kg, R$/L)
        └── evals/
            └── evals.json              # Casos de teste para validação
```

---

## Dados Pessoais e Privacidade

O skill **não armazena dados pessoais** internamente. Todo o histórico, preferências e endereço ficam no arquivo `user_state.json` no seu workspace local — que só você acessa. Para compartilhar ou fazer backup, basta copiar esse arquivo.

O `user_state.json` incluído neste repositório é um **template vazio**, sem dados de nenhum usuário.

---

## Contribuindo

Pull requests são bem-vindos! Algumas ideias de contribuição:

- Suporte a novas plataformas (Carrefour, Extra, Rappi Mercado)
- Novas categorias de substituição em `substitution_rules.md`
- Novos casos de teste em `evals/evals.json`
- Tradução do skill para outros idiomas

---

## Licença

MIT — veja [LICENSE](./LICENSE) para detalhes.
