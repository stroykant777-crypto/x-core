import streamlit as st
import pandas as pd

st.set_page_config(page_title="X_CORE: Смета", layout="wide")

# --- НАСТРОЙКИ ---
ADMIN_PASSWORD = "371555371"  # Установи здесь свой секретный пароль

# Инициализация базы
if "master_prices" not in st.session_state:
    st.session_state.master_prices = pd.DataFrame({
        "Вид работ": ["Штукатурка", "Стяжка", "Малярка", "Ламинат", "Кафель"],
        "Себестоимость (сом)": [200, 150, 100, 120, 450],
        "Маржа (%)": [30, 40, 50, 35, 40]
    })
    st.session_state.master_prices["Количество"] = 0.0

st.title("🏗️ X_CORE: Сметный калькулятор")

# --- АВТОРИЗАЦИЯ ---
st.sidebar.subheader("🔒 Вход для администратора")
password = st.sidebar.text_input("Введите пароль для изменения цен", type="password")
is_admin = (password == ADMIN_PASSWORD)

# --- ЛОГИКА ВКЛАДОК ---
if is_admin:
    tab1, tab2 = st.tabs(["📊 Прайс-лист (Админ)", "🧮 Калькулятор сметы"])
    
    with tab1:
        st.warning("⚠️ Внимание: Вы в режиме администратора. Изменения влияют на всех!")
        admin_df = st.data_editor(
            st.session_state.master_prices.drop(columns=["Количество"]),
            num_rows="dynamic",
            use_container_width=True
        )
        if st.button("💾 Сохранить изменения цен"):
            st.session_state.master_prices.update(admin_df)
            st.success("Прайс-лист обновлен!")
else:
    # Если не админ — показываем только калькулятор
    tab2 = st.container()
    st.sidebar.info("Вы в режиме гостя. Доступ к ценам ограничен.")

# --- ВКЛАДКА КАЛЬКУЛЯТОРА (Видна всем) ---
with tab2:
    st.subheader("Расчет сметы")
    calc_df = st.session_state.master_prices.copy()
    calc_df["Цена для клиента"] = (calc_df["Себестоимость (сом)"] * (1 + calc_df["Маржа (%)"] / 100)).round(2)
    
    edited_estimate = st.data_editor(
        calc_df[["Вид работ", "Цена для клиента", "Количество"]],
        disabled=["Вид работ", "Цена для клиента"],
        use_container_width=True
    )
    
    edited_estimate["Сумма (сом)"] = edited_estimate["Цена для клиента"] * edited_estimate["Количество"]
    grand_total = edited_estimate["Сумма (сом)"].sum()
    
    st.write("---")
    st.metric(label="💰 ОБЩАЯ СУММА СМЕТЫ", value=f"{grand_total:,.2f} сом")