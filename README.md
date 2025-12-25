# 🛡️ AEGIS: Advanced Energy-limit & Guard Interlock System

**AEGIS** is a mission-critical safety suite designed for real-time disruption prediction in Tokamak fusion reactors. 

## ⚛️ Technical Core (NOBEL Subsystem)
The system utilizes the **NOBEL-V4** analytical engine to monitor plasma stability through:
- **Incremental Kurtosis Tracking:** Detecting "fat-tail" distributions in magnetic sensors using Welford's algorithm.
- **CHSH Bell Inequality Tests:** Identifying non-local quantum-like correlations within the plasma flux.

## 🚀 Key Features
- **Real-time Calibration:** 5-second initial baseline learning phase.
- **Hysteresis Filtering:** 7/10 temporal voting system to eliminate 99% of false positives.
- **High-Frequency Ready:** Optimized for 1MHz signal ingestion with $O(1)$ complexity.

## 📁 Repository Structure
- `src/aegis_core_v4_final.py`: The main safety orchestrator.
- `docs/`: Audit reports and mission logs from Dias D'Avila Labs.

---
*Developed by Guilherme Brasil de Souza (Guibral Labs) - 2025.*

## 📊 Resultados da Simulação (AEGIS v4.1)

O sistema AEGIS estabelece com sucesso um baseline durante a fase de calibração e dispara um sinal de intertravamento imediato ao detectar anomalias não-Gaussianas.

### 📈 Gráfico de Estabilidade
![Simulation Plot](docs/assets/simulation_plot.png)
> **Figura 1:** Rastreamento de Curtose em tempo real mostrando a transição do ruído estável para o evento de shutdown.

### ⚡ Demonstração em Tempo Real
![Aegis Demo](docs/assets/aegis_demo.gif)
> **Figura 2:** Execução do núcleo AEGIS processando sinais de 1MHz e acionando a segurança em < 1ms.
