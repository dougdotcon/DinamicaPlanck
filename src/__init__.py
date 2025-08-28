"""
Módulo de Simulação de Física Teórica
Época de Planck com Leis Dinâmicas e Universo TARDIS

Este módulo contém as implementações principais para testar:
1. Hipótese de Leis Físicas Dinâmicas
2. Hipótese do Universo TARDIS

Versão: 2.0.0 (Numericamente Estável)
"""

__version__ = "2.0.0"
__author__ = "Sistema de Simulação de Física Teórica"

# Importações principais
from .constants_physics import DynamicPhysicsConstants
from .tardis_universe_model import TARDISUniverse
from .main_physics_test_v2 import PhysicsTestSystemV2

__all__ = [
    'DynamicPhysicsConstants',
    'TARDISUniverse', 
    'PhysicsTestSystemV2'
]
