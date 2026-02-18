# Padrões de Automação de Navegador

Referência técnica para automação de compras via Chrome MCP em diferentes plataformas.

## iFood Mercado (ifood.com.br/mercados)

### Fluxo Geral

1. Navegue para `ifood.com.br/mercados`
2. Confirme endereço de entrega no canto superior direito
3. Siga o fluxo de Seleção de Mercado (ver abaixo)
4. Dentro da loja escolhida, use "Busque nesta loja por item" para cada produto

### Descobrir Mercados Disponíveis

A página `ifood.com.br/mercados` lista supermercados organizados em seções:
- "Atacados perto de você" (Atacadão, Sam's Club, etc.)
- "Últimas Lojas" (visitadas recentemente)
- "Mais pedidos" (populares na região)

Para listar todos:
```
1. Navegue para ifood.com.br/mercados
2. Screenshot para capturar mercados visíveis
3. Scroll para baixo para ver mais seções
4. Screenshot novamente
5. Para cada mercado, capture: nome, avaliação, distância, tempo, taxa
```

Os dados aparecem no card de cada mercado:
- Nome: texto principal (ex: "Prezunic - Barra Marapendi")
- Avaliação: número com estrela (ex: "4.8")
- Tipo + distância: (ex: "Mercado · 3.1 km")
- Tempo e taxa: (ex: "36-56 min · R$ 19,99" ou "15-20 min · Grátis")

### Buscar Loja Específica

Se o usuário quer uma loja específica ou se quiser comparar:
```
1. Clique no campo de busca principal (topo da página)
2. Digite o nome do mercado (ex: "Prezunic")
3. A sugestão "Você procura por: Prezunic" aparece abaixo
4. Clique na sugestão
5. Resultados mostram aba "Lojas" com mercados e aba "Itens"
6. Clique na loja desejada para entrar
```

URL de busca: `ifood.com.br/busca?q=NomeMercado`

### Entrar na Loja

Após clicar na loja, a URL muda para:
```
ifood.com.br/delivery/{cidade}/{slug-da-loja}/{id-da-loja}
```

Guarde o slug e id para acessos futuros (salvar em `preferred_stores.store_id`).

Para acessar diretamente uma loja já conhecida:
```
Navegue para: ifood.com.br/delivery/{cidade}/{slug}/{id}
```

### Buscar Produto

```
1. Clique no campo de busca "Busque nesta loja por item"
2. Digite o termo de busca
3. Pressione Enter
4. Aguarde resultados (screenshot para confirmar)
```

Para busca seguinte (limpar campo):
```
1. Triple-click no campo de busca (seleciona todo o texto)
2. Digite novo termo (sobrescreve)
3. Pressione Enter
```

### Adicionar ao Carrinho

O iFood tem **dois fluxos** de adição, ambos válidos:

**Fluxo A — Direto pelo "+" no card (mais comum):**
```
1. Identifique o produto correto nos resultados
2. Clique no botão "+" no card do produto
3. Screenshot para confirmar (card muda para [-] 1 [+])
4. Carrinho no canto superior direito atualiza total
```

**Fluxo B — Via página de detalhe (ocorre quando o clique abre o produto):**
```
1. O clique no card abre a página do produto (URL muda para ?item=...)
2. Confirme o produto na página de detalhe (nome, preço, tamanho)
3. Clique no botão "Adicionar" (vermelho, grande, centralizado)
4. O card muda para [lixeira] 1 [+], confirmando adição
5. Use botão Voltar ou triple-click na busca para continuar
```

**Como saber qual fluxo ocorreu:** verifique a URL após o clique. Se contiver `?item=`, abriu detalhe (Fluxo B). Se não mudou, adicionou diretamente (Fluxo A).

**Nota sobre acentos:** o iFood não exige acentuação correta. "Feijao" funciona igual a "Feijão". Útil para buscas automatizadas.

### Aumentar Quantidade

Após o primeiro "+" o card mostra: [-] [1] [+]

```
1. Clique no "+" novamente (ao lado do número)
2. O número incrementa: 1 → 2 → 3...
3. Para qtd=N: clique "+" N-1 vezes após a primeira adição
```

### Verificar Carrinho

- Total e quantidade aparecem no canto superior direito (badge vermelho)
- Formato: "R$ XX,XX — N itens"
- Clique no ícone de sacola para ver detalhes

### Verificar Carrinho Pré-existente

Ao entrar na loja, o iFood preserva itens de sessões anteriores. Sempre confirme o estado do carrinho antes de começar:

```
1. Screenshot ao entrar na loja
2. Verifique o badge vermelho no canto superior direito
3. Se mostrar valor > R$ 0 ou itens > 0, há carrinho pré-existente
4. Informe o usuário: "Seu carrinho tem N itens de uma compra anterior (R$ XX,XX).
   Quer continuar de onde parou, limpar o carrinho ou ignorar e adicionar novos itens?"
5. Aguarde decisão antes de prosseguir
```

### Monitorar Pedido Mínimo

O pedido mínimo da loja aparece na lateral esquerda (ex: "Pedido mínimo R$ 60"). Durante a montagem do carrinho:

```
Calcule: valor_faltante = min_order - total_atual

Se valor_faltante > R$ 0:
  - Informe ao final de cada item: "Carrinho: R$ XX,XX | Faltam R$ YY,YY para pedido mínimo"

Se valor_faltante <= R$ 0:
  - Informe: "✓ Pedido mínimo atingido"

Se lista de compras completa e ainda abaixo do mínimo:
  - Alerte: "Lista concluída, mas o total (R$ XX) está abaixo do mínimo (R$ YY).
    Que tal adicionar [sugestão baseada no histórico]?"
```

### Problemas Comuns — iFood

- **Busca retorna 0 resultados**: tente termos mais genéricos (ver busca progressiva abaixo)
- **Produto sem imagem**: pode estar indisponível, verificar se tem "+"
- **Clique abre página de detalhe**: use Fluxo B acima (botão "Adicionar" na página)
- **Carrinho com itens antigos**: perguntar ao usuário antes de continuar
- **Loja fechada**: verificar horário de funcionamento na página da loja

## Prezunic (prezunic.com.br) — VTEX

### Fluxo Geral

1. Navegue para `prezunic.com.br`
2. Use a URL de busca ou o campo de busca

### Buscar Produto

URL direta (mais confiável):
```
https://www.prezunic.com.br/TERMO%20BUSCA?_q=TERMO%20BUSCA&map=ft
```

Exemplo:
```
https://www.prezunic.com.br/arroz%20tio%20joao?_q=arroz%20tio%20joao&map=ft
```

Via campo de busca:
```
1. Clique no campo de busca (topo da página)
2. Digite o termo
3. Pressione Enter ou clique na lupa
```

### Adicionar ao Carrinho

Na página de resultados:
```
1. Localize o produto
2. Clique em "COMPRAR" (botão azul no card)
3. Screenshot para confirmar
```

Na página de detalhe do produto:
```
1. Clique em "ADICIONAR AO CARRINHO" (botão grande)
2. Screenshot para confirmar
```

**CUIDADO**: Às vezes clicar em "COMPRAR" nos resultados navega para a página de detalhe em vez de adicionar diretamente. Nesse caso:
- Verifique se está na página de detalhe (URL muda)
- Clique em "Adicionar ao carrinho" na página de detalhe
- Só depois o "+" fica disponível

### Aumentar Quantidade

Após adicionar, o botão muda para [-] [1] [+]:

```
1. Use `find` para localizar o botão "+" (plus/increase)
2. Clique no "+" encontrado pelo ref
3. Repita N-1 vezes para quantidade N
```

### Verificar Carrinho

- Ícone de carrinho no header mostra quantidade de itens distintos
- Clique para ver detalhes e total

### Problemas Comuns — Prezunic

- **"COMPRAR" vai para detalhe**: clicar "Adicionar ao carrinho" na página de detalhe primeiro
- **"+" não encontrado**: pode precisar scroll, usar `find` com query específica
- **Preço zero ou indisponível**: item esgotado, aplicar substituição
- **Resultados misturados**: Prezunic mostra produtos patrocinados, verificar relevância

## Estratégia de Busca

### Termos Progressivos

Comece específico e generalize se necessário:

```
Tentativa 1: "Feijão Preto Super Máximo 1Kg"  → 0 resultados
Tentativa 2: "Feijão Preto Super Máximo"       → 0 resultados
Tentativa 3: "Feijão Preto"                    → 8 resultados ✓
```

### Dicas de Busca

- Remova tamanho/peso da busca (filtrar visualmente)
- Use nome da marca sem acentos se necessário
- Para marcas próprias (Prezunic), busque pela categoria
- Produtos de limpeza: use nome comercial (ex: "Veja X14" não "tira-limo")

## Registro de Preços

Após cada item adicionado, registre em memória de trabalho:

```
Item #: [número sequencial]
Produto: [nome completo como aparece no site]
Marca: [marca]
Tamanho: [peso/volume]
Preço unitário: R$ X,XX
Quantidade: N
Subtotal: R$ XX,XX
Nota: [substituição? promoção? diferença de tamanho?]
```

Ao final, compile o relatório completo com total estimado.
