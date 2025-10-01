# Implementação de Autenticação por Token

## Objetivo
Adicionar autenticação por token nos testes dos ViewSets de Product e Order.

## Problemas Resolvidos

### 1. Erro 403 Forbidden nos Testes
- **Causa**: Testes não estavam autenticando o usuário
- **Solução**: Adicionado `self.client.force_authenticate(user=self.user)` no setUp


### 2. UserFactory Abstrata
- **Causa**: Factory estava configurada como abstrata
- **Solução**: Corrigida configuração da UserFactory em `order/factories.py`

### 3. MultipleObjectsReturned em test_create_order
- **Causa**: Múltiplos pedidos para o mesmo usuário
- **Solução**: Alterado de `.get()` para `.filter().order_by('-id').first()`
## Resultados
- ✅ 8/8 testes passando
- ✅ Autenticação funcionando corretamente
- ✅ Endpoints protegidos validados

## Arquivos Modificados
- `product/tests/test_viewsets/test_product_viewset.py`
- `order/test/test_viewsets/test_order_viewset.py`
- `order/factories.py`
