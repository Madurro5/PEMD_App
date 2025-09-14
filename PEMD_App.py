import streamlit as st
import pandas as pd
from io import StringIO

# Liste des matériaux avec leurs densités
from materials import MATERIALS


st.set_page_config(page_title="Diagnostic PEMD", page_icon="🧱", layout="centered")

# --- Initialisation de l'état
if "estimates" not in st.session_state:
    st.session_state.estimates = []

st.title("📊 Diagnostic PEMD")
st.markdown(
    "Estimation des masses des matériaux pour vos diagnostics "
    "_Produits, Équipements, Matériaux et Déchets_."
)

# --- Choix du mode de saisie hors formulaire pour mise à jour dynamique
input_type = st.radio("Mode de saisie", ["Volume direct", "Dimensions", "Surface", "Unitaire"], horizontal=True)

# --- Formulaire
st.header("➕ Ajouter un matériau")

with st.form("material_form"):
    material_name = st.selectbox(
        "Type de matériau",
        options=[m["name"] for m in MATERIALS],
    )

    if input_type == "Volume direct":
        volume_direct = st.number_input("Volume (m³)", min_value=0.0, step=0.1, format="%.3f")
        multiple = st.number_input("Facteur (x)", min_value=1.0, step=1.0)
        volume_direct *= multiple
        length = width = height = None

    if input_type == "Dimensions":
        col1, col2, col3 = st.columns(3)
        with col1:
            length = st.number_input("Longueur (m)", min_value=0.0, step=0.1)
        with col2:
            width = st.number_input("Largeur (m)", min_value=0.0, step=0.1)
        with col3:
            height = st.number_input("Hauteur (m)", min_value=0.0, step=0.1)

        multiple = st.number_input("Facteur (x)", min_value=1.0, step=1.0)
        volume_direct = length * width * height * multiple

    if input_type == "Surface":
        surface = st.number_input("Surface (m²)", min_value=0.0, step=0.1)
        thickness = st.number_input("Épaisseur (m)", min_value=0.03, step=0.01)
        multiple = st.number_input("Facteur (x)", min_value=1.0, step=1.0)
        volume_direct = surface * thickness * multiple
        length = width = height = None
    if input_type == "Unitaire":
        multiple = st.number_input("Facteur (x)", min_value=1.0, step=1.0)
        unit_volume = st.number_input("Volume par unité (m³)", min_value=0.0, step=0.001)
        volume_direct = multiple * unit_volume
        length = width = height = None
    
    submitted = st.form_submit_button("Ajouter au tableau")

    if submitted:
        material = next((m for m in MATERIALS if m["name"] == material_name), None)
        if material and volume_direct > 0:
            mass = volume_direct * material["density"]
            estimate = {
                "material_type": material_name,
                "density": material["density"],
                "volume_input_type": "direct" if input_type == "Volume direct" else "dimensions",
                "volume_direct": volume_direct if input_type == "Volume direct" else None,
                "length": length if input_type == "Dimensions" else None,
                "width": width if input_type == "Dimensions" else None,
                "height": height if input_type == "Dimensions" else None,
                "unit_count": multiple,
                "calculated_volume": volume_direct,
                "calculated_mass": mass,
            }
            st.session_state.estimates.append(estimate)
            st.success(f"{material_name} ajouté avec succès ✅")

# --- Tableau récapitulatif
st.header("📋 Récapitulatif PEMD")

estimates = st.session_state.estimates

if not estimates:
    st.info("Aucun matériau ajouté. Utilisez le formulaire ci-dessus pour commencer.")
else:
    df = pd.DataFrame(estimates)
    df_display = df[["material_type", "unit_count", "calculated_volume", "calculated_mass", "density"]].rename(
        columns={
            "material_type": "Matériau",
            "unit_count": "Facteur",
            "calculated_volume": "Volume (m³)",
            "calculated_mass": "Masse (kg)",
            "density": "Masse volumique (kg/m³)",
        }
    )
    st.dataframe(df_display, use_container_width=True)

    total_volume = sum(est["calculated_volume"] for est in estimates)
    total_mass = sum(est["calculated_mass"] for est in estimates)

    col1, col2, col3 = st.columns(3)
    col1.metric("Volume total", f"{total_volume:.3f} m³")
    col2.metric("Masse totale", f"{total_mass:.2f} kg")
    col3.metric("Éléments", len(estimates))

# --- Export CSV
def export_data(estimates):
    if not estimates:
        return None

    total_volume = sum(est["calculated_volume"] for est in estimates)
    total_mass = sum(est["calculated_mass"] for est in estimates)

    export_data = []
    for i, est in enumerate(estimates, start=1):
        export_data.append({
            "N°": i,
            "Matériau": est["material_type"],
            "Masse volumique (kg/m³)": est["density"],
            "Volume (m³)": f"{est['calculated_volume']:.3f}",
            "Masse (kg)": f"{est['calculated_mass']:.2f}",
            "Pourcentage (%)": f"{(est['calculated_mass'] / total_mass * 100):.1f}" if total_mass > 0 else "0.0",
            "Facteur": est["unit_count"],
            "Mode de saisie": "Volume direct" if est["volume_input_type"] == "direct" else "Dimensions",
            "Dimensions (L×l×h)": (
                f"{est['length']}×{est['width']}×{est['height']}"
                if est["volume_input_type"] == "dimensions"
                else "-"
            )
        })

    # Ajout ligne TOTAL
    export_data.append({
        "N°": "",
        "Matériau": "TOTAL",
        "Masse volumique (kg/m³)": "",
        "Volume (m³)": f"{total_volume:.3f}",
        "Masse (kg)": f"{total_mass:.2f}",
        "Pourcentage (%)": "100.0",
        "Mode de saisie": "",
        "Dimensions (L×l×h)": ""
    })

    df = pd.DataFrame(export_data)
    output = StringIO()
    output.write("Diagnostic PEMD - Estimation des masses\n")
    output.write(f"Généré le {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
    df.to_csv(output, index=False, sep=",")
    return output.getvalue()

if estimates:
    csv_data = export_data(estimates)
    st.download_button(
        label="📥 Exporter en Excel (CSV)",
        data=csv_data,
        file_name=f"diagnostic-pemd-{pd.Timestamp.now().date()}.csv",
        mime="text/csv",
    )
