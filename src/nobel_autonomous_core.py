import time
import numpy as np
from aegis_titan_core import TitanControlSuite  # Seu cérebro V7
from kronos_safety_integrated import KronosSafetyResponse # Sua interface de hardware

class NobelAutonomousSystem:
    def __init__(self):
        print("🤖 INICIALIZANDO NOBEL AUTONOMOUS CORE...")
        
        # 1. O Cérebro (Predição)
        self.brain = TitanControlSuite()
        
        # 2. O Músculo (Ação Física)
        self.muscle = KronosSafetyResponse()
        
        # Estado de Conexão
        self.active = True
        print("✅ Sistemas Integrados: AEGIS TITAN <--> KRONOS HARDWARE")

    def run_cycle_realtime(self, t_ms, plasma_signal):
        """
        Ciclo de Controle Autônomo (Target: <1ms latência de decisão)
        """
        # --- ETAPA 1: PERCEPÇÃO & PREDIÇÃO (TITAN) ---
        # O Titan analisa o sinal e prevê o futuro
        # Retorna status e a ação recomendada baseada na previsão
        titan_result = self.brain.cycle(t_ms, plasma_signal)
        
        # --- ETAPA 2: TRADUÇÃO DE INTENÇÃO ---
        # Converter a "vontade" do Titan em "protocolos" do Kronos
        threat_level = 0
        
        if "CRITICAL" in titan_result:
            threat_level = 4 # EMERGÊNCIA TOTAL
        elif "PREDICTIVE_WARNING" in titan_result:
            threat_level = 2 # AÇÃO CORRETIVA (Protocolo 1)
        elif "WARNING" in titan_result:
            threat_level = 1 # MONITORAMENTO
            
        # --- ETAPA 3: ATUAÇÃO FÍSICA (KRONOS) ---
        # Se houver ameaça, o hardware executa sem perguntar
        if threat_level > 0:
            # Aqui fechamos o loop: O cérebro digital move o relé físico
            # Usamos métricas sintéticas aqui só para compatibilidade com a função existente
            dummy_ghost = {'warning_score': threat_level / 4.0}
            dummy_quantum = {'bell_parameter': 2.0 + (threat_level * 0.1)}
            
            # O Kronos decide e executa em <50ms
            real_threat, protocol = self.muscle.evaluate_threat(dummy_ghost, dummy_quantum)
            
            if real_threat >= threat_level:
                self.muscle.execute_safety_protocol(real_threat)
                print(f"🛡️ [T={t_ms}ms] KRONOS ATUOU: {protocol['name']} (Causa: {titan_result})")
                
                if threat_level == 4:
                    return False # Parar loop em emergência
                    
        return True

# --- SIMULAÇÃO FINAL: DADOS REAIS + HARDWARE VIRTUAL ---
if __name__ == "__main__":
    # 1. Carregar Dados Reais (do script de download)
    try:
        import pandas as pd
        data = pd.read_csv("data/cmod_real_shot.csv")
        signal_stream = data.iloc[:, 1].values # Pega a coluna de sinal
        time_stream = data.iloc[:, 0].values
        print("📂 Dados do C-Mod carregados para injeção.")
    except:
        print("⚠️ Dados reais não encontrados. Usando gerador sintético para teste.")
        signal_stream = np.random.normal(0, 1, 2000)
        time_stream = np.arange(2000)

    # 2. Iniciar Sistema Autônomo
    nobel = NobelAutonomousSystem()
    
    print("\n🚀 INICIANDO OPERAÇÃO AUTÔNOMA...")
    for i, t in enumerate(time_stream):
        sig = signal_stream[i]
        
        # Injeta o sinal no sistema
        keep_running = nobel.run_cycle_realtime(t*1000, sig) # t em ms
        
        if not keep_running:
            print(f"🛑 SISTEMA PAROU EM SEGURANÇA EM T={t:.4f}s")
            break
            
        # Simula tempo real (opcional, remover para processamento em lote)
        # time.sleep(0.001)
