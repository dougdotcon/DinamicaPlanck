#!/usr/bin/env python3
"""
TESTE DE HIPÓTESES DE FÍSICA TEÓRICA
Época de Planck com Leis Dinâmicas e Universo TARDIS

Arquivo principal para executar as simulações validadas.
Utilize este arquivo como ponto de entrada principal do projeto.

Autor: Sistema de Simulação de Física Teórica
Data: Agosto 2025
"""

import sys
import os

# Adicionar pasta src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Função principal - executa simulação V2.0 validada"""
    
    print("=" * 70)
    print("TESTE DE HIPÓTESES DE FÍSICA TEÓRICA")
    print("Época de Planck com Leis Dinâmicas e Universo TARDIS")
    print("=" * 70)
    print()
    print("🔬 Hipóteses testadas:")
    print("1. Leis físicas podem variar durante eventos supercosmicos")
    print("2. Universo TARDIS: maior por dentro que por fora")
    print()
    print("Executando simulação V2.0 numericamente estável...")
    print()
    
    try:
        # Importar e executar simulador V2.0
        from main_physics_test_v2 import PhysicsTestSystemV2
        
        system = PhysicsTestSystemV2()
        results = system.run_complete_simulation()
        
        if results.get('simulation_success', False):
            print("\n" + "=" * 70)
            print("✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print()
            print("📊 Verifique os resultados em:")
            print(f"   • resultados/physics_test_v2_results_{results['timestamp']}.json")
            print(f"   • resultados/physics_test_v2_visualization_{results['timestamp']}.png")
            print()
            print("📖 Para detalhes completos, consulte README.md")
            
        else:
            print("❌ Simulação falhou. Verifique os logs acima.")
            return 1
            
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("Certifique-se de que todos os arquivos estão na pasta 'src/'")
        return 1
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
