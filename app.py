import os
import json
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError, ClientError

load_dotenv()

st.set_page_config(
    page_title="PrintTok Market Radar v6.2",
    page_icon="🎯",
    layout="wide"
)

DB_FILE = "catalogo_market_radar.json"

def carregar_catalogo():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_no_catalogo(item):
    catalogo = carregar_catalogo()
    catalogo.append(item)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=4)

def limpar_catalogo():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

# --- BARRA LATERAL ---
st.sidebar.title("⚙️ PrintTok Radar v6.2")
api_key_env = os.getenv("GEMINI_API_KEY", "")
api_key_input = st.sidebar.text_input(
    "Gemini API Key", 
    value=api_key_env, 
    type="password",
    help="Cole sua chave do Google AI Studio"
)

ai_client = None
if api_key_input:
    try:
        ai_client = genai.Client(api_key=api_key_input)
        st.sidebar.success("🎯 Radar IA Ativo!")
    except Exception as e:
        st.sidebar.error(f"Erro na chave: {e}")
else:
    st.sidebar.warning("Insira sua Gemini API Key.")

st.sidebar.markdown("---")
st.sidebar.subheader("🖨️ Parâmetros da Oficina & SLA")
modelo_impressora = st.sidebar.text_input("Impressora:", value="Creality Ender-3 V3 KE")
tamanho_mesa = st.sidebar.number_input("Tamanho da Mesa (mm)", value=220, step=10)
horas_dia_trabalho = st.sidebar.slider("Horas de operação/dia da máquina:", 4, 24, 18)
meta_lucro = st.sidebar.number_input("Meta de Lucro Líquido (R$):", value=4000.0, step=500.0)
sla_limite_horas = st.sidebar.selectbox("SLA Limite de Envio do TikTok:", [24, 48, 72], index=1)

# --- TÍTULO ---
st.title("🎯 PrintTok Market Radar & Content Factory — v6.2")
st.caption("Ecossistema Completo com Proteção Anti-Queda de Servidor (503), Radar Brasil e Fábrica de Vídeos.")

tab_radar, tab_fabrica, tab_calc, tab_expedicao, tab_mesa, tab_cat, tab_seo, tab_ai_video = st.tabs([
    "🎯 Radar de Demanda & Nichos",
    "🎬 Fábrica de Lote de Vídeos",
    "🧮 Precificação, Kits & SLA",
    "📦 Expedição & Pós-Processamento",
    "📐 Otimizador de Mesa",
    "📦 Meu Catálogo & CSV",
    "🏷️ SEO & Anúncio TikTok",
    "🤖 Prompts IA de Vídeo"
])

# ==============================================================================
# ABA 1: RADAR DE DEMANDA & NICHOS
# ==============================================================================
with tab_radar:
    st.subheader("🎯 Radar Inteligente de Demanda para o TikTok Shop Brasil")
    st.caption("Selecione um nicho estratégico para a IA analisar o comportamento do consumidor brasileiro, volume de busca e validar o potencial de viralização.")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        nicho_radar = st.selectbox(
            "Escolha o Nicho de Mercado:",
            [
                "Fidget Toys Sensoriais & Clickers ASMR (Giro Rápido)",
                "Organização de Setup, Suportes de Headset & Cabos (Dor Real)",
                "Decoração Geek, Suportes de Controle & Luminárias Compactas",
                "Utilidades Domésticas Criativas & Organizadores de Cozinha",
                "Chaveiros Personalizados em Lote (Volume Extremo)"
            ]
        )
    with col_r2:
        publico_alvo = st.selectbox(
            "Público-Alvo Principal:",
            ["Gamer / Jovem Adulto (15-28 anos)", "Profissionais em Home Office / Escritório", "Entusiastas de Decoração Minimalista", "Público Infantil / Pais"]
        )

    if st.button("🔍 Analisar Demanda, Tendência e Produtos Campeões", use_container_width=True):
        if not ai_client:
            st.warning("Insira sua API Key na barra lateral.")
        else:
            with st.spinner("Analisando tendências do e-commerce e comportamento de consumo no Brasil..."):
                try:
                    prompt = f"""
                    Você é o analista de dados e estrategista chefe de e-commerce no TikTok Shop Brasil para impressão 3D.
                    Analise o nicho: '{nicho_radar}' voltado para o público '{publico_alvo}' fabricado na impressora '{modelo_impressora}'.

                    Entregue um relatório estratégico estruturado contendo:
                    1. **Temperatura da Demanda no Brasil:** O volume de buscas atual e por que esse nicho converte bem por impulso no feed do TikTok.
                    2. **Top 3 Produtos Campeões para Lançamento:** Nome da peça, tempo estimado de impressão na Ender-3 V3 KE e por que ela se destaca visualmente nos primeiros 3 segundos.
                    3. **Estratégia de Kit Ideal:** Como empacotar (ex: kit com 2 ou 3) para diluir a taxa fixa e gerar lucro real.
                    4. **Gatilho Psicológico de Vendas:** Qual o principal apelo emocional ou visual a ser usado nos vídeos para fazer o cliente clicar no carrinho laranja.
                    """
                    res = ai_client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
                    st.markdown(res.text)
                except ServerError:
                    st.error("⚠️ **Servidores do Google em alta demanda (Erro 503).** O sistema está temporariamente congestionado. Aguarde 10 segundos e clique no botão novamente!")
                except ClientError as ce:
                    st.error(f"Erro de Cliente/API: {ce}")
                except Exception as e:
                    st.error(f"Ocorreu um erro inesperado: {e}")

# ==============================================================================
# ABA 2: FÁBRICA DE 5 ROTEIROS DIÁRIOS
# ==============================================================================
with tab_fabrica:
    st.subheader("🎬 Fábrica de Conteúdo & Planeamento de Gravação em Lote")
    
    catalogo_atual = carregar_catalogo()
    nomes_produtos = [item["Produto"] for item in catalogo_atual] if catalogo_atual else ["Chaveiro Fidget Clicker", "Suporte Celular Minimalista", "Expositor de Óculos", "Luminária Órbita 3D"]

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        produto_escolhido = st.selectbox("Selecione a Peça Alvo de Hoje:", nomes_produtos)
        nicho_fabrica = st.selectbox("Estratégia de Abordagem:", [
            "Foco em Giro Rápido / Compras por Impulso",
            "Foco em Utilitário / Resolução de Problema (Setup)",
            "Foco em Decoração de Alto Valor Percebido",
            "Foco em ASMR Puro e Satisfação Visual"
        ])
    with col_f2:
        oferta_fabrica = st.text_input("Oferta / Condição no Carrinho:", value="Kit com 3 unidades + Frete Grátis no Carrinho Laranja")
        tom_voz = st.selectbox("Tom do Vídeo:", ["Divertido e Dinâmico", "Profissional e Direto", "Hype / Curiosidade Máxima"])

    if st.button("🚀 Gerar Lote de 5 Roteiros Virais Simultâneos", use_container_width=True):
        if not ai_client:
            st.warning("Insira sua API Key na barra lateral.")
        else:
            with st.spinner(f"Criando 5 estratégias de vídeo distintas para '{produto_escolhido}'..."):
                try:
                    prompt = f"""
                    Você é o diretor de marketing especialista em TikTok Shop para manufatura aditiva 3D.
                    Crie exatamente **5 ROTEIROS DE VÍDEOS CURTOS (15 a 25 segundos cada)** para vender o produto: '{produto_escolhido}'.
                    Estratégia: {nicho_fabrica}. Oferta: {oferta_fabrica}. Tom: {tom_voz}.

                    Os 5 vídeos devem ter ângulos psicológicos COMPLETAMENTE DIFERENTES:
                    - **Vídeo 1:** Focado em ASMR e satisfação visual pura (descolando da mesa PEI).
                    - **Vídeo 2:** Focado em Problema vs Solução (dor do dia a dia resolvida pela peça).
                    - **Vídeo 3:** Focado em Bastidores de Fábrica / Produção em Lote (mesa cheia imprimindo).
                    - **Vídeo 4:** Focado em Teste de Resistência do Material (durabilidade).
                    - **Vídeo 5:** Focado em Escassez e Urgência para clicar no Carrinho Laranja.

                    Estruture claramente cada vídeo com Título, Gancho (0-3s), Desenvolvimento, CTA e Legenda com hashtags otimizadas.
                    """
                    res = ai_client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
                    st.markdown(res.text)
                except ServerError:
                    st.error("⚠️ **Servidores do Google em alta demanda (Erro 503).** Aguarde alguns segundos e tente novamente.")
                except Exception as e:
                    st.error(f"Erro ao gerar roteiros: {e}")
                
    st.markdown("---")
    st.markdown("#### 📅 Guia de Organização: Bloco de Gravação de 1 Hora (Batch Recording)")
    st.info("""
    **Como eliminar o trabalho diário de gravação:**
    1. **Domingo (1 hora):** Grave os 5 roteiros seguidos mudando apenas o ângulo ou a blusa.
    2. **Segunda a Sexta:** Publique 1 vídeo por dia no TikTok Shop e responda aos clientes.
    3. **Resultado:** Consistência total no algoritmo sem estresse diário.
    """)

# ==============================================================================
# ABA 3: PRECIFICAÇÃO, KITS & ALERTA DE SLA
# ==============================================================================
with tab_calc:
    st.subheader("Simulador de Custos, Kits e Proteção contra Estouro de SLA")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("##### 🧵 Matéria-Prima & Peça")
        nome_prod = st.text_input("Nome do Produto para Salvar:", value="Chaveiro Fidget / Suporte")
        preco_kg = st.number_input("Preço do kg do Filamento (R$)", value=95.0, step=5.0)
        peso_g = st.number_input("Peso de 1 unidade (g)", value=15.0, step=1.0)
        tempo_min = st.number_input("Tempo de impressão (min)", value=22, step=1)
        custo_ferragem = st.number_input("Ferragem/Acessório un. (R$)", value=0.50, step=0.10)
        
    with c2:
        st.markdown("##### ⚡ Energia & Estrutura")
        potencia_w = st.number_input("Potência da Impressora (W)", value=150, step=10)
        tarifa_kwh = st.number_input("Tarifa de Energia (R$/kWh)", value=0.95, step=0.05)
        custo_deprec = st.number_input("Manutenção/Bico por hora (R$)", value=0.60, step=0.10)
        custo_emb = st.number_input("Embalagem por Pedido (R$)", value=1.50, step=0.25)
        taxa_perda = st.slider("Margem de Segurança / Falha (%)", 0, 15, 5)
        
    with c3:
        st.markdown("##### 🛒 Taxas & Demanda Esperada")
        preco_venda = st.number_input("Preço de Venda (1 un.) (R$)", value=24.90, step=1.0)
        comissao_tiktok = st.number_input("Comissão TikTok Shop (%)", value=10.0, step=0.5)
        comissao_afiliado = st.number_input("Comissão de Afiliados (%)", value=12.0, step=1.0)
        taxa_fixa = st.number_input("Taxa Fixa por Pedido (R$)", value=3.00, step=0.50)
        pedidos_dia_estimados = st.number_input("Média de Pedidos Esperados por Dia:", value=15, min_value=1, step=1)

    filamento_un = (preco_kg / 1000.0) * peso_g
    horas_un = tempo_min / 60.0
    energia_un = (potencia_w / 1000.0) * horas_un * tarifa_kwh
    maquina_un = horas_un * custo_deprec
    
    custo_fab_puro = filamento_un + energia_un + maquina_un + custo_ferragem
    custo_fab_un = custo_fab_puro * (1 + (taxa_perda / 100.0))
    comissoes_totais = (comissao_tiktok + comissao_afiliado) / 100.0
    
    custo_pedido_1 = custo_fab_un + custo_emb
    taxas_tt_1 = (preco_venda * comissoes_totais) + taxa_fixa
    lucro_1 = preco_venda - custo_pedido_1 - taxas_tt_1
    margem_1 = (lucro_1 / preco_venda) * 100 if preco_venda > 0 else 0

    horas_necessarias_dia = (pedidos_dia_estimados * tempo_min) / 60.0
    capacidade_max_maquina_dia = horas_dia_trabalho

    st.markdown("---")
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Custo de Fabricação (Un.)", f"R$ {custo_fab_un:.2f}")
    res2.metric("Taxas + Afiliados (1 un.)", f"R$ {taxas_tt_1:.2f}")
    res3.metric("Lucro Líquido (1 un.)", f"R$ {lucro_1:.2f}", delta=f"{margem_1:.1f}%")
    res4.metric("Demanda vs Capacidade", f"{horas_necessarias_dia:.1f}h / {capacidade_max_maquina_dia}h")

    if horas_necessarias_dia > capacidade_max_maquina_dia:
        st.error(f"🚨 **ALERTA CRÍTICO DE SLA:** Com {pedidos_dia_estimados} pedidos/dia, você precisa de {horas_necessarias_dia:.1f}h de impressão, mas sua máquina só opera {capacidade_max_maquina_dia}h! **Você vai estourar o prazo de envio de {sla_limite_horas}h.**")
    else:
        st.success(f"✅ **Operação Segura:** Demanda dentro da capacidade operacional para o SLA de {sla_limite_horas}h.")

    if st.button("💾 Guardar Produto no Catálogo Master", use_container_width=True):
        registro = {
            "Produto": nome_prod,
            "Peso (g)": peso_g,
            "Tempo (min)": tempo_min,
            "Custo Fab (R$)": round(custo_fab_un, 2),
            "Preço Venda (R$)": preco_venda,
            "Lucro Un. (R$)": round(lucro_1, 2),
            "Margem (%)": round(margem_1, 1)
        }
        salvar_no_catalogo(registro)
        st.success(f"✅ '{nome_prod}' guardado com sucesso!")

    st.markdown("#### 📊 Tabela de Alavancagem de Kits")
    tabela_kits = []
    for qtd, desc in [(1, 0.0), (2, 0.10), (3, 0.15), (5, 0.20)]:
        preco_k = (preco_venda * qtd) * (1 - desc)
        custo_k = (custo_fab_un * qtd) + custo_emb
        taxas_k = (preco_k * comissoes_totais) + taxa_fixa
        lucro_k = preco_k - custo_k - taxas_k
        margem_k = (lucro_k / preco_k) * 100 if preco_k > 0 else 0
        pedidos_meta = int(meta_lucro / lucro_k) if lucro_k > 0 else 9999
        
        tabela_kits.append({
            "Formato": f"Kit com {qtd} un." if qtd > 1 else "1 Unidade Avulsa",
            "Desconto": f"{int(desc*100)}%",
            "Preço do Kit": f"R$ {preco_k:.2f}",
            "Custo Produção": f"R$ {custo_k:.2f}",
            "Taxas + Afiliados": f"R$ {taxas_k:.2f}",
            "Lucro Líquido": f"R$ {lucro_k:.2f}",
            "Margem Real": f"{margem_k:.1f}%",
            "Pedidos p/ Meta": f"{pedidos_meta} pacotes"
        })
    st.dataframe(pd.DataFrame(tabela_kits), use_container_width=True, hide_index=True)

# ==============================================================================
# ABA 4: EXPEDIÇÃO E LOGÍSTICA
# ==============================================================================
with tab_expedicao:
    st.subheader("📦 Calculadora de Tempo de Pós-Processamento e Logística")
    e1, e2, e3 = st.columns(3)
    with e1:
        tempo_retirada_min = st.number_input("Tempo para descolar e limpar peças por lote (min):", value=3.0, step=1.0)
        tempo_montagem_min = st.number_input("Tempo para colocar ferragens/argolas por un. (min):", value=1.0, step=0.5)
    with e2:
        tempo_embalagem_min = st.number_input("Tempo para montar caixinha e embalar (min):", value=2.0, step=0.5)
        tempo_nf_etiqueta = st.number_input("Tempo para emitir NF/GTIN e colar etiqueta (min):", value=2.0, step=0.5)
    with e3:
        salario_hora_desejado = st.number_input("Quanto vale 1 hora do seu trabalho (R$):", value=30.0, step=5.0)

    minutos_totais_pos = tempo_retirada_min + tempo_montagem_min + tempo_embalagem_min + tempo_nf_etiqueta
    custo_mao_obra_pedido = (minutos_totais_pos / 60.0) * salario_hora_desejado

    st.markdown("---")
    em1, em2 = st.columns(2)
    em1.metric("Tempo Total Gasto no Pós-Venda", f"{minutos_totais_pos:.1f} minutos por pedido")
    em2.metric("Custo Oculto de Mão de Obra", f"R$ {custo_mao_obra_pedido:.2f}")

# ==============================================================================
# ABA 5: OTIMIZADOR DE MESA 3D
# ==============================================================================
with tab_mesa:
    st.subheader("📐 Otimizador de Lote e Espaço de Impressão")
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        largura_peca = st.number_input("Largura da peça (mm):", value=40.0, step=5.0)
    with mc2:
        profundidade_peca = st.number_input("Profundidade da peça (mm):", value=40.0, step=5.0)
    with mc3:
        espacamento_borda = st.number_input("Espaço entre peças / Borda (mm):", value=5.0, step=1.0)
        
    espaco_x = largura_peca + espacamento_borda
    espaco_y = profundidade_peca + espacamento_borda
    
    if espaco_x > 0 and espaco_y > 0:
        qtd_x = int((tamanho_mesa - 10) / espaco_x)
        qtd_y = int((tamanho_mesa - 10) / espaco_y)
        total_pecas_mesa = qtd_x * qtd_y
        
        st.markdown("---")
        mm1, mm2, mm3 = st.columns(3)
        mm1.metric("Peças por Eixo X", f"{qtd_x} un.")
        mm2.metric("Peças por Eixo Y", f"{qtd_y} un.")
        mm3.metric("Capacidade Máxima por Mesa", f"{total_pecas_mesa} unidades", delta="Lote ideal")
        st.success(f"✅ Programe lotes de {total_pecas_mesa} unidades no fatiador.")

# ==============================================================================
# ABA 6: CATÁLOGO & EXPORTAÇÃO CSV
# ==============================================================================
with tab_cat:
    st.subheader("📦 Gestão de Catálogo e Exportação de Dados")
    catalogo = carregar_catalogo()
    
    if len(catalogo) == 0:
        st.info("Nenhum produto guardado ainda.")
    else:
        df_master = pd.DataFrame(catalogo)
        st.dataframe(df_master, use_container_width=True, hide_index=True)
        
        csv_data = df_master.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Catálogo em Planilha (CSV)",
            data=csv_data,
            file_name="catalogo_lunella_3d.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        if st.button("🗑️ Apagar Todo o Catálogo"):
            limpar_catalogo()
            st.rerun()

# ==============================================================================
# ABA 7: SEO & ANÚNCIO TIKTOK SHOP
# ==============================================================================
with tab_seo:
    st.subheader("🏷️ Gerador de Títulos, Tags e Descrição Otimizada (SEO TikTok)")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        produto_seo = st.text_input("Nome/Tipo do Produto:", value="Expositor de Óculos / Fidget Toy")
        material_seo = st.text_input("Material e Acabamento:", value="PETG Premium Ultra Resistente")
    with s_col2:
        beneficio_seo = st.text_input("Principal Diferencial:", value="Design moderno, não quebra, encaixe perfeito")

    if st.button("✨ Gerar SEO Completo para o TikTok Shop", use_container_width=True):
        if not ai_client:
            st.warning("Insira sua API Key na barra lateral.")
        else:
            with st.spinner("Gerando otimização algorítmica..."):
                try:
                    prompt = f"Crie otimização de SEO para o produto 3D '{produto_seo}' feito em '{material_seo}', diferencial '{beneficio_seo}'. Inclua 5 títulos virais focados em busca, bullet points para a descrição e ideias de fotos de capa para o TikTok Shop."
                    res = ai_client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
                    st.markdown(res.text)
                except ServerError:
                    st.error("⚠️ **Servidores do Google em alta demanda (Erro 503).** Tente novamente em instantes.")
                except Exception as e:
                    st.error(f"Erro: {e}")

# ==============================================================================
# ABA 8: PROMPTS IA DE VÍDEO
# ==============================================================================
with tab_ai_video:
    st.subheader("🤖 Gerador de Prompts para IAs (Kling, Runway, Luma)")
    prompt_base = st.text_area("Cena desejada:", value="Suporte de óculos minimalista impresso em 3D sobre mesa de madeira escura.")
    if st.button("🎥 Gerar Prompts Cinematográficos", use_container_width=True):
        if not ai_client:
            st.warning("Insira sua API Key na barra lateral.")
        else:
            with st.spinner("Gerando descrições visuais..."):
                try:
                    prompt = f"Crie prompts detalhados em inglês para IAs de vídeo (Kling/Luma) com base em: '{prompt_base}'. Inclua close macro nas camadas de impressão 3D."
                    res = ai_client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
                    st.markdown(res.text)
                except ServerError:
                    st.error("⚠️ **Servidores do Google em alta demanda (Erro 503).** Tente novamente em instantes.")
                except Exception as e:
                    st.error(f"Erro: {e}")