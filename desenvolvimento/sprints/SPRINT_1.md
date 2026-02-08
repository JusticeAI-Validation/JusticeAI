# 🎯 SPRINT 1: Métricas Core

**Período**: Semanas 3-4 (22 Fev - 8 Mar 2026)
**Objetivo**: Implementar 15+ métricas de fairness
**Capacity**: 80 horas (2 devs × 2 semanas × 20h/semana)

---

## 📋 Objetivos da Sprint

### Objetivo Principal
Implementar todas as métricas fundamentais de fairness (pre-training e post-training)

### Entregáveis
1. 4 métricas pre-training (independentes de modelo)
2. 11 métricas post-training (dependentes de predições)
3. Confusion matrix por grupo
4. Threshold analysis
5. FairnessCalculator facade
6. Coverage ≥ 95% nas métricas

---

## User Stories

### 🎯 US-007: Métricas Pre-Training

**Prioridade**: 🔴 CRITICAL | **Estimativa**: 12 horas | **Status**: ⏳ TODO

#### User Story
> Como **data scientist**,
> Eu quero **métricas independentes de modelo**,
> Para **avaliar viés no dataset antes do treinamento**

#### Critérios de Aceite
- [ ] Class Balance implementado
- [ ] Concept Balance implementado
- [ ] KL Divergence implementado
- [ ] JS Divergence implementado
- [ ] Testes unitários (coverage ≥ 95%)
- [ ] Docstrings completas
- [ ] Type hints em tudo

#### Implementação
```python
# justiceai/core/metrics/pretrain.py

def class_balance(y: pd.Series, sensitive_attr: pd.Series) -> Dict[str, float]:
    """
    Calculate class balance across sensitive attribute groups.

    Args:
        y: Target variable
        sensitive_attr: Sensitive attribute (e.g., gender, race)

    Returns:
        Dictionary with balance metrics per group
    """
    pass

def concept_balance(X: pd.DataFrame, y: pd.Series,
                   sensitive_attr: pd.Series) -> float:
    """Calculate concept balance using mutual information."""
    pass

def kl_divergence(dist1: np.ndarray, dist2: np.ndarray) -> float:
    """Calculate Kullback-Leibler divergence between distributions."""
    pass

def js_divergence(dist1: np.ndarray, dist2: np.ndarray) -> float:
    """Calculate Jensen-Shannon divergence between distributions."""
    pass
```

#### Testes
```python
# tests/core/metrics/test_pretrain.py

def test_class_balance_equal_distribution(sample_balanced_data):
    """Test class balance with perfectly balanced data."""
    result = class_balance(sample_balanced_data['y'],
                          sample_balanced_data['sensitive'])
    assert all(0.9 <= v <= 1.1 for v in result.values())

def test_class_balance_imbalanced(sample_imbalanced_data):
    """Test class balance detects imbalance."""
    result = class_balance(sample_imbalanced_data['y'],
                          sample_imbalanced_data['sensitive'])
    assert any(v < 0.5 or v > 1.5 for v in result.values())
```

**Referência**: DeepBridge `fairness/metrics.py:class_balance`

---

### 🎯 US-008: Métricas Post-Training Básicas

**Prioridade**: 🔴 CRITICAL | **Estimativa**: 14 horas | **Status**: ⏳ TODO

#### User Story
> Como **data scientist**,
> Eu quero **métricas dependentes de predições**,
> Para **avaliar viés do modelo treinado**

#### Critérios de Aceite
- [ ] Statistical Parity implementado
- [ ] Disparate Impact implementado
- [ ] Equal Opportunity implementado
- [ ] Equalized Odds implementado
- [ ] Testes com modelos reais (sklearn)
- [ ] Edge cases cobertos

#### Implementação
```python
# justiceai/core/metrics/posttrain.py

def statistical_parity(y_pred: np.ndarray,
                      sensitive_attr: pd.Series) -> float:
    """
    Calculate statistical parity difference.

    Statistical parity is satisfied when P(Y_pred=1|A=a) = P(Y_pred=1|A=b)
    for all groups a, b.

    Returns:
        Difference between max and min positive prediction rates
    """
    pass

def disparate_impact(y_pred: np.ndarray,
                    sensitive_attr: pd.Series) -> float:
    """
    Calculate disparate impact ratio.

    DI = min(P(Y=1|A=a)) / max(P(Y=1|A=a))

    Returns:
        Ratio between 0 and 1 (1 = perfect fairness)
    """
    pass

def equal_opportunity(y_true: np.ndarray, y_pred: np.ndarray,
                     sensitive_attr: pd.Series) -> float:
    """Calculate equal opportunity difference (TPR difference)."""
    pass

def equalized_odds(y_true: np.ndarray, y_pred: np.ndarray,
                  sensitive_attr: pd.Series) -> Dict[str, float]:
    """Calculate equalized odds (TPR and FPR differences)."""
    pass
```

**Referência**: DeepBridge `fairness/metrics.py:statistical_parity`

---

### 🎯 US-009: Métricas Post-Training Avançadas

**Prioridade**: 🔴 CRITICAL | **Estimativa**: 16 horas | **Status**: ⏳ TODO

#### Métricas Implementadas
1. False Negative Rate Difference
2. Conditional Acceptance (PPV)
3. Conditional Rejection (NPV)
4. Precision Difference
5. Accuracy Difference
6. Treatment Equality
7. Entropy Index

#### Validação
- [ ] Benchmark contra Fairlearn
- [ ] Documentar diferenças (se houver)
- [ ] Performance adequada (< 1s para 10k samples)

---

### 🎯 US-010: Confusion Matrix por Grupo

**Prioridade**: 🟡 SHOULD | **Estimativa**: 6 horas | **Status**: ⏳ TODO

#### Implementação
```python
def confusion_matrix_by_group(y_true: np.ndarray,
                             y_pred: np.ndarray,
                             sensitive_attr: pd.Series) -> Dict[str, Dict]:
    """
    Calculate confusion matrix stratified by sensitive attribute.

    Returns:
        {
            'group_A': {'TP': X, 'FP': Y, 'TN': Z, 'FN': W},
            'group_B': {...}
        }
    """
    pass
```

---

### 🎯 US-011: Threshold Analysis

**Prioridade**: 🟡 SHOULD | **Estimativa**: 10 horas | **Status**: ⏳ TODO

#### User Story
> Como **ML engineer**,
> Eu quero **análise de thresholds de decisão**,
> Para **otimizar fairness vs performance**

#### Implementação
```python
# justiceai/core/evaluators/threshold.py

class ThresholdAnalyzer:
    """Analyze fairness metrics across different decision thresholds."""

    def analyze(self, y_true, y_prob, sensitive_attr,
                thresholds=np.linspace(0.01, 0.99, 100)):
        """
        Test multiple thresholds and calculate metrics for each.

        Returns:
            DataFrame with threshold, fairness metrics, and performance metrics
        """
        pass

    def find_optimal_threshold(self, fairness_metric='disparate_impact',
                              performance_metric='f1_score',
                              fairness_weight=0.5):
        """Find optimal threshold balancing fairness and performance."""
        pass
```

**Referência**: DeepBridge `fairness_suite.py:run_threshold_analysis`

---

### 🎯 US-012: FairnessCalculator Facade

**Prioridade**: 🔴 CRITICAL | **Estimativa**: 8 horas | **Status**: ⏳ TODO

#### User Story
> Como **desenvolvedor**,
> Eu quero **uma classe unificada**,
> Para **calcular todas as métricas de uma vez**

#### Implementação
```python
# justiceai/core/metrics/calculator.py

class FairnessCalculator:
    """Unified interface for calculating all fairness metrics."""

    def __init__(self, cache_results: bool = True):
        self.cache = {} if cache_results else None

    def calculate_all(self,
                     y_true: np.ndarray,
                     y_pred: np.ndarray,
                     sensitive_attr: pd.Series,
                     X: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Calculate all fairness metrics.

        Returns:
            {
                'pretrain': {...},  # If X provided
                'posttrain': {...},
                'confusion_matrix': {...},
                'summary': {...}
            }
        """
        pass

    def calculate_pretrain_metrics(self, X, y, sensitive_attr):
        """Calculate pre-training metrics only."""
        pass

    def calculate_posttrain_metrics(self, y_true, y_pred, sensitive_attr):
        """Calculate post-training metrics only."""
        pass
```

---

## Definition of Done

### Sprint 1 está completa quando:
- [ ] 15+ métricas implementadas e testadas
- [ ] Coverage ≥ 95% em `justiceai/core/metrics/`
- [ ] Benchmark vs Fairlearn documentado
- [ ] Todas docstrings completas (Google style)
- [ ] Type hints 100%
- [ ] CI passando
- [ ] Demo preparada

---

## Tarefas Técnicas

### Semana 1 (22-28 Fev)
- [ ] Dia 1-2: US-007 (Métricas pre-training)
- [ ] Dia 3-4: US-008 (Métricas post-training básicas)
- [ ] Dia 5: Iniciar US-009

### Semana 2 (1-7 Mar)
- [ ] Dia 1-2: Finalizar US-009 (Métricas avançadas)
- [ ] Dia 3: US-010 (Confusion matrix)
- [ ] Dia 4: US-011 (Threshold analysis)
- [ ] Dia 5: US-012 (Calculator facade)

---

## Métricas de Sucesso

| Métrica | Target | Atual |
|---------|--------|-------|
| **Métricas Implementadas** | 15+ | 0 |
| **Code Coverage** | ≥ 95% | - |
| **Performance** | < 2s (10k samples) | - |
| **Type Coverage** | 100% | - |
| **Docstrings** | 100% | - |

---

## Riscos

| Risco | Mitigação |
|-------|-----------|
| **R1**: Cálculo incorreto de métricas | Benchmark vs Fairlearn/AIF360 |
| **R2**: Performance ruim | Profiling desde início, usar NumPy/Pandas vectorizado |
| **R3**: Complexidade alta | Começar simples, refatorar depois |

---

## Entregáveis

- ✅ 15+ métricas de fairness
- ✅ Confusion matrix por grupo
- ✅ Threshold analysis
- ✅ FairnessCalculator facade
- ✅ Coverage ≥ 95%
- ✅ Benchmarks documentados

---

**Status**: ⏳ TODO
**Última Atualização**: 2026-02-08
**Sprint Anterior**: Sprint 0 (Setup)
**Próxima Sprint**: Sprint 2 (Reports HTML)
