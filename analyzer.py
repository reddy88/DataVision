import pandas as pd 
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import io
import base64

st.set_page_config(
    page_title='DataVision',
    page_icon='📊'
)

st.title(':rainbow[DataVision]')
st.subheader(':gray[Drop your Data—-Visualized and Analyzed in Seconds]', divider = 'rainbow')

file = st.file_uploader('Drop csv or excel file',type=['csv','xlsx'])
if file is not None:
    if file.name.endswith('csv'):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)   
    
    st.dataframe(data)
    st.info('File is successfully Uploaded',icon='🚨')

    st.subheader(':rainbow[Basic information of the dataset]')
    tab1,tab2,tab3,tab4 = st.tabs(['Summary','Top and Bottom Rows','Data Types','Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and  {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statistical summary of the dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))
    with tab3:
        st.subheader(':grey[Data types of column]')
        st.dataframe(data.dtypes)
    with tab4:
        st.subheader('Column Names in Dataset')
        st.write(list(data.columns))
    
    st.subheader(':rainbow[Column Values To Count]')
    with st.expander('Value Count'):
        col1,col2 = st.columns(2)
        with col1:
          column  = st.selectbox('Choose Column name',options=list(data.columns))
        with col2:
            toprows = st.number_input('Top rows',min_value=1,step=1)
        
        count = st.button('Count')
        if count:
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='gray')
            fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)

    st.subheader(':rainbow[Groupby : Simplify your data analysis]')
    st.write('The groupby lets you summarize data by specific categories and groups')
    with st.expander('Group By your columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your column to groupby',options = list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation',options=list(data.columns))
        with col3:
            operation = st.selectbox('Choose operation',options=['sum','max','min','mean','median','count'])
        
        if groupby_cols:
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_col,operation)
            ).reset_index()

            st.dataframe(result)

            st.subheader(':gray[Data Visualization]')
            graphs = st.selectbox('Choose your graphs',options=['line','bar','scatter','pie','sunburst'])
            if graphs=='line':
                x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Color Information',options= [None] +list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif graphs=='bar':
                 x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                 y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                 color = st.selectbox('Color Information',options= [None] +list(result.columns))
                 facet_col = st.selectbox('Column Information',options=[None] +list(result.columns))
                 fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                 st.plotly_chart(fig)
            elif graphs=='scatter':
                x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Color Information',options= [None] +list(result.columns))
                size = st.selectbox('Size Column',options=[None] + list(result.columns))
                fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
                st.plotly_chart(fig)
            elif graphs=='pie':
                values = st.selectbox('Choose Numerical Values',options=list(result.columns))
                names = st.selectbox('Choose labels',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)
            elif graphs=='sunburst':
                path = st.multiselect('Choose your Path',options=list(result.columns))
                fig = px.sunburst(data_frame=result,path=path,values='newcol')
                st.plotly_chart(fig)

    st.subheader(':rainbow[Data Filtering]')
    with st.expander('Filter your data'):
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_column = st.selectbox('Select column to filter', options=list(data.columns))
        with col2:
            filter_operation = st.selectbox('Select filter operation', options=['==', '!=', '>', '<', '>=', '<='])
        with col3:
            filter_value = st.text_input('Enter filter value')
        
        apply_filter = st.button('Apply Filter')
        
        if apply_filter:
            try:
                if filter_operation == '==':
                    filtered_data = data[data[filter_column] == filter_value]
                elif filter_operation == '!=':
                    filtered_data = data[data[filter_column] != filter_value]
                elif filter_operation == '>':
                    filtered_data = data[data[filter_column] > float(filter_value)]
                elif filter_operation == '<':
                    filtered_data = data[data[filter_column] < float(filter_value)]
                elif filter_operation == '>=':
                    filtered_data = data[data[filter_column] >= float(filter_value)]
                elif filter_operation == '<=':
                    filtered_data = data[data[filter_column] <= float(filter_value)]
                
                st.write(f"Filtered data shape: {filtered_data.shape}")
                st.dataframe(filtered_data)
                
                data = filtered_data
            except Exception as e:
                st.error(f"Error applying filter: {str(e)}")

    st.subheader(':rainbow[Time Series Analysis]')
    with st.expander('Analyze Time Series Data'):
        date_columns = data.select_dtypes(include=['datetime64']).columns
        if len(date_columns) > 0:
            date_column = st.selectbox('Select date column', options=date_columns)
            value_column = st.selectbox('Select value column', options=data.select_dtypes(include=['float64', 'int64']).columns)
            
            if st.button('Generate Time Series Plot'):
                fig = px.line(data, x=date_column, y=value_column)
                st.plotly_chart(fig)
        else:
            st.write('No datetime columns found in the dataset.')

    st.subheader(':rainbow[Correlation Matrix]')
    with st.expander('View Correlation Matrix'):
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_columns) > 0:
            corr_matrix = data[numeric_columns].corr()
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='Viridis'
            ))
            fig.update_layout(title='Correlation Matrix')
            st.plotly_chart(fig)
        else:
            st.write('No numeric columns found in the dataset.')

    st.subheader(':rainbow[Data Export]')
    with st.expander('Export Data'):
        export_format = st.selectbox('Select export format', options=['CSV', 'Excel', 'JSON'])
        if st.button('Export Data'):
            if export_format == 'CSV':
                csv = data.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="exported_data.csv">Download CSV File</a>'
            elif export_format == 'Excel':
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    data.to_excel(writer, sheet_name='Sheet1', index=False)
                b64 = base64.b64encode(output.getvalue()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="exported_data.xlsx">Download Excel File</a>'
            else:  
                json = data.to_json(orient='records')
                b64 = base64.b64encode(json.encode()).decode()
                href = f'<a href="data:file/json;base64,{b64}" download="exported_data.json">Download JSON File</a>'
            
            st.markdown(href, unsafe_allow_html=True)

    st.subheader(':rainbow[Custom Calculations]')
    with st.expander('Perform Custom Calculations'):
        custom_formula = st.text_input('Enter custom formula (e.g., A + B * 2)')
        if st.button('Apply Custom Calculation'):
            try:
                result = data.eval(custom_formula)
                st.write('Result of custom calculation:')
                st.dataframe(result)
                
                if st.button('Add as New Column'):
                    new_column_name = st.text_input('Enter new column name')
                    if new_column_name:
                        data[new_column_name] = result
                        st.write('Updated dataset:')
                        st.dataframe(data)
            except Exception as e:
                st.error(f"Error in custom calculation: {str(e)}")

