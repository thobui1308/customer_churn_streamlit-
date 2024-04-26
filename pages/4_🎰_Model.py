import streamlit as st
import numpy as np
import pandas as pd
import joblib
import pickle
import random

st.title(':card_index: Mô hình dự đoán khách hàng rời bỏ')
##

# Hiển thị dictionary inputs
#st.write(inputs)
#print(inputs)
##

with st.sidebar:
    st.sidebar.image('Customer-Churn.png')
    choice = st.radio('Tùy chọn đầu vào',['Tự nhập đầu vào','Đầu vào ngẫu nhiên'])
    models = st.radio('Chọn loại thuật toán:',['Hồi quy Logistic','Cây quyết định','Rừng cây quyết định'])
    #st.button('Predict')




if choice == 'Tự nhập đầu vào':
    st.write('Vui lòng nhập đầu vào:')
    with st.expander('Nhập thông tin ở đây:'):
        inputs = {}
        st.subheader('**Thông tin về khách hàng**')

        st.write('**1. Giới tính của khách hàng**')
        gender = st.selectbox('*Vui lòng chọn:*', ['Male', 'Female'])

        st.write('**2. Tuổi của khách hàng**')
        age = st.slider('*Vui lòng kéo chọn:*', min_value=18, max_value=100)

        st.write('**3. Tình trạng hôn nhân của khách hàng**')
        married_radio = st.radio('*Vui lòng chọn:*',['Chưa kết hôn', 'Đã kết hôn '])

        st.write('**4. Khách hàng có ở chung với người thân**')
        dependents_radio = st.radio('*Vui lòng chọn:*',['Không sống chung','Sống chung cùng người thân'])
        st.write('**5. Số người thân ở chung**  *(Nếu không có mục 4 vui lòng bỏ qua)* ')
        if dependents_radio == 'Sống chung cùng người thân':
            num_dependents = st.slider('*Vui lòng kéo chọn số người:*', min_value=1, max_value=15)
        else:
            num_dependents = 0
            st.empty()

        st.write('**6. Khách hàng có giới thiệu dịch vụ với người thân**')
        referred_radio = st.radio('*Vui lòng chọn:*',['Không giới thiệu','Khách hàng có giới thiệu dịch vụ với người thân'])
        st.write('**7. Số người được giới thiệu**  *(Nếu không có mục 6 vui lòng bỏ qua)*')
        if referred_radio == 'Khách hàng có giới thiệu dịch vụ với người thân':
            num_referrals = st.slider('*Vui lòng kéo chọn số người:*', min_value=1, max_value=20)
        else:
            num_referrals = 0
            st.empty()

        ##
        st.subheader('**Thông tin về dịch vụ**')

        st.write('**1. Số tháng gắn bó**')
        tenure_months = st.slider('*Vui lòng kéo chọn:*', min_value=1, max_value=120)

        st.write('**2. Điểm hài lòng**')
        satisfaction_score = st.slider('*Vui lòng kéo chọn*', min_value=1, max_value=5)

        st.write('**3. Điểm rời bỏ**')
        churn_score = st.slider('*Vui lòng kéo chọn*', min_value=0, max_value=150, step=1)

        st.write('**4. Điểm vòng đời khách hàng**')
        cltv = st.slider('*Vui lòng kéo chọn*', min_value=2000, max_value=10000, step=1)


        st.write('**5. Loại yêu cầu**')
        offer = st.selectbox('*Vui lòng chọn*', ['Offer A', 'Offer B', 'Offer C', 'Offer D', 'Offer E', 'No Offer'])

        st.write('**6. Loại Internet**')
        internet_type = st.selectbox('*Vui lòng chọn*', ['DSL', 'Fiber Optic', 'Cable', 'No Internet Type'])

        st.write('**7. Loại hợp đồng**')
        contract = st.selectbox('*Vui lòng chọn*', ['Month-to-Month', 'One Year', 'Two Year'])

        st.write('**8. Loại thanh toán**')
        payment_method = st.selectbox('*Vui lòng chọn*', ['Bank Withdrawal', 'Credit Card', 'Mailed Check'])

        st.write('**9. Các loại dịch vụ mà khách hàng sử dụng** *(Chỉ :heavy_check_mark: vào những Dịch vụ có sử dụng )*')
        # Tạo các checkbox và lưu giá trị vào một dictionary
        inputs['Phone Service'] = st.checkbox('Phone Service')
        inputs['Multiple Lines'] = st.checkbox('Multiple Lines')
        inputs['Internet Service'] = st.checkbox('Internet Service')
        inputs['Online Security'] = st.checkbox('Online Security')
        inputs['Online Backup'] = st.checkbox('Online Backup')
        inputs['Device Protection Plan'] = st.checkbox('Device Protection Plan')
        inputs['Premium Tech Support'] = st.checkbox('Premium Tech Support')
        inputs['Streaming TV'] = st.checkbox('Streaming TV')
        inputs['Streaming Movies'] = st.checkbox('Streaming Movies')
        inputs['Streaming Music'] = st.checkbox('Streaming Music')
        inputs['Unlimited Data'] = st.checkbox('Unlimited Data')
        inputs['Paperless Billing'] = st.checkbox('Paperless Billing')

        st.write('**10. Các loại phí**')
        st.write('*Vui lòng điền vào những loại phí dịch vụ mà khách hàng sử dụng (Nếu không có thì bỏ qua)*')
        avg_long_distance_charges = st.number_input('Avg Monthly Long Distance Charges', min_value=0.0, max_value=80.0, step=0.01)
        avg_gb_download = st.number_input('Avg Monthly GB Download', min_value=0, max_value=150, step=1)
        monthly_charge = st.number_input('Monthly Charge', min_value=0.0, max_value=200.0, step=0.01)
        total_charges = st.number_input('Total Charges', min_value=0.0, max_value=10000.0, step=0.01)
        total_refunds = st.number_input('Total Refunds', min_value=0.0, max_value=80.0, step=0.01)
        total_extra_data_charges = st.number_input('Total Extra Data Charges', min_value=0, max_value=200, step=1)
        total_long_distance_charges = st.number_input('Total Long Distance Charges', min_value=0.0, max_value=4000.0, step=0.01)
        total_revenue = st.number_input('Total Revenue', min_value=0.0, max_value=15000.0, step=0.01)

        inputs = {
            'Gender': gender,
            'Age': age,
            'Married': married_radio,
            'Dependents': dependents_radio,
            'Number of Dependents': num_dependents,
            'Referred a Friend': referred_radio,
            'Number of Referrals': num_referrals,
            'Tenure in Months': tenure_months,
            'Offer': offer,
            'Phone Service': 1 if inputs.get('Phone Service') else 0,
            'Avg Monthly Long Distance Charges': avg_long_distance_charges,
            'Multiple Lines': 1 if inputs.get('Multiple Lines') else 0,
            'Internet Service': 1 if inputs.get('Internet Service') else 0,
            'Internet Type': internet_type,
            'Avg Monthly GB Download': avg_gb_download,
            'Online Security': 1 if inputs.get('Online Security') else 0,
            'Online Backup': 1 if inputs.get('Online Backup') else 0,
            'Device Protection Plan': 1 if inputs.get('Device Protection Plan') else 0,
            'Premium Tech Support': 1 if inputs.get('Premium Tech Support') else 0,
            'Streaming TV': 1 if inputs.get('Streaming TV') else 0,
            'Streaming Movies': 1 if inputs.get('Streaming Movies') else 0,
            'Streaming Music': 1 if inputs.get('Streaming Music') else 0,
            'Unlimited Data': 1 if inputs.get('Unlimited Data') else 0,
            'Contract': contract,
            'Paperless Billing': 1 if inputs.get('Paperless Billing') else 0,
            'Payment Method': payment_method,
            'Monthly Charge': monthly_charge,
            'Total Charges': total_charges,
            'Total Refunds': total_refunds,
            'Total Extra Data Charges': total_extra_data_charges,
            'Total Long Distance Charges': total_long_distance_charges,
            'Total Revenue': total_revenue,
            'Satisfaction Score': satisfaction_score,
            'Churn Score': churn_score,
            'CLTV': cltv
        }

        # Chuyển các cột khác sang biến định lượng, không có giá trị mặc định
        inputs['Gender'] = 0 if gender == 'Male' else 1
        inputs['Married'] = 0 if married_radio == 'Chưa kết hôn' else 1
        inputs['Dependents'] = 0 if dependents_radio == 'Không sống chung' else 1
        inputs['Referred a Friend'] = 0 if referred_radio == 'Không giới thiệu' else 1
        inputs['Offer'] = {'Offer A': 1, 'Offer B': 2, 'Offer C': 3, 'Offer D': 4, 'Offer E': 5, 'No Offer':6}.get(inputs['Offer'])
        inputs['Internet Type'] = {'DSL': 1, 'Fiber Optic': 2, 'Cable': 3, 'No Internet Type': 4}.get(inputs['Internet Type'])
        inputs['Contract'] = {'Month-to-Month': 1, 'One Year': 2, 'Two Year': 3}.get(inputs['Contract'])
        inputs['Payment Method'] = {'Bank Withdrawal': 1, 'Credit Card': 2, 'Mailed Check': 3}.get(inputs['Payment Method'])
    



if choice == 'Đầu vào ngẫu nhiên':
    def generate_random_inputs():
        gender = random.choice(['Male', 'Female'])
        age = random.randint(18, 100)
        married_radio = random.choice(['Chưa kết hôn', 'Đã kết hôn '])
        dependents_radio = random.choice(['Không sống chung','Sống chung cùng người thân'])
        num_dependents = random.randint(0, 15) if dependents_radio == 'Sống chung cùng người thân' else 0
        referred_radio = random.choice(['Không giới thiệu','Khách hàng có giới thiệu dịch vụ với người thân'])
        num_referrals = random.randint(0, 20) if referred_radio == 'Khách hàng có giới thiệu dịch vụ với người thân' else 0
        tenure_months = random.randint(1, 120)
        satisfaction_score = random.randint(1, 5)
        churn_score = random.randint(0, 150)
        cltv = random.randint(2000, 10000)
        offer = random.choice(['Offer A', 'Offer B', 'Offer C', 'Offer D', 'Offer E', 'No Offer'])
        internet_type = random.choice(['DSL', 'Fiber Optic', 'Cable', 'No Internet Type'])
        contract = random.choice(['Month-to-Month', 'One Year', 'Two Year'])
        payment_method = random.choice(['Bank Withdrawal', 'Credit Card', 'Mailed Check'])

        random_inputs = {
            'Gender': gender,
            'Age': age,
            'Married': married_radio,
            'Dependents': dependents_radio,
            'Number of Dependents': num_dependents,
            'Referred a Friend': referred_radio,
            'Number of Referrals': num_referrals,
            'Tenure in Months': tenure_months,
            'Offer': offer,
            'Phone Service': random.choice([0, 1]),
            'Avg Monthly Long Distance Charges': random.uniform(0.0, 80.0),
            'Multiple Lines': random.choice([0, 1]),
            'Internet Service': random.choice([0, 1]),
            'Internet Type': internet_type,
            'Avg Monthly GB Download': random.randint(0, 150),
            'Online Security': random.choice([0, 1]),
            'Online Backup': random.choice([0, 1]),
            'Device Protection Plan': random.choice([0, 1]),
            'Premium Tech Support': random.choice([0, 1]),
            'Streaming TV': random.choice([0, 1]),
            'Streaming Movies': random.choice([0, 1]),
            'Streaming Music': random.choice([0, 1]),
            'Unlimited Data': random.choice([0, 1]),
            'Contract': contract,
            'Paperless Billing': random.choice([0, 1]),
            'Payment Method': payment_method,
            'Monthly Charge': random.uniform(0.0, 200.0),
            'Total Charges': random.uniform(0.0, 10000.0),
            'Total Refunds': random.uniform(0.0,80.0),
            'Total Extra Data Charges': random.randint(0,200),
            'Total Long Distance Charges': random.uniform(0.0,4000.0),
            'Total Revenue': random.uniform(0.0,15000.0),
            'Satisfaction Score': satisfaction_score,
            'Churn Score': churn_score,
            'CLTV': cltv
        }
        
        return random_inputs

    # Giao diện người dùng
    st.write('Đầu vào ngẫu nhiên:')
    with st.expander('Xem thông tin ở đây:'):
        inputs = generate_random_inputs()
        st.subheader('**Thông tin về khách hàng**')

        st.write('**1. Giới tính của khách hàng**')
        gender = st.selectbox('*Vui lòng chọn:*', ['Male', 'Female'], index=0 if inputs['Gender'] == 'Male' else 1)

        st.write('**2. Tuổi của khách hàng**')
        age = st.slider('*Vui lòng kéo chọn:*', min_value=18, max_value=100, value=inputs['Age'])

        st.write('**3. Tình trạng hôn nhân của khách hàng**')
        married_radio = st.radio('*Vui lòng chọn:*',['Chưa kết hôn', 'Đã kết hôn '], index=0 if inputs['Married'] == 'Chưa kết hôn' else 1)

        st.write('**4. Khách hàng có ở chung với người thân**')
        dependents_radio = st.radio('*Vui lòng chọn:*',['Không sống chung','Sống chung cùng người thân'], index=0 if inputs['Dependents'] == 'Không sống chung' else 1)
        st.write('**5. Số người thân ở chung**  *(Nếu không có mục 4 vui lòng bỏ qua)* ')
        if dependents_radio == 'Sống chung cùng người thân':
            num_dependents = st.slider('*Vui lòng kéo chọn số người:*', min_value=1, max_value=15, value=inputs['Number of Dependents'])
        else:
            num_dependents = 0
            st.empty()

        st.write('**6. Khách hàng có giới thiệu dịch vụ với người thân**')
        referred_radio = st.radio('*Vui lòng chọn:*',['Không giới thiệu','Khách hàng có giới thiệu dịch vụ với người thân'], index=0 if inputs['Referred a Friend'] == 'Không giới thiệu' else 1)
        st.write('**7. Số người được giới thiệu**  *(Nếu không có mục 6 vui lòng bỏ qua)*')
        if referred_radio == 'Khách hàng có giới thiệu dịch vụ với người thân':
            num_referrals = st.slider('*Vui lòng kéo chọn số người:*', min_value=1, max_value=20, value=inputs['Number of Referrals'])
        else:
            num_referrals = 0
            st.empty()

        ##
        st.subheader('**Thông tin về dịch vụ**')

        st.write('**1. Số tháng gắn bó**')
        tenure_months = st.slider('*Vui lòng kéo chọn:*', min_value=1, max_value=120, value=inputs['Tenure in Months'])

        st.write('**2. Điểm hài lòng**')
        satisfaction_score = st.slider('*Vui lòng kéo chọn*', min_value=1, max_value=5, value=inputs['Satisfaction Score'])

        st.write('**3. Điểm rời bỏ**')
        churn_score = st.slider('*Vui lòng kéo chọn*', min_value=0, max_value=150, step=1, value=inputs['Churn Score'])

        st.write('**4. Điểm vòng đời khách hàng**')
        cltv = st.slider('*Vui lòng kéo chọn*', min_value=2000, max_value=10000, step=1, value=inputs['CLTV'])
        ###
        offer_mapping = {'Offer A': 1, 'Offer B': 2, 'Offer C': 3, 'Offer D': 4, 'Offer E': 5, 'No Offer': 6}
        internet_type_mapping = {'DSL': 1, 'Fiber Optic': 2, 'Cable': 3, 'No Internet Type': 4}
        contract_mapping = {'Month-to-Month': 1, 'One Year': 2, 'Two Year': 3}
        payment_method_mapping = {'Bank Withdrawal': 1, 'Credit Card': 2, 'Mailed Check': 3}

        offer_index = offer_mapping[inputs['Offer']]
        internet_type_index = internet_type_mapping[inputs['Internet Type']]
        contract_index = contract_mapping[inputs['Contract']]
        payment_method_index = payment_method_mapping[inputs['Payment Method']]

        st.write('**5. Loại yêu cầu**')
        offer = st.selectbox('*Vui lòng chọn*', ['Offer A', 'Offer B', 'Offer C', 'Offer D', 'Offer E', 'No Offer'], index=offer_index - 1)
        st.write('**6. Loại Internet**')
        internet_type = st.selectbox('*Vui lòng chọn*', ['DSL', 'Fiber Optic', 'Cable', 'No Internet Type'], index=internet_type_index - 1)
        st.write('**7. Loại hợp đồng**')
        contract = st.selectbox('*Vui lòng chọn*', ['Month-to-Month', 'One Year', 'Two Year'], index=contract_index - 1)
        st.write('**8. Loại thanh toán**')
        payment_method = st.selectbox('*Vui lòng chọn*', ['Bank Withdrawal', 'Credit Card', 'Mailed Check'], index=payment_method_index - 1)

        ##
        st.write('**9. Các loại dịch vụ mà khách hàng sử dụng** *(Chỉ :heavy_check_mark: vào những Dịch vụ có sử dụng )*')
        inputs['Phone Service'] = st.checkbox('Phone Service', value=inputs['Phone Service'])
        inputs['Multiple Lines'] = st.checkbox('Multiple Lines', value=inputs['Multiple Lines'])
        inputs['Internet Service'] = st.checkbox('Internet Service', value=inputs['Internet Service'])
        inputs['Online Security'] = st.checkbox('Online Security', value=inputs['Online Security'])
        inputs['Online Backup'] = st.checkbox('Online Backup', value=inputs['Online Backup'])
        inputs['Device Protection Plan'] = st.checkbox('Device Protection Plan', value=inputs['Device Protection Plan'])
        inputs['Premium Tech Support'] = st.checkbox('Premium Tech Support', value=inputs['Premium Tech Support'])
        inputs['Streaming TV'] = st.checkbox('Streaming TV', value=inputs['Streaming TV'])
        inputs['Streaming Movies'] = st.checkbox('Streaming Movies', value=inputs['Streaming Movies'])
        inputs['Streaming Music'] = st.checkbox('Streaming Music', value=inputs['Streaming Music'])
        inputs['Unlimited Data'] = st.checkbox('Unlimited Data', value=inputs['Unlimited Data'])
        inputs['Paperless Billing'] = st.checkbox('Paperless Billing', value=inputs['Paperless Billing'])


        st.write('**10. Các loại phí**')
        st.write('*Vui lòng điền vào những loại phí dịch vụ mà khách hàng sử dụng (Nếu không có thì bỏ qua)*')
        avg_long_distance_charges = st.number_input('Avg Monthly Long Distance Charges', min_value=0.0, max_value=80.0, step=0.01, value=inputs['Avg Monthly Long Distance Charges'])
        avg_gb_download = st.number_input('Avg Monthly GB Download', min_value=0, max_value=150, step=1, value=inputs['Avg Monthly GB Download'])
        monthly_charge = st.number_input('Monthly Charge', min_value=0.0, max_value=200.0, step=0.01, value=inputs['Monthly Charge'])
        total_charges = st.number_input('Total Charges', min_value=0.0, max_value=10000.0, step=0.01, value=inputs['Total Charges'])
        total_refunds = st.number_input('Total Refunds', min_value=0.0, max_value=80.0, step=0.01, value=inputs['Total Refunds'])
        total_extra_data_charges = st.number_input('Total Extra Data Charges', min_value=0, max_value=200, step=1, value=inputs['Total Extra Data Charges'])
        total_long_distance_charges = st.number_input('Total Long Distance Charges', min_value=0.0, max_value=4000.0, step=0.01, value=inputs['Total Long Distance Charges'])
        total_revenue = st.number_input('Total Revenue', min_value=0.0, max_value=15000.0, step=0.01, value=inputs['Total Revenue'])

        inputs.update({
            'Tenure in Months': tenure_months,
            'Satisfaction Score': satisfaction_score,
            'Churn Score': churn_score,
            'CLTV': cltv,
            'Offer': offer,
            'Internet Type': internet_type,
            'Contract': contract,
            'Payment Method': payment_method,
            'Avg Monthly Long Distance Charges': avg_long_distance_charges,
            'Avg Monthly GB Download': avg_gb_download,
            'Monthly Charge': monthly_charge,
            'Total Charges': total_charges,
            'Total Refunds': total_refunds,
            'Total Extra Data Charges': total_extra_data_charges,
            'Total Long Distance Charges': total_long_distance_charges,
            'Total Revenue': total_revenue
        })
        #
        inputs = {
        'Gender': 0 if gender == 'Male' else 1,
        'Age': age,
        'Married': 0 if married_radio == 'Chưa kết hôn' else 1,
        'Dependents': 0 if dependents_radio == 'Không sống chung' else 1,
        'Number of Dependents': num_dependents,
        'Referred a Friend': 0 if referred_radio == 'Không giới thiệu' else 1,
        'Number of Referrals': num_referrals,
        'Tenure in Months': tenure_months,
        'Offer': {'Offer A': 1, 'Offer B': 2, 'Offer C': 3, 'Offer D': 4, 'Offer E': 5, 'No Offer': 6}.get(offer),
        'Phone Service': 1 if inputs.get('Phone Service') else 0,
        'Avg Monthly Long Distance Charges': avg_long_distance_charges,
        'Multiple Lines': 1 if inputs.get('Multiple Lines') else 0,
        'Internet Service': 1 if inputs.get('Internet Service') else 0,
        'Internet Type': {'DSL': 1, 'Fiber Optic': 2, 'Cable': 3, 'No Internet Type': 4}.get(internet_type),
        'Avg Monthly GB Download': avg_gb_download,
        'Online Security': 1 if inputs.get('Online Security') else 0,
        'Online Backup': 1 if inputs.get('Online Backup') else 0,
        'Device Protection Plan': 1 if inputs.get('Device Protection Plan') else 0,
        'Premium Tech Support': 1 if inputs.get('Premium Tech Support') else 0,
        'Streaming TV': 1 if inputs.get('Streaming TV') else 0,
        'Streaming Movies': 1 if inputs.get('Streaming Movies') else 0,
        'Streaming Music': 1 if inputs.get('Streaming Music') else 0,
        'Unlimited Data': 1 if inputs.get('Unlimited Data') else 0,
        'Contract': {'Month-to-Month': 1, 'One Year': 2, 'Two Year': 3}.get(contract),
        'Paperless Billing': 1 if inputs.get('Paperless Billing') else 0,
        'Payment Method': {'Bank Withdrawal': 1, 'Credit Card': 2, 'Mailed Check': 3}.get(payment_method),
        'Monthly Charge': monthly_charge,
        'Total Charges': total_charges,
        'Total Refunds': total_refunds,
        'Total Extra Data Charges': total_extra_data_charges,
        'Total Long Distance Charges': total_long_distance_charges,
        'Total Revenue': total_revenue,
        'Satisfaction Score': satisfaction_score,
        'Churn Score': churn_score,
        'CLTV': cltv
        }
    #st.write(inputs)


def predict_with_model(inputs):
    input_df = pd.DataFrame([inputs])
    if models == 'Hồi quy Logistic':
        model = joblib.load('logistic_regression_model.pkl')
    elif models == 'Cây quyết định':
        model = joblib.load('decision_tree_model.pkl')
    elif models == 'Rừng cây quyết định':
        model = joblib.load('random_forest_model.pkl')
    prediction = model.predict(input_df)
    if prediction == 1:
        st.error('Khách hàng rời bỏ :sob:')
    else:
        st.success('Khách hàng ở lại :hugging_face:')

# Xử lý sự kiện khi người dùng nhấn nút "Predict"
if st.button('Predict', key='predict_button'):
    predict_with_model(inputs)




