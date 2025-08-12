import pandas as pd
import numpy as np
import streamlit as st
import pickle
from pathlib import Path
from sklearn.metrics import fbeta_score, recall_score, precision_score, accuracy_score
import time


current_path = Path(__file__).resolve()
main_folder_path = current_path.parent.parent 
clean_folder = main_folder_path/ "data" / "clean" 
model_path = main_folder_path /"models" / "svc_best.pkl"

with open(model_path, "rb") as f:
    model = pickle.load(f)


#________________________testing model______________________________
df = pd.read_csv(clean_folder / "hotel_booking_demand_clean_2.csv")
y = df["is_canceled"]
x = df.drop(columns="is_canceled")
# y_pred = model.predict(x)

# f2_score = fbeta_score(y, y_pred, beta=2, zero_division=0)
# recall = recall_score(y,y_pred,zero_division=0)
# precision = precision_score(y,y_pred,zero_division=0)
# accuracy = accuracy_score(y,y_pred)

# print(f"F2 Score      : {f2_score:.3f}")
# print(f"Recall Score  : {recall:.3f}")
# print(f"Precision     : {precision:.3f}")
# print(f"Accuracy      : {accuracy:.3f}")
#__________________________________________________________________


st.set_page_config("Hotel Booking Predict App", page_icon="🏩")

st.title("Hotel Booking Cancellation Prediction App")
st.markdown("""
---
Aplikasi ini memanfaatkan machine learning untuk memprediksi kemungkinan pembatalan reservasi hotel.
Dapatkan insight yang membantu pengelolaan booking, meningkatkan layanan, dan mengurangi kerugian operasional.
""", unsafe_allow_html=True)

st.markdown("""
Model: <br>
**Support Vector Classifier** <br>
*F2 Score* : :green[76%],&nbsp; *Recall* : :green[91%]

""", unsafe_allow_html=True)

tab_single, tab_batch = st.tabs(["Single-Predict", "Multi-Predict"])

#_____________________Single-Predict________________________________
def singe_input():
    st.sidebar.header("Single Prediction Input Features")

    countries = ["PRT", "GBR", "ESP", "FRA", "DEU", "IRL", "ITA", "BEL", "USA",
                "BRA", "NLD", "CHE", "CN", "POL", "SWE", "AUT", "RUS", "CHN", "NOR",
                "FIN", "ISR", "DNK", "ROU", "Others"]
    country = st.sidebar.selectbox("Country", countries)
    market_segment = st.sidebar.selectbox("Market Segment", ['Offline TA/TO', 'Online TA', 'Direct', 
                                                            'Groups', 'Corporate', 'Complementary', 'Aviation'])
    deposit_type = st.sidebar.selectbox("Deposit Type", ['No Deposit', 'Non Refund', 'Refundable'])
    customer_type = st.sidebar.selectbox("Customer Type", ['Transient-Party', 'Transient', 'Contract', 'Group'])
    reserved_room_type = st.sidebar.selectbox("Reserved Room Type", ['A', 'E', 'D', 'F', 'B', 'G', 'C', 'H', 'L', 'P'])
    days_in_waiting_list = st.sidebar.slider("Days in Waiting List",0,60,0)
    previous_cancellations = st.sidebar.slider("Previous Cancellations",0,26,0)
    booking_changes = st.sidebar.slider("Booking Changes",0,21,0)
    required_car_parking_spaces = st.sidebar.slider("Parking Spaces",0,8,0)
    total_of_special_requests = st.sidebar.slider("Special Request",0,5,0)

    data = {"country": country,
            "market_segment": market_segment,
            "previous_cancellations": previous_cancellations,
            "booking_changes": booking_changes,
            "deposit_type": deposit_type,
            "days_in_waiting_list":days_in_waiting_list,
            "customer_type":customer_type,
            "reserved_room_type":reserved_room_type,
            "required_car_parking_spaces":required_car_parking_spaces,
            "total_of_special_requests":total_of_special_requests
            }
    return pd.DataFrame([data])

input_df = singe_input()
tab_single.dataframe(input_df)
bt_single_predict = tab_single.button("Predict!")

if bt_single_predict:
    y_pred = model.predict(input_df)
    if y_pred[0] == 1:
        tab_single.subheader("**Canceled**")
        tab_single.markdown("""
                            Berdasarkan data input yang diberikan, model memprediksi bahwa booking ini berpotensi dibatalkan oleh pelanggan. 
                            Hal ini menunjukkan adanya risiko pembatalan, sehingga disarankan untuk melakukan tindakan pencegahan atau konfirmasi ulang guna meminimalkan dampak negatif pada operasional dan pendapatan.
                            """)
    else:
        tab_single.subheader("**Not Canceled**")
        tab_single.markdown("""
                            Berdasarkan data input yang diberikan, model memprediksi bahwa booking ini kemungkinan akan tetap berjalan tanpa pembatalan. 
                            Hal ini menunjukkan risiko pembatalan yang rendah
                            """)
        
#_____________________Multi-Predict________________________________
with tab_batch:
    st.subheader("Multiple Prediction")
    df_example = pd.read_csv(clean_folder / "example_input.csv")
    csv = df_example.to_csv(index=False)

    st.download_button(
        label="Download CSV Example",
        data=csv,
        file_name="example_input.csv",
        mime="text/csv"
    )

    csv_upload = st.file_uploader("Upload a CSV file :", type="csv")
    if csv_upload:

        upload_df = pd.read_csv(csv_upload)
        y_preds = model.predict(upload_df)
        y_preds_series = pd.Series(y_preds).map({1: "Canceled", 0: "Not Canceled"})

        teks = "{}% Complete"
        bar = st.progress(0)
        for i in range(100):
            bar.progress(i +1 , text=teks.format(i+1))
            time.sleep(0.01)
        bar.empty()
        
        # Buat dua kolom
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Prediction Result")
            st.dataframe(y_preds_series.rename("Prediction"))

        with col2:
            st.subheader("Input Features")
            st.dataframe(upload_df)