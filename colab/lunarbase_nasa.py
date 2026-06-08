# ============================================================
# LunarBase — Coleta de Dados NASA + Classificação de Risco
# Google Colab — execute célula por célula
# Dados até: 08/06/2026
# ============================================================

# CÉLULA 1 — Instalar dependências
# !pip install pandas scikit-learn requests --quiet

# ============================================================
# CÉLULA 2 — Imports
# ============================================================
import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

print("Bibliotecas carregadas com sucesso.")

# ============================================================
# CÉLULA 3 — Buscar dados reais da NASA DONKI (tempestades solares)
# API pública, sem chave necessária
# ============================================================

def fetch_solar_events():
    """
    Busca eventos solares reais dos últimos 30 dias.
    NASA DONKI API — https://kauai.ccmc.gsfc.nasa.gov/DONKI/
    Não requer chave de API.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    events = []
    
    # CME — Coronal Mass Ejections (ejeções de massa coronal)
    try:
        url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?startDate={start_str}&endDate={end_str}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            cmes = r.json()
            for cme in cmes:
                events.append({
                    'tipo': 'CME',
                    'data': cme.get('startTime', '')[:10],
                    'velocidade_km_s': float(cme.get('cmeAnalyses', [{}])[0].get('speed', 0) or 0),
                    'latitude': float(cme.get('cmeAnalyses', [{}])[0].get('latitude', 0) or 0),
                    'fonte': 'NASA DONKI CME'
                })
        print(f"CMEs encontrados: {len([e for e in events if e['tipo']=='CME'])}")
    except Exception as e:
        print(f"Aviso CME: {e}")

    # Solar Flares (erupções solares)
    try:
        url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate={start_str}&endDate={end_str}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            flares = r.json()
            for f in flares:
                classe = f.get('classType', 'A1.0')
                # Converter classe em valor numérico
                letra = classe[0] if classe else 'A'
                num = float(classe[1:] if len(classe) > 1 else 1.0)
                multiplicador = {'A': 1, 'B': 10, 'C': 100, 'M': 1000, 'X': 10000}.get(letra, 1)
                intensidade = num * multiplicador
                events.append({
                    'tipo': 'FLARE',
                    'data': f.get('beginTime', '')[:10],
                    'velocidade_km_s': intensidade / 100,
                    'latitude': 0,
                    'fonte': f'NASA DONKI FLARE {classe}'
                })
        print(f"Solar Flares encontrados: {len([e for e in events if e['tipo']=='FLARE'])}")
    except Exception as e:
        print(f"Aviso Flare: {e}")

    # Geomagnetic Storms (tempestades geomagnéticas)
    try:
        url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/GST?startDate={start_str}&endDate={end_str}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            storms = r.json()
            for s in storms:
                kp = s.get('allKpIndex', [{}])
                kp_val = float(kp[0].get('kpIndex', 0) if kp else 0)
                events.append({
                    'tipo': 'GEOMAG',
                    'data': s.get('startTime', '')[:10],
                    'velocidade_km_s': kp_val * 50,
                    'latitude': 0,
                    'fonte': f'NASA DONKI GEOMAG Kp={kp_val}'
                })
        print(f"Tempestades Geomagnéticas: {len([e for e in events if e['tipo']=='GEOMAG'])}")
    except Exception as e:
        print(f"Aviso GEOMAG: {e}")

    return events

solar_events = fetch_solar_events()
print(f"\nTotal de eventos solares coletados: {len(solar_events)}")

# ============================================================
# CÉLULA 4 — Buscar asteroides próximos (NASA NeoWs)
# API pública — requer chave gratuita OU usa DEMO_KEY (limite 30/hora)
# ============================================================

def fetch_asteroids():
    """
    Busca asteroides próximos da Terra nos próximos 7 dias.
    NASA NeoWs — https://api.nasa.gov/neo/rest/v1/feed
    DEMO_KEY = chave de demonstração gratuita, sem cadastro.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=3)
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    asteroids = []
    
    try:
        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_str}&end_date={end_str}&api_key=DEMO_KEY"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for date_key, neos in data.get('near_earth_objects', {}).items():
                for neo in neos:
                    diametro = neo.get('estimated_diameter', {}).get('kilometers', {})
                    diametro_max = float(diametro.get('estimated_diameter_max', 0))
                    
                    close_approach = neo.get('close_approach_data', [{}])[0]
                    distancia_lunar = float(close_approach.get('miss_distance', {}).get('lunar', 999))
                    velocidade = float(close_approach.get('relative_velocity', {}).get('kilometers_per_second', 0))
                    
                    asteroids.append({
                        'nome': neo.get('name', 'Desconhecido'),
                        'data': date_key,
                        'diametro_km': round(diametro_max, 4),
                        'distancia_lunar': round(distancia_lunar, 2),
                        'velocidade_km_s': round(velocidade, 2),
                        'potencialmente_perigoso': neo.get('is_potentially_hazardous_asteroid', False),
                        'fonte': 'NASA NeoWs'
                    })
        print(f"Asteroides encontrados: {len(asteroids)}")
    except Exception as e:
        print(f"Aviso NeoWs: {e}")
        asteroids = []
    
    return asteroids

asteroids = fetch_asteroids()
print(f"Total de asteroides coletados: {len(asteroids)}")
if asteroids:
    df_ast = pd.DataFrame(asteroids)
    print("\nAsteroides mais próximos:")
    print(df_ast.sort_values('distancia_lunar').head(5)[['nome','distancia_lunar','velocidade_km_s','potencialmente_perigoso']])

# ============================================================
# CÉLULA 5 — Classificação de Risco com Machine Learning
# RandomForestClassifier para classificar nível de risco
# ============================================================

def classify_risk_ml(solar_events, asteroids):
    """
    Usa RandomForestClassifier para classificar o nível de risco
    da missão lunar com base nos dados reais da NASA.
    
    Níveis: 0=Baixo, 1=Moderado, 2=Alto, 3=Crítico
    """
    
    # Criar dataset de features
    features = []
    
    # Features de eventos solares
    n_cme = len([e for e in solar_events if e['tipo'] == 'CME'])
    n_flare = len([e for e in solar_events if e['tipo'] == 'FLARE'])
    n_geomag = len([e for e in solar_events if e['tipo'] == 'GEOMAG'])
    max_vel_solar = max([e['velocidade_km_s'] for e in solar_events], default=0)
    
    # Features de asteroides
    n_perigosos = len([a for a in asteroids if a['potencialmente_perigoso']])
    distancia_min = min([a['distancia_lunar'] for a in asteroids], default=999)
    vel_max_ast = max([a['velocidade_km_s'] for a in asteroids], default=0)
    
    features = [n_cme, n_flare, n_geomag, max_vel_solar,
                n_perigosos, distancia_min, vel_max_ast]
    
    # Dataset de treinamento sintético baseado em parâmetros reais NASA
    # (em produção real seria substituído por histórico de missões)
    X_train = np.array([
        [0, 0, 0, 0, 0, 999, 0],      # Sem eventos — risco baixo
        [0, 1, 0, 100, 0, 50, 5],     # Flare fraco — baixo
        [1, 2, 0, 400, 0, 30, 10],    # CME lento — moderado
        [1, 3, 1, 600, 1, 20, 15],    # CME + flare — moderado
        [2, 4, 1, 800, 1, 15, 20],    # Múltiplos eventos — alto
        [3, 5, 2, 1200, 2, 10, 25],   # CME rápido + asteroides — alto
        [4, 6, 3, 2000, 3, 5, 35],    # Tempestade severa — crítico
        [5, 8, 4, 3000, 4, 2, 50],    # Condições extremas — crítico
    ])
    y_train = np.array([0, 0, 1, 1, 2, 2, 3, 3])
    
    labels = ['Baixo', 'Moderado', 'Alto', 'Crítico']
    
    # Normalizar features
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_real = scaler.transform([features])
    
    # Treinar e classificar
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_train)
    
    nivel = int(clf.predict(X_real)[0])
    probabilidades = clf.predict_proba(X_real)[0]
    importancias = clf.feature_importances_
    
    feature_names = ['CMEs', 'Flares', 'Geomag', 'Vel.Solar',
                     'Ast.Perigosos', 'Dist.Lunar', 'Vel.Ast']
    
    print("\n=== CLASSIFICAÇÃO DE RISCO ML ===")
    print(f"Nível de risco: {labels[nivel]} ({nivel}/3)")
    print(f"Confiança: {probabilidades[nivel]*100:.1f}%")
    print("\nImportância das features:")
    for name, imp in sorted(zip(feature_names, importancias), key=lambda x: -x[1]):
        print(f"  {name}: {imp:.3f}")
    
    return {
        'nivel': nivel,
        'label': labels[nivel],
        'confianca': round(float(probabilidades[nivel]) * 100, 1),
        'features': dict(zip(feature_names, [round(f, 2) for f in features])),
        'importancias': dict(zip(feature_names, [round(float(i), 3) for i in importancias]))
    }

risco = classify_risk_ml(solar_events, asteroids)

# ============================================================
# CÉLULA 6 — Montar JSON final para o jogo
# ============================================================

def build_game_json(solar_events, asteroids, risco):
    """
    Monta o JSON que o jogo HTML vai consumir.
    """
    hoje = datetime.utcnow().strftime('%Y-%m-%d')
    
    # Eventos mais recentes e relevantes para o jogo
    eventos_recentes = sorted(solar_events, key=lambda x: x['data'], reverse=True)[:5]
    asteroides_proximos = sorted(asteroids, key=lambda x: x['distancia_lunar'])[:3]
    
    # Gerar mensagem de alerta baseada no risco
    alertas = {
        0: "Condições espaciais favoráveis. Missão pode prosseguir normalmente.",
        1: "Atividade solar moderada detectada. Monitorar painéis e sistemas de comunicação.",
        2: "Atividade solar elevada. Protocolo de proteção contra radiação recomendado.",
        3: "ALERTA CRÍTICO: Condições espaciais severas. Mover tripulação para módulo blindado."
    }
    
    # Evento do dia para o jogo (gerado pelos dados reais)
    evento_do_dia = None
    if risco['nivel'] >= 3 and len([e for e in solar_events if e['tipo'] == 'CME']) > 0:
        evento_do_dia = {
            'tipo': 'tempestade',
            'titulo': 'Tempestade Solar Real Detectada',
            'descricao': f"NASA DONKI registrou {risco['features']['CMEs']} CME(s) nos últimos 30 dias.",
            'impacto': {'energia': -25, 'o2': 0}
        }
    elif len([a for a in asteroids if a['potencialmente_perigoso']]) > 0:
        evento_do_dia = {
            'tipo': 'meteorito',
            'titulo': 'Asteroide Potencialmente Perigoso',
            'descricao': f"NASA NeoWs detectou {risco['features']['Ast.Perigosos']} asteroide(s) classificados como potencialmente perigosos.",
            'impacto': {'energia': -10, 'o2': -8}
        }
    
    payload = {
        'gerado_em': datetime.utcnow().isoformat() + 'Z',
        'data_referencia': hoje,
        'fonte': 'NASA DONKI + NASA NeoWs — dados públicos',
        'aviso': 'Dados baseados em documentação pública da NASA. Base atualizada até 08/06/2026.',
        'risco': risco,
        'alerta_missao': alertas[risco['nivel']],
        'evento_do_dia': evento_do_dia,
        'resumo': {
            'total_eventos_solares': len(solar_events),
            'cmes_30_dias': risco['features']['CMEs'],
            'flares_30_dias': risco['features']['Flares'],
            'asteroides_proximos': len(asteroids),
            'asteroides_perigosos': risco['features']['Ast.Perigosos'],
            'distancia_lunar_minima': risco['features']['Dist.Lunar']
        },
        'eventos_solares': eventos_recentes,
        'asteroides': asteroides_proximos
    }
    
    return payload

game_data = build_game_json(solar_events, asteroids, risco)

print("\n=== JSON GERADO ===")
print(json.dumps(game_data, indent=2, ensure_ascii=False))

# ============================================================
# CÉLULA 7 — Salvar e baixar o arquivo
# ============================================================

with open('nasa_data.json', 'w', encoding='utf-8') as f:
    json.dump(game_data, f, indent=2, ensure_ascii=False)

print("Arquivo nasa_data.json salvo com sucesso!")
print("\nPróximo passo:")
print("1. No painel esquerdo do Colab, clique no ícone de pasta")
print("2. Encontre o arquivo 'nasa_data.json'")
print("3. Clique com botão direito → Fazer download")
print("4. Arraste o arquivo baixado para a pasta do seu repositório no GitHub")

# Download automático no Colab
try:
    from google.colab import files
    files.download('nasa_data.json')
    print("\nDownload iniciado automaticamente!")
except:
    print("\n(Execute no Google Colab para download automático)")

