import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import uuid
import sys
import asyncio
sys.path.append("server")
from ai_feedback import generate_trade_feedback

# Configuration de la page Streamlit (doit être le premier appel Streamlit)
st.set_page_config(
    page_title="TradeMind AI Journal",
    page_icon="📈",
    layout="wide"
)

# Charger les variables d'environnement
load_dotenv()

# Configuration de Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Titre de l'application
st.title("📈 TradeMind AI Journal")
st.markdown("---")

def upload_screenshot(file):
    """Upload un screenshot vers Supabase Storage"""
    try:
        # Générer un nom de fichier unique
        file_extension = file.name.split(".")[-1]
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4()}.{file_extension}"
        
        # Lire le contenu du fichier
        file_bytes = file.read()
        
        # Upload vers le bucket 'screenshots'
        supabase.storage.from_("screenshots").upload(
            path=file_name,
            file=file_bytes,
            file_options={"content-type": file.type}
        )
        
        # Générer l'URL publique
        file_url = supabase.storage.from_("screenshots").get_public_url(file_name)
        return file_url
    except Exception as e:
        st.error(f"Erreur lors de l'upload du screenshot: {str(e)}")
        return None

def calculate_rr(row):
    """Calculer le ratio risk/reward pour un trade"""
    try:
        if row["direction"] == "LONG":
            risk = abs(row["entry_price"] - row["stop_loss"])
            reward = abs(row["take_profit"] - row["entry_price"])
        else:  # SHORT
            risk = abs(row["entry_price"] - row["stop_loss"])
            reward = abs(row["entry_price"] - row["take_profit"])
        
        return reward / risk if risk != 0 else 0
    except:
        return 0

def load_trades():
    """Charger les trades depuis Supabase"""
    try:
        response = supabase.table("trades").select("*").order("created_at", desc=True).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            # Calculer le R:R pour chaque trade
            df["risk_reward"] = df.apply(calculate_rr, axis=1)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors du chargement des trades: {str(e)}")
        return pd.DataFrame()

def update_trade_screenshot(trade_id, screenshot_url):
    """Mettre à jour l'URL du screenshot pour un trade"""
    try:
        supabase.table("trades").update({"screenshot_url": screenshot_url}).eq("id", trade_id).execute()
        return True
    except Exception as e:
        st.error(f"Erreur lors de la mise à jour du trade: {str(e)}")
        return False

def update_trade_notes(trade_id, notes):
    """Mettre à jour les notes pour un trade"""
    try:
        supabase.table("trades").update({"notes": notes}).eq("id", trade_id).execute()
        return True
    except Exception as e:
        st.error(f"Erreur lors de la mise à jour des notes: {str(e)}")
        return False

def get_ai_feedback(trade_data):
    """Obtenir le feedback IA pour un trade"""
    try:
        feedback = generate_trade_feedback(trade_data)
        return feedback
    except Exception as e:
        st.error(f"Erreur lors de la génération du feedback IA: {str(e)}")
        return None

def calculate_win_rate(df):
    """Calculer le win rate basé sur le R:R (temporaire en attendant les résultats réels)"""
    if df.empty:
        return 0
    # Pour l'instant, on considère un trade gagnant si R:R >= 1
    winning_trades = df[df["risk_reward"] >= 1]
    return len(winning_trades) / len(df) * 100

def get_trend_icon(current, target):
    """Retourner l'icône de tendance appropriée"""
    if current >= target:
        return "↗️"
    return "↘️"

def get_rr_color(rr):
    """Retourner la couleur en fonction du R:R"""
    if rr >= 2.0:
        return "green"
    elif rr >= 1.0:
        return "orange"
    return "red"

# Section Sélection du Trade
st.sidebar.header("🎯 Sélection du Trade")

# Charger les trades pour la sélection
trades_df = load_trades()
if not trades_df.empty:
    # Créer une liste de trades pour la sélection
    trade_options = trades_df.apply(
        lambda x: pd.to_datetime(x['created_at']).strftime('%d/%m/%Y %H:%M'),
        axis=1
    ).tolist()
    trade_ids = trades_df['id'].tolist()
    
    # Sélection du trade
    selected_trade_index = st.sidebar.selectbox(
        "Sélectionner une date",
        range(len(trade_options)),
        format_func=lambda x: trade_options[x]
    )
    selected_trade_id = trade_ids[selected_trade_index]
    
    # Afficher les détails du trade sélectionné
    selected_trade = trades_df.loc[trades_df['id'] == selected_trade_id].iloc[0]
    st.sidebar.markdown(f"""
    **Trade sélectionné :**
    - Instrument : {selected_trade['instrument']}
    - Direction : {selected_trade['direction']}
    - Prix d'entrée : {selected_trade['entry_price']}
    """)
    
    # Section Screenshot
    st.sidebar.markdown("---")
    st.sidebar.header("📸 Screenshot du Trade")
    uploaded_file = st.sidebar.file_uploader("Ajouter une capture d'écran", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Afficher l'aperçu
        st.sidebar.image(uploaded_file, caption="Aperçu", use_column_width=True)
        
        # Bouton pour sauvegarder
        if st.sidebar.button("💾 Sauvegarder le screenshot"):
            with st.spinner("Upload en cours..."):
                screenshot_url = upload_screenshot(uploaded_file)
                if screenshot_url:
                    # Mettre à jour le trade avec l'URL du screenshot
                    if update_trade_screenshot(selected_trade_id, screenshot_url):
                        st.sidebar.success("Screenshot sauvegardé !")
                        # Recharger les trades pour afficher les changements
                        trades_df = load_trades()
                    else:
                        st.sidebar.error("Erreur lors de la sauvegarde")
                else:
                    st.sidebar.error("Erreur lors de l'upload")
    
    # Section Notes
    st.sidebar.markdown("---")
    st.sidebar.header("📝 Notes du Trade")
    current_notes = trades_df.loc[trades_df['id'] == selected_trade_id, 'notes'].iloc[0]
    new_notes = st.sidebar.text_area(
        "Ajouter/modifier les notes",
        value=current_notes if pd.notna(current_notes) else "",
        height=150,
        placeholder="Écrivez vos notes ici..."
    )
    
    if st.sidebar.button("💾 Sauvegarder les notes"):
        if update_trade_notes(selected_trade_id, new_notes):
            st.sidebar.success("Notes sauvegardées !")
            trades_df = load_trades()
        else:
            st.sidebar.error("Erreur lors de la sauvegarde")
    
    # Section Analyse IA
    st.sidebar.markdown("---")
    st.sidebar.header("🤖 Analyse IA")
    
    def handle_analyze_button():
        progress_placeholder = st.sidebar.empty()
        progress_placeholder.info("Analyse en cours...")
        trade_data = {
            "instrument": selected_trade["instrument"],
            "direction": selected_trade["direction"],
            "entry_price": selected_trade["entry_price"],
            "stop_loss": selected_trade["stop_loss"],
            "take_profit": selected_trade["take_profit"],
            "risk_reward": selected_trade["risk_reward"],
            "notes": selected_trade["notes"] if pd.notna(selected_trade["notes"]) else ""
        }
        try:
            feedback = get_ai_feedback(trade_data)
            progress_placeholder.empty()
            if feedback:
                # Mettre à jour le trade avec le feedback
                try:
                    supabase.table("trades").update({"ai_feedback": feedback}).eq("id", selected_trade_id).execute()
                    trades_df = load_trades()
                    st.sidebar.success("✅ Analyse IA générée avec succès !")
                except Exception as e:
                    st.sidebar.error(f"Erreur lors de la sauvegarde du feedback: {str(e)}")
        except Exception as e:
            progress_placeholder.error(f"Erreur lors de l'analyse: {str(e)}")

    if st.sidebar.button("📊 Analyser ce trade"):
        handle_analyze_button()

else:
    st.sidebar.info("Aucun trade disponible pour le moment.")

# Charger les trades
trades_df = load_trades()

if not trades_df.empty:
    # Afficher les statistiques générales
    st.subheader("📊 Statistiques Générales")
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcul des statistiques
    total_trades = len(trades_df)
    longs = trades_df[trades_df["direction"] == "LONG"]
    shorts = trades_df[trades_df["direction"] == "SHORT"]
    long_ratio = len(longs) / total_trades * 100 if total_trades > 0 else 0
    avg_rr = trades_df["risk_reward"].mean()
    trades_today = len(trades_df[pd.to_datetime(trades_df["created_at"]).dt.date == pd.Timestamp.now().date()])
    win_rate = calculate_win_rate(trades_df)
    trend_icon = get_trend_icon(avg_rr, 2.0)
    
    # Style CSS pour les statistiques
    st.markdown("""
    <style>
    .stat-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.25rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .stat-title {
        font-size: 0.9em;
        color: rgba(128, 128, 128, 0.8);
        margin-bottom: 0.5rem;
    }
    .stat-value {
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .stat-delta {
        font-size: 0.9em;
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">📈 Nombre de trades</div>
            <div class="stat-value">{total_trades}</div>
            <div class="stat-delta">Aujourd'hui: {trades_today}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">⚖️ Long/Short</div>
            <div class="stat-value">{long_ratio:.1f}% / {100-long_ratio:.1f}%</div>
            <div class="stat-delta">{"Long dominant" if long_ratio > 50 else "Short dominant"}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">📏 R:R Moyen</div>
            <div class="stat-value">{avg_rr:.2f} {trend_icon}</div>
            <div class="stat-delta">Objectif: 2.0</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">🎯 Win Rate</div>
            <div class="stat-value">{win_rate:.1f}%</div>
            <div class="stat-delta">Basé sur R:R ≥ 1</div>
        </div>
        """, unsafe_allow_html=True)

    # Filtres
    st.subheader("🔍 Filtres")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # Filtre par date
        date_range = st.date_input(
            "Période",
            value=(
                pd.to_datetime(trades_df["created_at"]).min().date(),
                pd.to_datetime(trades_df["created_at"]).max().date()
            ) if not trades_df.empty else (datetime.now().date(), datetime.now().date()),
            key="date_filter"
        )

    with col2:
        # Filtre par instrument
        instruments = ["Tous"] + sorted(trades_df["instrument"].unique().tolist())
        selected_instrument = st.selectbox("Instrument", instruments)

    with col3:
        # Filtre par direction
        directions = ["Tous", "LONG", "SHORT"]
        selected_direction = st.selectbox("Direction", directions)

    with col4:
        # Filtre par performance
        performances = ["Tous", "Gagnants (R:R ≥ 1)", "Perdants (R:R < 1)"]
        selected_performance = st.selectbox("Performance", performances)

    with col5:
        # Recherche par mots-clés
        search_query = st.text_input("Rechercher dans les notes", placeholder="Mots-clés...")

    # Bouton pour réinitialiser les filtres
    if st.button("🔄 Réinitialiser les filtres"):
        st.session_state.date_filter = (
            pd.to_datetime(trades_df["created_at"]).min().date(),
            pd.to_datetime(trades_df["created_at"]).max().date()
        )
        selected_instrument = "Tous"
        selected_direction = "Tous"
        selected_performance = "Tous"
        search_query = ""

    # Appliquer les filtres
    filtered_df = trades_df.copy()

    # Filtre par date
    filtered_df = filtered_df[
        (pd.to_datetime(filtered_df["created_at"]).dt.date >= date_range[0]) &
        (pd.to_datetime(filtered_df["created_at"]).dt.date <= date_range[1])
    ]

    # Filtre par instrument
    if selected_instrument != "Tous":
        filtered_df = filtered_df[filtered_df["instrument"] == selected_instrument]

    # Filtre par direction
    if selected_direction != "Tous":
        filtered_df = filtered_df[filtered_df["direction"] == selected_direction]

    # Filtre par performance
    if selected_performance == "Gagnants (R:R ≥ 1)":
        filtered_df = filtered_df[filtered_df["risk_reward"] >= 1]
    elif selected_performance == "Perdants (R:R < 1)":
        filtered_df = filtered_df[filtered_df["risk_reward"] < 1]

    # Filtre par mots-clés
    if search_query:
        filtered_df = filtered_df[
            filtered_df["notes"].fillna("").str.contains(search_query, case=False) |
            filtered_df["ai_feedback"].fillna("").str.contains(search_query, case=False)
        ]

    # Afficher les trades filtrés
    st.subheader("📝 Journal de Trading")

    if not filtered_df.empty:
        for _, trade in filtered_df.iterrows():
            # Définir la couleur du R:R
            rr_color = get_rr_color(trade["risk_reward"])
            
            # Préparer les badges
            badges = []
            if pd.notna(trade["ai_feedback"]) and trade["ai_feedback"].strip():
                badges.append("🤖")
            if trade["risk_reward"] >= 1:
                badges.append("✨")
            
            # Créer le titre de l'expandeur avec les badges
            expander_title = (
                f"🔸 {pd.to_datetime(trade['created_at']).strftime('%d/%m/%Y %H:%M')} - "
                f"{trade['instrument']} ({trade['direction']}) - "
                f"R:R: :{rr_color}[{trade['risk_reward']:.2f}] "
                f"{' '.join(badges)}"
            )
            
            with st.expander(expander_title):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 📊 Détails du Trade")
                    st.markdown(f"""
                    - **Instrument:** {trade['instrument']}
                    - **Direction:** {trade['direction']}
                    - **Prix d'entrée:** {trade['entry_price']}
                    - **Stop Loss:** {trade['stop_loss']}
                    - **Take Profit:** {trade['take_profit']}
                    - **Ratio R:R:** :{rr_color}[{trade['risk_reward']:.2f}]
                    """)
                    
                    if pd.notna(trade['notes']) and trade['notes'].strip():
                        st.markdown("### 📝 Notes personnelles")
                        st.markdown(trade['notes'])
                    
                    if pd.notna(trade['ai_feedback']) and trade['ai_feedback'].strip():
                        st.markdown("### 🤖 Feedback IA")
                        st.markdown(trade['ai_feedback'])
                
                with col2:
                    if pd.notna(trade['screenshot_url']) and trade['screenshot_url'].strip():
                        st.markdown("### 📸 Screenshot")
                        st.image(trade['screenshot_url'], use_column_width=True)
    else:
        st.info("Aucun trade ne correspond aux filtres sélectionnés.")

else:
    st.info("Aucun trade enregistré pour le moment.") 