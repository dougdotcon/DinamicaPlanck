"""
Simulador da Época de Planck com leis físicas dinâmicas
Integra ambas as hipóteses: constantes variáveis e universo TARDIS
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from constants_physics import DynamicPhysicsConstants
from tardis_universe_model import TARDISUniverse
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple

class PlanckEpochSimulator:
    """
    Simulador completo da época de Planck integrando:
    1. Constantes físicas dinâmicas
    2. Modelo do universo TARDIS
    3. Efeitos quânticos gravitacionais
    """
    
    def __init__(self):
        self.physics = DynamicPhysicsConstants()
        self.tardis = TARDISUniverse()
        
        # Parâmetros da simulação
        self.planck_time = 5.391e-44  # segundos
        self.planck_length = 1.616e-35  # metros
        self.planck_mass = 2.176e-8   # kg
        self.planck_energy = 1.956e9  # J
        
        # Configurar eventos supercosmicos
        self._setup_supercosmic_events()
        
    def _setup_supercosmic_events(self):
        """Configura eventos supercosmicos que alteram as leis físicas"""
        
        # Big Bang - altera todas as constantes fundamentais
        self.physics.add_supercosmic_event(
            time=0, 
            event_type='big_bang',
            affected_constants=['c', 'G', 'h', 'k_B', 'alpha'],
            intensity=1.0
        )
        
        # Separação das forças fundamentais
        self.physics.add_supercosmic_event(
            time=1e-43,  # Tempo de Planck
            event_type='gravity_separation',
            affected_constants=['G', 'c'],
            intensity=0.9
        )
        
        # Início da inflação
        self.physics.add_supercosmic_event(
            time=1e-36,
            event_type='inflation_start',
            affected_constants=['h', 'c'],
            intensity=0.8
        )
        
        # Fim da inflação
        self.physics.add_supercosmic_event(
            time=1e-32,
            event_type='inflation_end',
            affected_constants=['h', 'alpha'],
            intensity=0.7
        )
        
    def quantum_gravity_equations(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        Sistema de equações diferenciais para gravitação quântica
        na época de Planck com leis físicas dinâmicas
        
        Args:
            t: Tempo (unidades de Planck)
            y: Vetor de estado [a, da/dt, rho, T] onde:
                a = fator de escala interno
                da/dt = taxa de expansão interna
                rho = densidade de energia
                T = temperatura
                
        Returns:
            Derivadas do vetor de estado
        """
        a, a_dot, rho, T = y
        
        # Obter constantes físicas no tempo atual
        G = self.physics.get_constant('G', t)
        c = self.physics.get_constant('c', t)
        h = self.physics.get_constant('h', t)
        k_B = self.physics.get_constant('k_B', t)
        
        # Parâmetro de Hubble interno
        H = a_dot / a if a > 0 else 0
        
        # Equação de Friedmann modificada para o modelo TARDIS
        # Considera que a curvatura externa é fixa
        external_constraint = self.tardis.external_radius
        compression_factor = self.tardis.quantum_compression_ratio(t)
        
        # Densidade crítica modificada
        rho_crit = 3 * H**2 / (8 * np.pi * G) * compression_factor
        
        # Equação de estado para a época de Planck
        # Mistura de radiação e flutuações quânticas
        pressure = rho / 3  # Radiação
        quantum_pressure = h * c / (self.planck_length**4) * np.exp(-t)
        total_pressure = pressure + quantum_pressure
        
        # Equações de evolução
        # d²a/dt² = -4πG/3 * a * (rho + 3P/c²)
        a_ddot = -4 * np.pi * G / (3 * c**2) * a * (rho + 3 * total_pressure)
        
        # Conservação de energia: drho/dt = -3H(rho + P/c²)
        rho_dot = -3 * H * (rho + total_pressure / c**2)
        
        # Evolução da temperatura
        # Para radiação: T ∝ 1/a, mas com correções quânticas
        quantum_correction = 1 + h / (k_B * T * self.planck_time) if T > 0 else 1
        T_dot = -H * T * quantum_correction
        
        return np.array([a_dot, a_ddot, rho_dot, T_dot])
    
    def simulate_planck_epoch(self, t_span: Tuple[float, float], 
                             initial_conditions: Dict) -> Dict:
        """
        Simula a evolução durante a época de Planck
        
        Args:
            t_span: (t_inicial, t_final) em unidades de Planck
            initial_conditions: Condições iniciais
            
        Returns:
            Resultados da simulação
        """
        # Condições iniciais
        y0 = np.array([
            initial_conditions.get('scale_factor', 1e-50),
            initial_conditions.get('expansion_rate', 1e50),
            initial_conditions.get('energy_density', 1e100),
            initial_conditions.get('temperature', 1e32)
        ])
        
        # Resolver sistema de EDOs com parâmetros mais estáveis
        sol = solve_ivp(
            self.quantum_gravity_equations,
            t_span,
            y0,
            method='RK45',
            dense_output=True,
            rtol=1e-6,
            atol=1e-8,
            max_step=1e-35  # Limitar tamanho do passo
        )
        
        if not sol.success:
            print(f"Aviso: Simulação pode ter problemas de convergência")
        
        # Processar resultados
        times = sol.t
        scale_factors = sol.y[0]
        expansion_rates = sol.y[1]
        energy_densities = sol.y[2]
        temperatures = sol.y[3]
        
        # Calcular quantidades derivadas
        hubble_params = expansion_rates / scale_factors
        compression_ratios = [self.tardis.quantum_compression_ratio(t) for t in times]
        
        # Evolução das constantes físicas
        constants_evolution = {
            'c': [self.physics.get_constant('c', t) for t in times],
            'G': [self.physics.get_constant('G', t) for t in times],
            'h': [self.physics.get_constant('h', t) for t in times],
            'alpha': [self.physics.get_constant('alpha', t) for t in times],
        }
        
        return {
            'times': times,
            'scale_factors': scale_factors,
            'expansion_rates': expansion_rates,
            'energy_densities': energy_densities,
            'temperatures': temperatures,
            'hubble_parameters': hubble_params,
            'compression_ratios': compression_ratios,
            'constants_evolution': constants_evolution,
            'success': sol.success
        }
    
    def compare_with_standard_model(self, results: Dict) -> Dict:
        """
        Compara resultados com o modelo cosmológico padrão
        
        Args:
            results: Resultados da simulação
            
        Returns:
            Comparação com predições padrão
        """
        times = results['times']
        
        # Modelo padrão (constantes fixas, expansão normal)
        standard_scale = times**(2/3)  # Expansão dominada por radiação
        standard_temp = 1e32 / times**(1/2)  # T ∝ 1/√t para radiação
        
        comparison = {
            'standard_scale_factors': standard_scale,
            'standard_temperatures': standard_temp,
            'tardis_scale_factors': results['scale_factors'],
            'tardis_temperatures': results['temperatures'],
            'scale_factor_ratio': results['scale_factors'] / standard_scale,
            'temperature_ratio': results['temperatures'] / standard_temp
        }
        
        return comparison
    
    def plot_simulation_results(self, results: Dict, comparison: Dict = None):
        """
        Visualiza os resultados da simulação
        
        Args:
            results: Resultados da simulação
            comparison: Comparação com modelo padrão (opcional)
        """
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Evolução do Fator de Escala',
                'Evolução da Temperatura',
                'Parâmetro de Hubble vs Compressão',
                'Evolução das Constantes Físicas',
                'Densidade de Energia',
                'Comparação: TARDIS vs Modelo Padrão'
            )
        )
        
        times = results['times']
        
        # Fator de escala
        fig.add_trace(
            go.Scatter(x=times, y=results['scale_factors'],
                      name='Fator de Escala TARDIS', line=dict(color='red')),
            row=1, col=1
        )
        
        # Temperatura
        fig.add_trace(
            go.Scatter(x=times, y=results['temperatures'],
                      name='Temperatura', line=dict(color='orange')),
            row=1, col=2
        )
        
        # Hubble vs Compressão
        fig.add_trace(
            go.Scatter(x=times, y=results['hubble_parameters'],
                      name='Parâmetro de Hubble', line=dict(color='blue')),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=times, y=results['compression_ratios'],
                      name='Razão de Compressão', line=dict(color='green'),
                      yaxis='y2'),
            row=2, col=1
        )
        
        # Constantes físicas
        for const_name, values in results['constants_evolution'].items():
            fig.add_trace(
                go.Scatter(x=times, y=np.array(values) / values[0],
                          name=f'{const_name} (normalizado)'),
                row=2, col=2
            )
        
        # Densidade de energia
        fig.add_trace(
            go.Scatter(x=times, y=results['energy_densities'],
                      name='Densidade de Energia', line=dict(color='purple')),
            row=3, col=1
        )
        
        # Comparação se disponível
        if comparison:
            fig.add_trace(
                go.Scatter(x=times, y=comparison['scale_factor_ratio'],
                          name='Razão Fator Escala (TARDIS/Padrão)',
                          line=dict(color='red')),
                row=3, col=2
            )
            fig.add_trace(
                go.Scatter(x=times, y=comparison['temperature_ratio'],
                          name='Razão Temperatura (TARDIS/Padrão)',
                          line=dict(color='orange')),
                row=3, col=2
            )
        
        # Configurar eixos
        fig.update_xaxes(type="log", title_text="Tempo (unidades de Planck)")
        fig.update_yaxes(type="log")
        
        fig.update_layout(
            title_text="Simulação da Época de Planck - Modelo TARDIS com Leis Dinâmicas",
            height=1000,
            showlegend=True
        )
        
        fig.show()
    
    def test_hypotheses(self) -> Dict:
        """
        Testa as duas hipóteses principais
        
        Returns:
            Resultados dos testes
        """
        print("Testando Hipóteses da Física Teórica...")
        print("=" * 50)
        
        # Simular época de Planck com parâmetros mais realistas
        t_span = (1e-43, 1e-30)  # Do tempo de Planck até fim da inflação
        initial_conditions = {
            'scale_factor': 1e-30,    # Tamanho inicial mais razoável
            'expansion_rate': 1e13,   # Taxa de expansão inicial mais moderada
            'energy_density': 1e113,  # Densidade de Planck real
            'temperature': 1.4e32     # Temperatura de Planck real
        }
        
        results = self.simulate_planck_epoch(t_span, initial_conditions)
        comparison = self.compare_with_standard_model(results)
        
        # Análise das hipóteses
        hypothesis_tests = {
            'dynamic_constants': self._test_dynamic_constants(results),
            'tardis_universe': self._test_tardis_model(results),
            'observational_predictions': self._generate_predictions(results)
        }
        
        return {
            'simulation_results': results,
            'comparison': comparison,
            'hypothesis_tests': hypothesis_tests
        }
    
    def _test_dynamic_constants(self, results: Dict) -> Dict:
        """Testa a hipótese de constantes dinâmicas"""
        constants_evolution = results['constants_evolution']
        
        # Calcular variações percentuais
        variations = {}
        for const, values in constants_evolution.items():
            initial_value = values[0]
            final_value = values[-1]
            max_variation = max(values) - min(values)
            
            variations[const] = {
                'initial': initial_value,
                'final': final_value,
                'change_percent': abs(final_value - initial_value) / initial_value * 100,
                'max_variation_percent': max_variation / initial_value * 100
            }
        
        return {
            'variations': variations,
            'hypothesis_supported': any(v['max_variation_percent'] > 1 for v in variations.values()),
            'most_variable_constant': max(variations.keys(), 
                                        key=lambda k: variations[k]['max_variation_percent'])
        }
    
    def _test_tardis_model(self, results: Dict) -> Dict:
        """Testa a hipótese do universo TARDIS"""
        compression_ratios = results['compression_ratios']
        scale_factors = results['scale_factors']
        
        # Verificar se compressão aumenta enquanto tamanho externo permanece fixo
        compression_growth = compression_ratios[-1] / compression_ratios[0]
        internal_growth = scale_factors[-1] / scale_factors[0]
        
        return {
            'compression_growth_factor': compression_growth,
            'internal_growth_factor': internal_growth,
            'external_size_constant': True,  # Por definição no modelo
            'hypothesis_supported': compression_growth > 1e10,  # Crescimento significativo
            'quantum_compression_signature': np.std(compression_ratios) / np.mean(compression_ratios)
        }
    
    def _generate_predictions(self, results: Dict) -> Dict:
        """Gera predições observacionais testáveis"""
        return {
            'cmb_temperature_deviation': "Desvios na temperatura da CMB devido à compressão quântica",
            'gravitational_wave_signature': "Assinatura específica em ondas gravitacionais primordiais",
            'fine_structure_constant_variation': f"Variação de α: {results['constants_evolution']['alpha'][-1] / results['constants_evolution']['alpha'][0] - 1:.2e}",
            'cosmic_acceleration_anomaly': "Aceleração cósmica aparente vs real",
            'quantum_foam_effects': "Efeitos de espuma quântica na estrutura do espaço-tempo"
        }

if __name__ == "__main__":
    # Executar simulação completa
    simulator = PlanckEpochSimulator()
    test_results = simulator.test_hypotheses()
    
    # Exibir resultados
    print("\nResultados dos Testes de Hipóteses:")
    print("=" * 50)
    
    # Teste de constantes dinâmicas
    dynamic_test = test_results['hypothesis_tests']['dynamic_constants']
    print(f"\n1. Hipótese de Constantes Dinâmicas:")
    print(f"   Suportada: {dynamic_test['hypothesis_supported']}")
    print(f"   Constante mais variável: {dynamic_test['most_variable_constant']}")
    
    for const, var in dynamic_test['variations'].items():
        print(f"   {const}: variação máxima de {var['max_variation_percent']:.2f}%")
    
    # Teste do modelo TARDIS
    tardis_test = test_results['hypothesis_tests']['tardis_universe']
    print(f"\n2. Hipótese do Universo TARDIS:")
    print(f"   Suportada: {tardis_test['hypothesis_supported']}")
    print(f"   Fator de crescimento da compressão: {tardis_test['compression_growth_factor']:.2e}")
    print(f"   Fator de crescimento interno: {tardis_test['internal_growth_factor']:.2e}")
    
    # Predições
    predictions = test_results['hypothesis_tests']['observational_predictions']
    print(f"\n3. Predições Observacionais:")
    for key, value in predictions.items():
        print(f"   {key}: {value}")
    
    # Plotar resultados
    simulator.plot_simulation_results(
        test_results['simulation_results'],
        test_results['comparison']
    )
