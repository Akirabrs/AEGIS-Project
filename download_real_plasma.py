import requests
import os

def download_cmod_shot():
    # URL direta para um arquivo de exemplo do DisruptionBench (Hospedado publicamente)
    # Este é um disparo disruptivo clássico do C-Mod usado em papers
    url = "https://zenodo.org/record/6366146/files/CMod_disruption_sample.csv?download=1"
    
    filename = "data/cmod_real_shot.csv"
    os.makedirs("data", exist_ok=True)
    
    print(f"⬇️ Iniciando download de dados reais do MIT (Alcator C-Mod)...")
    print(f"   Alvo: {filename}")
    
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filename, 'wb') as f:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                
        print(f"✅ Download concluído! Tamanho: {total_size/1024:.2f} KB")
        print(f"   Agora você tem plasma real para injetar no AEGIS.")
        
    except Exception as e:
        print(f"❌ Erro no download: {e}")
        print("   Alternativa: Baixe manualmente 'DisruptionBench' no Zenodo.")

if __name__ == "__main__":
    download_cmod_shot()
