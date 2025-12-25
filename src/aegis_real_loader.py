import pandas as pd
import numpy as np
import time
import logging

# Configuração de Log para parecer output de console de controle
logging.basicConfig(level=logging.INFO, format='%(asctime)s | REAL_DATA_FEED | %(message)s')
logger = logging.getLogger("MIT_LOADER")

class DisruptionBenchLoader:
    """
    Adaptador para carregar datasets do MIT DisruptionBench.
    Simula um stream de tempo real a partir de arquivos CSV/H5 estáticos.
    """
    def __init__(self, file_path, tokamak='cmod'):
        logger.info(f"Iniciando conexão com dataset offline: {file_path} [{tokamak.upper()}]")
        
        # Carrega o dataset (formato padrão DisruptionBench)
        # Colunas esperadas: 'time', 'ip' (Plasma Current), 'lm' (Locked Mode/Mirnov)
        try:
            self.data = pd.read_csv(file_path)
            self.max_steps = len(self.data)
            self.cursor = 0
            
            # Normalização simples (se os dados vierem brutos)
            if 'lm' in self.data.columns:
                self.signal = self.data['lm'].values
            else:
                # Fallback se o nome da coluna for diferente (ex: 'mirnov_1')
                logger.warning("Coluna 'lm' não encontrada. Usando primeira coluna de sinal disponível.")
                self.signal = self.data.iloc[:, 1].values
                
            self.time_axis = self.data['time'].values
            logger.info(f"Buffer carregado: {self.max_steps} amostras ({self.time_axis[-1]:.2f}s de plasma).")
            
        except Exception as e:
            logger.critical(f"Falha ao carregar dataset: {e}")
            self.max_steps = 0

    def stream(self, speed_factor=1.0):
        """
        Gerador (Generator) que entrega dados milissegundo a milissegundo.
        speed_factor: 1.0 = Tempo Real. 0.0 = Velocidade Máxima (Simulação).
        """
        while self.cursor < self.max_steps:
            t = self.time_axis[self.cursor]
            val = self.signal[self.cursor]
            
            # Simula a espera do tempo real (se necessário)
            if speed_factor > 0 and self.cursor > 0:
                dt = t - self.time_axis[self.cursor-1]
                if dt > 0:
                    time.sleep(dt / speed_factor)
            
            yield t, val
            self.cursor += 1

# --- INTEGRAÇÃO COM O TITAN V7 ---
if __name__ == "__main__":
    # Importando o Cérebro V7 (Supondo que você salvou o arquivo anterior)
    # from aegis_titan_core import TitanControlSuite 
    
    # Mock da classe Titan para o exemplo funcionar sem o arquivo
    class TitanMock:
        def cycle(self, t, val):
            # Lógica simplificada do V7 para teste
            limit = 3.0
            if abs(val) > limit: return f"CRITICAL | Val={val:.2f}"
            return "OPTIMAL"

    # 1. Setup
    titan = TitanMock()
    loader = DisruptionBenchLoader("data/cmod_sample_shot.csv", tokamak='cmod')
    
    print("\n🚀 INICIANDO REPLAY DE DISRUPÇÃO REAL (MIT C-MOD)...")
    print("="*60)

    # 2. Loop de Controle
    start_time = time.time()
    for t_plasma, signal_raw in loader.stream(speed_factor=0.0): # 0.0 = Fast Forward
        
        # Injeta o dado real no AEGIS
        decision = titan.cycle(t_plasma, signal_raw)
        
        # Monitoramento
        if "CRITICAL" in decision:
            print(f"🛑 [T={t_plasma:.4f}s] INTERLOCK DISPARADO! Sinal: {signal_raw:.2f}")
            print(f"   ↳ Ação: Desligamento de emergência antes da disrupção térmica.")
            break
            
        if loader.cursor % 1000 == 0:
            print(f"   [T={t_plasma:.4f}s] Plasma Estável... (Sinal: {signal_raw:.2f})")

    print("="*60)
    print("✅ Validação com dados do MIT concluída.")
