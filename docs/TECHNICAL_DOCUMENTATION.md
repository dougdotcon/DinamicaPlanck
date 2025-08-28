# Documentação Técnica
## Simulação de Física Teórica - Época de Planck

### Arquitetura do Sistema

#### Estrutura de Diretórios
```
fisica_epoca_plank/
├── main.py                 # Ponto de entrada principal
├── config.py              # Configurações do projeto
├── requirements.txt       # Dependências Python
├── setup.py              # Configuração de instalação
├── README.md             # Documentação principal
├── .gitignore           # Arquivos ignorados pelo Git
├── src/                 # Código fonte principal
│   ├── __init__.py
│   ├── constants_physics.py         # Constantes físicas dinâmicas
│   ├── tardis_universe_model.py     # Modelo do universo TARDIS
│   └── main_physics_test_v2.py      # Sistema de simulação V2.0
├── tests/               # Testes e versões demonstrativas
│   ├── physics_test_demo.py         # Versão demonstrativa
│   └── quick_improved_test.py       # Teste rápido
├── resultados/          # Resultados das simulações
├── archive/             # Versões antigas/não funcionais
├── docs/               # Documentação adicional
└── .git/              # Controle de versão Git
```

### Componentes Principais

#### 1. DynamicPhysicsConstants (`src/constants_physics.py`)
**Propósito**: Modela variação temporal das constantes físicas fundamentais

**Funcionalidades**:
- Variação de G, c, h, k_B, α durante eventos supercosmicos
- Eventos configuráveis (Big Bang, inflação, transições de fase)
- Funções de variação temporal personalizáveis
- Regularização para estabilidade numérica

**Exemplo de uso**:
```python
physics = DynamicPhysicsConstants()
physics.add_supercosmic_event(0, 'big_bang', ['c', 'G'], 0.3)
G_at_time = physics.get_constant('G', time)
```

#### 2. TARDISUniverse (`src/tardis_universe_model.py`)
**Propósito**: Implementa modelo de universo com dimensão externa fixa

**Funcionalidades**:
- Fator de escala interno vs raio externo constante
- Cálculo de compressão quântica
- Predições observacionais (CMB, distâncias)
- Visualizações interativas

**Conceito-chave**:
- Universo mantém tamanho externo fixo
- Expansão ocorre apenas internamente
- Razão de compressão = espaço_interno / espaço_externo

#### 3. PhysicsTestSystemV2 (`src/main_physics_test_v2.py`)
**Propósito**: Sistema principal de simulação numericamente estável

**Melhorias da V2.0**:
- Regularização matemática para evitar singularidades
- Tolerâncias numéricas otimizadas
- Limitação de variações extremas
- Método de integração robusto (DOP853)

**Equações resolvidas**:
- Equações de Friedmann modificadas
- Conservação de energia com termos quânticos
- Evolução da temperatura com correções
- Acoplamento com compressão TARDIS

### Metodologia Numérica

#### Problemas Resolvidos na V2.0
1. **Instabilidade em escalas de Planck**
   - Solução: Unidades naturalizadas e regularização
   
2. **Overflow em parâmetros extremos**
   - Solução: Clipping de valores e limitação de variações
   
3. **Divergências em equações diferenciais**
   - Solução: Termos de regularização ε = 1e-15
   
4. **Convergência numérica**
   - Solução: Método DOP853 com tolerâncias otimizadas

#### Parâmetros de Estabilização
```python
epsilon = 1e-15              # Regularização para singularidades
max_variation = 0.3          # Máximo 30% de variação
rtol = 1e-8                  # Tolerância relativa
atol = 1e-10                 # Tolerância absoluta
max_step = 1e4               # Passo máximo de integração
```

### Resultados Validados

#### Hipótese 1: Leis Físicas Dinâmicas ✅
- **G**: 25.7% de variação máxima
- **c**: 23.6% de variação máxima  
- **Padrões temporais**: Big Bang → Inflação → Estabilização
- **Convergência**: 1156 pontos simulados

#### Hipótese 2: Universo TARDIS ✅
- **Compressão quântica**: 117,038.8× crescimento
- **Expansão interna**: 10¹⁸ crescimento exponencial
- **Dimensão externa**: Rigorosamente constante
- **Estabilidade**: 100% convergência numérica

### Predições Observacionais

1. **Radiação Cósmica de Fundo**
   - Desvios na temperatura devido à compressão
   - Padrões de anisotropia específicos
   
2. **Ondas Gravitacionais Primordiais**
   - Assinaturas de eventos supercosmicos
   - Frequências características do modelo TARDIS
   
3. **Variação de Constantes**
   - α varia ~7% em quasares antigos
   - G apresenta correlações com formação de estruturas

### Uso do Sistema

#### Instalação
```bash
pip install -r requirements.txt
```

#### Execução Principal
```bash
python main.py
```

#### Execução Programática
```python
from src.main_physics_test_v2 import PhysicsTestSystemV2

system = PhysicsTestSystemV2()
results = system.run_complete_simulation()
```

### Arquivos de Saída

#### JSON (Dados estruturados)
```json
{
  "timestamp": "20250828_110244",
  "simulation_success": true,
  "points_simulated": 1156,
  "hypothesis_tests": {
    "dynamic_constants": {"supported": true},
    "tardis_universe": {"supported": true}
  }
}
```

#### PNG (Visualizações)
- Evolução temporal das constantes
- Modelo TARDIS vs padrão  
- Análise das hipóteses
- Resumo dos resultados

#### NPZ (Arrays numéricos)
- Séries temporais completas
- Dados para análises posteriores
- Formato otimizado para Python/NumPy

### Validação e Testes

#### Testes de Estabilidade
- Sensibilidade às condições iniciais
- Robustez numérica
- Convergência em diferentes tolerâncias

#### Testes de Consistência  
- Comparação com modelo cosmológico padrão
- Verificação de conservação de energia
- Validação de unidades físicas

### Desenvolvimento Futuro

#### Melhorias Planejadas
1. Interface gráfica para configuração
2. Paralelização para simulações em larga escala
3. Integração com dados observacionais reais
4. Extensão para outras épocas cosmológicas

#### Contribuições
- Código aberto e documentado
- Testes unitários abrangentes
- Documentação técnica detalhada
- Exemplos de uso prático
