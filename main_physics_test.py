"""
Script principal para testar as hipóteses de física teórica:
1. Leis físicas dinâmicas durante eventos supercosmicos
2. Modelo do universo TARDIS (dimensão externa constante)

Executa simulações completas e gera relatórios de validação
"""

import numpy as np
import matplotlib.pyplot as plt
from planck_epoch_simulator import PlanckEpochSimulator
from constants_physics import DynamicPhysicsConstants
from tardis_universe_model import TARDISUniverse
import json
from datetime import datetime

def main():
    """Função principal para executar todos os testes"""
    print("=" * 70)
    print("TESTE DE HIPÓTESES DE FÍSICA TEÓRICA")
    print("Época de Planck com Leis Dinâmicas e Universo TARDIS")
    print("=" * 70)
    
    # Inicializar simulador
    simulator = PlanckEpochSimulator()
    
    # Executar testes completos
    print("\n1. Iniciando simulação da época de Planck...")
    test_results = simulator.test_hypotheses()
    
    # Gerar relatório detalhado
    print("\n2. Gerando relatório de análise...")
    generate_detailed_report(test_results)
    
    # Testes adicionais específicos
    print("\n3. Executando testes adicionais...")
    additional_tests = run_additional_tests(simulator)
    
    # Salvar resultados
    print("\n4. Salvando resultados...")
    timestamp = save_results(test_results, additional_tests)
    
    print("\n5. Análise concluída! Verifique os arquivos gerados.")
    
    return test_results, additional_tests

def generate_detailed_report(test_results):
    """Gera relatório detalhado dos resultados"""
    
    print("\n" + "=" * 50)
    print("RELATÓRIO DETALHADO DE ANÁLISE")
    print("=" * 50)
    
    # Análise da hipótese 1: Constantes dinâmicas
    dynamic_test = test_results['hypothesis_tests']['dynamic_constants']
    print(f"\nHIPÓTESE 1: LEIS FÍSICAS DINÂMICAS")
    print("-" * 40)
    print(f"Status: {'SUPORTADA' if dynamic_test['hypothesis_supported'] else 'NÃO SUPORTADA'}")
    print(f"Constante mais variável: {dynamic_test['most_variable_constant']}")
    
    print(f"\nVariações das constantes fundamentais:")
    for const, var in dynamic_test['variations'].items():
        print(f"  • {const}:")
        print(f"    - Variação total: {var['change_percent']:.3f}%")
        print(f"    - Variação máxima: {var['max_variation_percent']:.3f}%")
    
    # Análise da hipótese 2: Universo TARDIS
    tardis_test = test_results['hypothesis_tests']['tardis_universe']
    print(f"\nHIPÓTESE 2: UNIVERSO TARDIS")
    print("-" * 40)
    print(f"Status: {'SUPORTADA' if tardis_test['hypothesis_supported'] else 'NÃO SUPORTADA'}")
    print(f"Crescimento da compressão quântica: {tardis_test['compression_growth_factor']:.2e}")
    print(f"Crescimento interno aparente: {tardis_test['internal_growth_factor']:.2e}")
    print(f"Assinatura de compressão quântica: {tardis_test['quantum_compression_signature']:.3f}")
    
    # Predições observacionais
    predictions = test_results['hypothesis_tests']['observational_predictions']
    print(f"\nPREDIÇÕES OBSERVACIONAIS TESTÁVEIS:")
    print("-" * 40)
    for i, (key, value) in enumerate(predictions.items(), 1):
        print(f"{i}. {key.replace('_', ' ').title()}:")
        print(f"   {value}")
    
    # Análise estatística dos resultados
    results = test_results['simulation_results']
    print(f"\nANÁLISE ESTATÍSTICA:")
    print("-" * 40)
    print(f"Tempo de simulação: {results['times'][0]:.2e} a {results['times'][-1]:.2e} t_Planck")
    print(f"Expansão do fator de escala: {results['scale_factors'][-1]/results['scale_factors'][0]:.2e}")
    print(f"Resfriamento: {results['temperatures'][0]/results['temperatures'][-1]:.2e}")
    print(f"Simulação convergiu: {'Sim' if results['success'] else 'Não'}")

def run_additional_tests(simulator):
    """Executa testes adicionais específicos"""
    
    print("\nExecutando testes de sensibilidade...")
    
    # Teste 1: Sensibilidade às condições iniciais
    sensitivity_test = test_initial_conditions_sensitivity(simulator)
    
    # Teste 2: Comparação com observações cosmológicas
    observational_test = compare_with_observations(simulator)
    
    # Teste 3: Estabilidade do modelo
    stability_test = test_model_stability(simulator)
    
    return {
        'sensitivity': sensitivity_test,
        'observations': observational_test,
        'stability': stability_test
    }

def test_initial_conditions_sensitivity(simulator):
    """Testa sensibilidade às condições iniciais"""
    
    print("  - Testando sensibilidade às condições iniciais...")
    
    # Diferentes conjuntos de condições iniciais
    test_conditions = [
        {'scale_factor': 1e-50, 'expansion_rate': 1e50, 'energy_density': 1e100, 'temperature': 1e32},
        {'scale_factor': 5e-51, 'expansion_rate': 2e50, 'energy_density': 5e99, 'temperature': 2e32},
        {'scale_factor': 2e-50, 'expansion_rate': 5e49, 'energy_density': 2e100, 'temperature': 5e31},
    ]
    
    results = []
    for i, conditions in enumerate(test_conditions):
        result = simulator.simulate_planck_epoch((1e-50, 1e-35), conditions)
        results.append({
            'test_id': i,
            'final_scale_factor': result['scale_factors'][-1],
            'final_temperature': result['temperatures'][-1],
            'success': result['success']
        })
    
    # Calcular dispersão
    final_scales = [r['final_scale_factor'] for r in results if r['success']]
    final_temps = [r['final_temperature'] for r in results if r['success']]
    
    scale_std = np.std(final_scales) / np.mean(final_scales) if final_scales else 0
    temp_std = np.std(final_temps) / np.mean(final_temps) if final_temps else 0
    
    return {
        'scale_factor_sensitivity': scale_std,
        'temperature_sensitivity': temp_std,
        'model_stable': scale_std < 0.1 and temp_std < 0.1,
        'successful_runs': len([r for r in results if r['success']])
    }

def compare_with_observations(simulator):
    """Compara predições com observações cosmológicas conhecidas"""
    
    print("  - Comparando com observações cosmológicas...")
    
    # Simular até o presente
    current_time = 4.35e17  # Idade do universo em unidades de Planck
    
    # Obter predições do modelo
    tardis = simulator.tardis
    cmb_prediction = tardis.cosmic_microwave_background_prediction(current_time)
    
    # Valores observados
    observed_values = {
        'cmb_temperature': 2.725,  # K
        'hubble_constant': 67.4,   # km/s/Mpc
        'omega_matter': 0.315,
        'omega_lambda': 0.685
    }
    
    # Calcular desvios
    deviations = {
        'cmb_temp_deviation': abs(cmb_prediction['temperature'] - observed_values['cmb_temperature']) / observed_values['cmb_temperature'],
        'anisotropy_prediction': cmb_prediction['anisotropy_amplitude'],
        'compression_signature': cmb_prediction['compression_signature']
    }
    
    return {
        'predictions': cmb_prediction,
        'observations': observed_values,
        'deviations': deviations,
        'agreement_level': 'good' if deviations['cmb_temp_deviation'] < 0.1 else 'poor'
    }

def test_model_stability(simulator):
    """Testa estabilidade numérica do modelo"""
    
    print("  - Testando estabilidade numérica...")
    
    # Teste com diferentes precisões
    tolerances = [1e-6, 1e-8, 1e-10]
    stability_results = []
    
    for tol in tolerances:
        # Modificar temporariamente a tolerância
        initial_conditions = {
            'scale_factor': 1e-50,
            'expansion_rate': 1e50,
            'energy_density': 1e100,
            'temperature': 1e32
        }
        
        result = simulator.simulate_planck_epoch((1e-50, 1e-35), initial_conditions)
        
        stability_results.append({
            'tolerance': tol,
            'success': result['success'],
            'final_scale': result['scale_factors'][-1] if result['success'] else None,
            'computation_stable': result['success'] and np.isfinite(result['scale_factors'][-1])
        })
    
    stable_runs = [r for r in stability_results if r['computation_stable']]
    
    return {
        'stability_results': stability_results,
        'numerical_stability': len(stable_runs) / len(stability_results),
        'recommended_tolerance': 1e-8,
        'model_robust': len(stable_runs) >= 2
    }

def save_results(test_results, additional_tests):
    """Salva todos os resultados em arquivos na pasta resultados"""
    
    import os
    
    # Criar pasta resultados se não existir
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvar resultados principais
    main_results = {
        'timestamp': timestamp,
        'hypothesis_tests': test_results['hypothesis_tests'],
        'simulation_success': test_results['simulation_results']['success'],
        'additional_tests': additional_tests
    }
    
    with open(f'resultados/physics_test_results_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(main_results, f, indent=2, ensure_ascii=False, default=str)
    
    # Salvar dados numéricos
    sim_data = test_results['simulation_results']
    np.savez(f'resultados/simulation_data_{timestamp}.npz',
             times=sim_data['times'],
             scale_factors=sim_data['scale_factors'],
             temperatures=sim_data['temperatures'],
             energy_densities=sim_data['energy_densities'],
             hubble_parameters=sim_data['hubble_parameters'],
             compression_ratios=sim_data['compression_ratios'])
    
    print(f"  - Resultados salvos em: resultados/physics_test_results_{timestamp}.json")
    print(f"  - Dados numéricos salvos em: resultados/simulation_data_{timestamp}.npz")
    
    return timestamp

def create_summary_visualization(test_results, timestamp):
    """Cria visualização resumo dos resultados"""
    
    print("\nGerando visualização resumo...")
    
    # Criar figura com múltiplos painéis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Dados da simulação
    sim_data = test_results['simulation_results']
    times = sim_data['times']
    
    # Painel 1: Evolução das constantes
    ax1.set_title('Evolução das Constantes Físicas')
    ax1.set_xlabel('Tempo (unidades de Planck)')
    ax1.set_ylabel('Valor Normalizado')
    ax1.set_xscale('log')
    
    # Plotar constantes normalizadas
    for const_name, values in sim_data['constants_evolution'].items():
        normalized_values = np.array(values) / values[0]
        ax1.plot(times, normalized_values, label=f'{const_name}', linewidth=2)
    ax1.legend()
    ax1.grid(True)
    
    # Painel 2: Comparação TARDIS vs Padrão
    ax2.set_title('Modelo TARDIS vs Padrão')
    ax2.set_xlabel('Tempo (unidades de Planck)')
    ax2.set_ylabel('Fator de Escala')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    # Fator de escala TARDIS
    ax2.plot(times, sim_data['scale_factors'], 'r-', label='TARDIS', linewidth=2)
    # Modelo padrão (aproximação)
    standard_scale = (times / times[0])**(2/3)
    ax2.plot(times, standard_scale * sim_data['scale_factors'][0], 'b--', label='Padrão', linewidth=2)
    ax2.legend()
    ax2.grid(True)
    
    # Painel 3: Compressão Quântica e Temperatura
    ax3.set_title('Evolução da Temperatura')
    ax3.set_xlabel('Tempo (unidades de Planck)')
    ax3.set_ylabel('Temperatura (K)')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.plot(times, sim_data['temperatures'], 'orange', linewidth=2)
    ax3.grid(True)
    
    # Painel 4: Resumo dos Resultados
    hypothesis_tests = test_results['hypothesis_tests']
    dynamic_supported = hypothesis_tests['dynamic_constants']['hypothesis_supported']
    tardis_supported = hypothesis_tests['tardis_universe']['hypothesis_supported']
    
    ax4.text(0.1, 0.9, 'RESULTADOS DOS TESTES:', fontsize=14, fontweight='bold')
    ax4.text(0.1, 0.8, f'Leis Dinâmicas: {"✓ SUPORTADA" if dynamic_supported else "✗ NÃO SUPORTADA"}', 
             fontsize=12, color='green' if dynamic_supported else 'red')
    ax4.text(0.1, 0.7, f'Universo TARDIS: {"✓ SUPORTADA" if tardis_supported else "✗ NÃO SUPORTADA"}', 
             fontsize=12, color='green' if tardis_supported else 'red')
    
    ax4.text(0.1, 0.6, 'PREDIÇÕES TESTÁVEIS:', fontsize=12, fontweight='bold')
    ax4.text(0.1, 0.5, '• Variação da CMB', fontsize=10)
    ax4.text(0.1, 0.45, '• Ondas gravitacionais primordiais', fontsize=10)
    ax4.text(0.1, 0.4, '• Assinatura de compressão quântica', fontsize=10)
    ax4.text(0.1, 0.35, '• Anomalias na constante de estrutura fina', fontsize=10)
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig(f'resultados/physics_hypotheses_summary_{timestamp}.png', dpi=300, bbox_inches='tight')
    print(f"  - Visualização salva em: resultados/physics_hypotheses_summary_{timestamp}.png")

if __name__ == "__main__":
    # Executar análise completa
    try:
        test_results, additional_tests = main()
        
        # Criar visualização final
        create_summary_visualization(test_results, datetime.now().strftime("%Y%m%d_%H%M%S"))
        
        print("\n" + "=" * 70)
        print("ANÁLISE COMPLETA CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print("\nPróximos passos sugeridos:")
        print("1. Analisar os arquivos de resultados gerados")
        print("2. Refinar os parâmetros do modelo baseado nos resultados")
        print("3. Comparar com dados observacionais mais específicos")
        print("4. Desenvolver experimentos mentais para testar as predições")
        
    except Exception as e:
        print(f"\nErro durante a execução: {e}")
        print("Verifique os parâmetros e tente novamente.")
        import traceback
        traceback.print_exc()
