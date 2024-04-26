import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 

st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu(
        menu_title = "Dashboard",
        options = ["Khách hàng","Dịch vụ","Nguyên nhân rời bỏ"],
        icons=['person-circle','telephone-fill','chat-quote-fill'],
        menu_icon='file-earmark-bar-graph'
        )
    



if selected == "Khách hàng":
    st.title(f':shopping_bags: Chân dung khách hàng')
    #read data
    df = pd.read_excel("df_dashboard.xlsx",index_col=0)

    #side bar
    st.sidebar.header('Lọc dữ liệu tại đây:')
    #create filter
    status_options = list(df['Customer Status'].unique())
    select_status_options = st.sidebar.multiselect(
        "Nhóm khách hàng:",
        options = status_options,
        default=[]
    )
    if not select_status_options:
        df_filtered = df.copy()
    else:
        df_filtered = df[df['Customer Status'].isin(select_status_options)]

    #overview
    @st.cache_data
    def compute_statistics(df_filtered):
        total_customer = len(df_filtered)
        total_group = df_filtered['Customer Status'].nunique()
        mean_age = df_filtered['Age'].mean()

        return total_customer, total_group, mean_age

    total_customer, total_group, mean_age = compute_statistics(df_filtered)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.info('Tổng số khách hàng:')
        st.subheader("{:,}:shopping_bags:".format(total_customer))
    with middle_column:
        st.info('Nhóm khách hàng:')
        st.subheader(f'{total_group} :man-girl-boy:')
    with right_column:
        st.info('Độ tuổi trung bình của khách hàng:')
        st.subheader(f'{int(mean_age)} :hourglass:' )
    st.markdown('---')

    #Plot
    ##Pie_Customer status
    customer_status_count = df_filtered['Customer Status'].value_counts()
    fig = px.pie(
        values=customer_status_count.values, 
        names=customer_status_count.index, 
        title='Phân nhóm khách hàng'
    )
    # Cài đặt kích thước của biểu đồ
    fig.update_layout(width=1100,height=450)
    st.plotly_chart(fig)

    ##
    # Chia cột thành hai cột
    left_column, right_column = st.columns(2)

    with left_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm
        customer_count = df_filtered.groupby(['Customer Status', 'Gender']).size().reset_index(name='Count')
        # Tính toán phần trăm khách hàng theo giới tính và trạng thái của khách hàng
        total_per_status = customer_count.groupby('Customer Status')['Count'].transform('sum')
        customer_count['Percentage'] = (customer_count['Count'] / total_per_status) * 100
        # Tạo biểu đồ cột ghép bằng Plotly Express
        fig = px.bar(customer_count, x='Customer Status', y='Percentage', color='Gender',
                    barmode='group', text='Count', title='Giới tính khách hàng')
        # Hiển thị giá trị số lượng và phần trăm trên cột
        fig.update_traces(texttemplate='%{text:.0f}', textposition='inside')
        fig.update_yaxes(title_text="Phần trăm (%)")
        fig.update_xaxes(title_text="Nhóm khách hàng")
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=550,height=400)
        # Hiển thị biểu đồ cột ghép trong Streamlit
        st.plotly_chart(fig)

    with right_column: 
        # Tính toán số lượng khách hàng trong mỗi nhóm
        customer_count = df_filtered.groupby(['Customer Status', 'Married']).size().reset_index(name='Count')
        # Tính toán phần trăm khách hàng theo giới tính và trạng thái của khách hàng
        total_per_status = customer_count.groupby('Customer Status')['Count'].transform('sum')
        customer_count['Percentage'] = (customer_count['Count'] / total_per_status) * 100
        # Tạo biểu đồ cột ghép bằng Plotly Express
        color_map_married = {'Yes': 'darkred', 'No': 'red'}
        fig = px.bar(customer_count, x='Customer Status', y='Percentage', color='Married',
                    barmode='group', text='Count', title='Tình trạng hôn nhân của khách hàng',
                    color_discrete_map=color_map_married)
        # Hiển thị giá trị số lượng và phần trăm trên cột
        fig.update_traces(texttemplate='%{text:.0f}', textposition='inside')
        fig.update_yaxes(title_text="Phần trăm (%)")
        fig.update_xaxes(title_text="Nhóm khách hàng")
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=550,height=400)
        # Hiển thị biểu đồ cột ghép trong Streamlit
        st.plotly_chart(fig)

    ##
    # Chia cột thành hai cột
    left_column, right_column = st.columns(2)
    with left_column:
        # Vẽ biểu đồ KDE bằng Seaborn
        import seaborn as sns
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 6))
        sns.kdeplot(data=df_filtered['Age'], shade=True)
        plt.title('Phân phối tuổi của khách hàng')
        plt.xlabel('Tuổi')
        plt.ylabel('Mật độ')
        plt.grid(True)
        plt.xticks(range(20, 80, 5))
        plt.yticks(range(0, 1, 1))
        plt.grid(False)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Xóa khung
        sns.despine()
        # Hiển thị biểu đồ KDE trong Streamlit
        st.pyplot()

    with right_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm tuổi và trạng thái
        customer_count = df_filtered.groupby(['Age Range', 'Customer Status']).size().reset_index(name='Count')
        # Tạo biểu đồ Sunburst bằng Plotly Express
        fig = px.sunburst(customer_count, path=['Customer Status', 'Age Range'], values='Count',
                        title='Nhóm tuổi của khách hàng')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=550,height=450)
        # Hiển thị biểu đồ Sunburst trong Streamlit
        st.plotly_chart(fig)

    ##
    left_column, right_column = st.columns(2)

    with left_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm
        customer_count = df_filtered.groupby(['Customer Status', 'Dependents']).size().reset_index(name='Count')
        # Tính toán phần trăm khách hàng theo giới tính và trạng thái của khách hàng
        total_per_status = customer_count.groupby('Customer Status')['Count'].transform('sum')
        customer_count['Percentage'] = (customer_count['Count'] / total_per_status) * 100
        # Tạo biểu đồ cột ghép bằng Plotly Express
        color_map_married = {'Yes': 'yellow', 'No': 'lightgoldenrodyellow'}
        fig = px.bar(customer_count, x='Customer Status', y='Percentage', color='Dependents',
                    barmode='group', text='Count', title='Khách hàng có ở chung với người thân hay không?',
                    color_discrete_map=color_map_married)
        # Hiển thị giá trị số lượng và phần trăm trên cột
        fig.update_traces(texttemplate='%{text:.0f}', textposition='inside')
        fig.update_yaxes(title_text="Phần trăm (%)")
        fig.update_xaxes(title_text="Nhóm khách hàng")
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=550,height=400)
        # Hiển thị biểu đồ cột ghép trong Streamlit
        st.plotly_chart(fig)

    with right_column:
        # Đếm số lượng Customer ID cho mỗi nhóm
        df_count = df_filtered.groupby([ 'Number of Dependents','Customer Status',]).size().reset_index(name='Count')
        # Tạo biểu đồ cây bằng Plotly Express
        fig = px.treemap(df_count, path=['Number of Dependents', 'Customer Status'], values='Count',
                        title='Số người thân ở chung với khách hàng')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=600,height=450)
        # Hiển thị biểu đồ cây trong Streamlit
        st.plotly_chart(fig)




    
if selected == "Dịch vụ":
    st.title(f':telephone: Dịch vụ')
    #read data
    df = pd.read_excel("df_dashboard.xlsx",index_col=0)

    #side bar
    st.sidebar.header('Lọc dữ liệu tại đây:')
    #create filter
    status_options = list(df['Customer Status'].unique())
    select_status_options = st.sidebar.multiselect(
        "Nhóm khách hàng:",
        options = status_options,
        default=[]
    )
    if not select_status_options:
        df_filtered = df.copy()
    else:
        df_filtered = df[df['Customer Status'].isin(select_status_options)]

    #overview
    @st.cache_data
    def compute_statistics(df_filtered):
        total_service = len(df_filtered)
        mean_tenure = round(df_filtered['Tenure in Months'].mean(),2)
        mean_satisfied = round(df_filtered['Satisfaction Score'].mean(),1)
        star_rating = ":star:" * int(mean_satisfied)
        mean_age = df_filtered['Number of Referrals'].mean()

        return total_service, mean_tenure, mean_satisfied, mean_age, star_rating

    total_service, mean_tenure, mean_satisfied, mean_age, star_rating = compute_statistics(df_filtered)

    left_column, middle_left_column, middle_right_column, right_column = st.columns(4)
    with left_column:
        st.info('Tổng số dịch vụ:')
        st.subheader("{:,} :telephone_receiver:".format(total_service))
    with middle_left_column:
        st.info('Trung bình tháng hợp đồng:')
        st.subheader(f"{mean_tenure} :memo:")
    with middle_right_column:
        st.info('Mức độ hài lòng:')
        st.subheader(f'{mean_satisfied} {star_rating}')
    with right_column:
        st.info('Trung bình số người được giới thiệu:')
        st.subheader(f'{int(mean_age)} :love_letter:')
    st.markdown('---')

    ##
    left_column, right_column = st.columns(2)
    with left_column:
        # Đếm số lượng khách hàng trong mỗi nhóm
        df_count = df_filtered.groupby(['Customer Status', 'Tenure in Months']).size().reset_index(name='Count')

        # Tạo biểu đồ vùng bằng Plotly Express
        fig = px.area(df_count, x='Tenure in Months', y='Count', 
                    color='Customer Status', title='Số khách hàng theo số tháng sử dụng hợp đồng')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=590,height=460)
        # Hiển thị biểu đồ vùng trong Streamlit
        st.plotly_chart(fig)
    with right_column:
        # Đếm số lượng Customer ID cho mỗi nhóm
        df_count = df_filtered.groupby([ 'Contract','Customer Status',]).size().reset_index(name='Count')
        # Tạo biểu đồ cây bằng Plotly Express
        fig = px.treemap(df_count, path=['Contract', 'Customer Status'], values='Count',
                        title='Loại hợp đồng')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=550,height=460)
        # Hiển thị biểu đồ cây trong Streamlit
        st.plotly_chart(fig)

    ##
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm tuổi và trạng thái
        customer_count = df_filtered.groupby(['Internet Type', 'Customer Status']).size().reset_index(name='Count')
        # Tạo biểu đồ Sunburst bằng Plotly Express
        fig = px.sunburst(customer_count, path=['Customer Status', 'Internet Type'], values='Count',
                        title='Loại Internet')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=300,height=400)
        # Hiển thị biểu đồ Sunburst trong Streamlit
        st.plotly_chart(fig)
    with middle_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm tuổi và trạng thái
        customer_count = df_filtered.groupby(['Offer', 'Customer Status']).size().reset_index(name='Count')
        # Tạo biểu đồ Sunburst bằng Plotly Express
        fig = px.sunburst(customer_count, path=['Customer Status', 'Offer'], values='Count',
                        title='Các loại yêu cầu')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=300,height=400)
        # Hiển thị biểu đồ Sunburst trong Streamlit
        st.plotly_chart(fig)
    with right_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm tuổi và trạng thái
        customer_count = df_filtered.groupby(['Payment Method', 'Customer Status']).size().reset_index(name='Count')
        # Tạo biểu đồ Sunburst bằng Plotly Express
        fig = px.sunburst(customer_count, path=['Customer Status', 'Payment Method'], values='Count',
                        title='Các phương thức thanh toán')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=350,height=400)
        # Hiển thị biểu đồ Sunburst trong Streamlit
        st.plotly_chart(fig)

    ##
    left_column, right_column = st.columns(2)
    with left_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm tuổi và trạng thái
        customer_count = df_filtered.groupby(['Satisfaction Score', 'Customer Status']).size().reset_index(name='Count')
        # Tạo biểu đồ Sunburst bằng Plotly Express
        fig = px.sunburst(customer_count, path=['Customer Status', 'Satisfaction Score'], values='Count',
                        title='Điểm hài lòng')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=600,height=430)
        # Hiển thị biểu đồ Sunburst trong Streamlit
        st.plotly_chart(fig)
    with right_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm tuổi và trạng thái
        customer_count = df_filtered.groupby(['Referred a Friend','Number of Referrals', 'Customer Status']).size().reset_index(name='Count')
        # Tạo biểu đồ Sunburst bằng Plotly Express
        fig = px.sunburst(customer_count, path=['Customer Status', 'Referred a Friend','Number of Referrals'], values='Count',
                        title='Khách hàng giới thiệu bạn bè')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=600,height=430)
        # Hiển thị biểu đồ Sunburst trong Streamlit
        st.plotly_chart(fig)
    ##
    st.write('**Các loại dịch vụ theo nhóm khách hàng:**')
    Service = ['Phone Service', 'Multiple Lines','Internet Service', 'Online Security', 'Online Backup',
                'Device Protection Plan', 'Premium Tech Support', 'Streaming TV', 'Streaming Movies', 'Streaming Music', 'Unlimited Data']
    choose_service = st.selectbox('Please select a service', Service)
    if choose_service:
        # Nhóm dữ liệu theo cả hai biến Customer Status và Phone Service, tính tổng số lượng khách hàng cho mỗi nhóm
        customer_count = df_filtered.groupby([choose_service,'Customer Status']).size().reset_index(name='Count')

        # Tạo biểu đồ cột ghép bằng Plotly Express
        fig = px.bar(customer_count, x=choose_service, y='Count', color='Customer Status',
                    barmode='group',
                    labels={'Customer Status': 'Trạng thái khách hàng', 'Count': 'Số người dùng',
                            choose_service: 'Dịch vụ'})

        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=1100, height=450)

        # Hiển thị biểu đồ cột ghép trong Streamlit
        st.plotly_chart(fig)
    ##
    st.write('**Các loại phí theo nhóm khách hàng:**')
    Fee = ['Avg Monthly Long Distance Charges', 'Avg Monthly GB Download', 'Monthly Charge', 'Total Charges', 'Total Refunds',
            'Total Extra Data Charges', 'Total Long Distance Charges', 'Total Revenue']
    choose_fee = st.selectbox('Please select a fee', Fee)
    if choose_fee:
        fig = px.box(df_filtered, x='Customer Status', y=choose_fee,
                    labels={'Customer Status': 'Trạng thái khách hàng', choose_fee: 'Phí'})
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=1100, height=450)
    # Hiển thị biểu đồ boxplot trong Streamlit
    st.plotly_chart(fig)




if selected == "Nguyên nhân rời bỏ":
    st.title(f':runner::shopping_trolley: Nguyên nhân rời bỏ')
    #read data
    df = pd.read_excel("df_dashboard.xlsx",index_col=0)
    #overview
    @st.cache_data
    def compute_statistics(df):
        df_churned = df[df['Customer Status'] == 'Churned']
        total_customer = len(df_churned)
        mean_satisfied = round(df_churned['Satisfaction Score'].mean(),1)
        star_rating = ":star:" * int(mean_satisfied)
        total_group_reason = df['Churn Category'].nunique()
        total_reason = df['Churn Reason'].nunique()
        mean_churn_score = round(df['Churn Score'].mean(),2)
        mean_cltv = round(df['CLTV'].mean(),2)

        return total_customer, mean_churn_score, mean_satisfied, mean_cltv, star_rating, total_group_reason,total_reason

    total_customer, mean_churn_score, mean_satisfied, mean_cltv, star_rating, total_group_reason,total_reason = compute_statistics(df)

    left_column, middle_left_column, middle_right_column, right_column = st.columns(4)
    with left_column:
        st.info('Tổng số khách hàng rời bỏ:')
        st.subheader("{:,} :runner:".format(total_customer))
    with middle_left_column:
        st.info('Mức độ hài lòng:')
        st.subheader(f'{mean_satisfied} {star_rating}')
    with middle_right_column:
        st.info('Nhóm lý do rời bỏ:')
        st.subheader(f"{total_group_reason} :chart_with_downwards_trend:")
    with right_column:
        st.info('Lý do rời bỏ:')
        st.subheader(f'{total_reason} :thumbsdown:')
    st.markdown('---')
    # Lọc DataFrame để chỉ bao gồm khách hàng có trạng thái là "Churned"
    df_churned = df[df['Customer Status'] == 'Churned']
    # Tính toán số lượng khách hàng trong mỗi nhóm tuổi và trạng thái
    customer_count = df_churned.groupby(['Churn Category', 'Churn Reason']).size().reset_index(name='Count')
    # Tạo biểu đồ Sunburst bằng Plotly Express
    fig = px.sunburst(customer_count, path=['Churn Category', 'Churn Reason'], values='Count',
                    title='Nhóm lý do và các lý do khách hàng rời bỏ doanh nghiệp')
    # Cài đặt kích thước của biểu đồ
    fig.update_layout(width=1100, height=600)
    # Hiển thị biểu đồ Sunburst trong Streamlit
    st.plotly_chart(fig)
    ##
    left_column, right_column = st.columns(2)
    with left_column:
        st.info('Trung bình điểm rời bỏ:')
        st.subheader("{:,}".format(mean_churn_score))
    with right_column:
        st.info('Trung bình điểm vòng đời khách hàng:')
        st.subheader(f"{mean_cltv}")
    left_column, right_column = st.columns(2)
    with left_column:
        # Đếm số lượng từng nhóm trong CLTV Category
        df_count = df['Churn Score Category'].value_counts().reset_index(name='Count')
        df_count.columns = ['Churn Score Category', 'Count']
        # Tạo biểu đồ vùng bằng Plotly Express
        fig = px.area(df_count, x='Churn Score Category', y='Count', 
                    title='Số lượng khách hàng theo Nhóm điểm rời bỏ')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=590, height=460)
        # Hiển thị biểu đồ vùng trong Streamlit
        st.plotly_chart(fig)
    with right_column:
                # Đếm số lượng từng nhóm trong CLTV Category
        df_count = df['CLTV Category'].value_counts().reset_index(name='Count')
        df_count.columns = ['CLTV Category', 'Count']
        # Tạo biểu đồ vùng bằng Plotly Express
        fig = px.area(df_count, x='CLTV Category', y='Count', 
                    title='Số lượng khách hàng theo Nhóm điểm Vòng đời khách hàng')
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=590, height=460)
        # Hiển thị biểu đồ vùng trong Streamlit
        st.plotly_chart(fig)

    left_column, right_column = st.columns(2)

    with left_column:
        # Tính toán số lượng khách hàng trong mỗi nhóm
        customer_count = df.groupby(['Customer Status', 'Churn Score Category']).size().reset_index(name='Count')
        # Tính toán phần trăm khách hàng theo giới tính và trạng thái của khách hàng
        total_per_status = customer_count.groupby('Customer Status')['Count'].transform('sum')
        customer_count['Percentage'] = (customer_count['Count'] / total_per_status) * 100
        # Tạo biểu đồ cột ghép bằng Plotly Express
        fig = px.bar(customer_count, x='Churn Score Category', y='Percentage', color='Customer Status',
                    barmode='group', text='Count', title='Số lượng khách hàng trong từng nhóm Điểm rời bỏ')
        # Hiển thị giá trị số lượng và phần trăm trên cột
        fig.update_traces(texttemplate='%{text:.0f}', textposition='inside')
        fig.update_yaxes(title_text="Phần trăm (%)")
        fig.update_xaxes(title_text="Nhóm khách hàng")
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=550,height=400)
        # Hiển thị biểu đồ cột ghép trong Streamlit
        st.plotly_chart(fig)

    with right_column: 
        # Tính toán số lượng khách hàng trong mỗi nhóm
        customer_count = df.groupby(['Customer Status', 'CLTV Category']).size().reset_index(name='Count')
        # Tính toán phần trăm khách hàng theo giới tính và trạng thái của khách hàng
        total_per_status = customer_count.groupby('Customer Status')['Count'].transform('sum')
        customer_count['Percentage'] = (customer_count['Count'] / total_per_status) * 100
        # Tạo biểu đồ cột ghép bằng Plotly Express
        fig = px.bar(customer_count, x='CLTV Category', y='Percentage', color='Customer Status',
                    barmode='group', text='Count', title='Số lượng khách hàng trong từng nhóm Điểm vòng đời khách hàng')
        # Hiển thị giá trị số lượng và phần trăm trên cột
        fig.update_traces(texttemplate='%{text:.0f}', textposition='inside')
        fig.update_yaxes(title_text="Phần trăm (%)")
        fig.update_xaxes(title_text="Nhóm khách hàng")
        # Cài đặt kích thước của biểu đồ
        fig.update_layout(width=550,height=400)
        # Hiển thị biểu đồ cột ghép trong Streamlit
        st.plotly_chart(fig)

                                        

