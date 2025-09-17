import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt

# Configure the model 
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = 'AIzaSyCA2uu5GaTNoNUXeelsTv0G4rgzzjRL_Zs')
model = genai.GenerativeModel('gemini-2.5-flash-lite')

st.sidebar.title(':red[UPLOAD YOUR IMAGE HERE]')
uploaded_image = st.sidebar.file_uploader('Here',type = ['jpeg','jpg','png'])
if uploaded_image:
        image = Image.open(uploaded_image)
        st.sidebar.subheader(':blue[UPLOADED IMAGE]')
        st.sidebar.image(image)

# Create main page
st.title(':orange[STRUCTURAL DEFECTS] : :green[AI Assisted structural defect identifier in construction business]')
tips = '''To use the application follow the steps below:
* Upload the image
* Click on the button to generate summary
* Click download to save the report generated'''
st.write(tips)

rep_title = st.text_input('Report Title:',None)
prep_by = st.text_input('Report Prepared by:',None)
prep_for = st.text_input('Report prepare for:',None)

prompt = f''' Assume you are a structural engineer. The user has provided an image of a structure.
You need to identify the structural defects in the image and generate a report.
The report should contail the following:

It should start with the title, prepared by and prepared for details, Provided by user.
Use {rep_title} as title, {prep_by} as prepared by, {prep_for} as prepared for the same.
also mention current date from {dt.datetime.now().date()}.

* Identify and classify the defect for eg.: crack, spalling, corrosion, honeycombing, etc.
* There could more than one defects in the image. Identify all the defects seperately.
* For each defect identified, provide a short description of the defect and its potential impact on the structure.
* For each measure the severity of the defect as low, medium or high. Also mention if the defect is inevitable or avoidable.
* Also mention the time before  this defect leads to permament damage to the structure.
* Provide a short term and long term solution along with their estimated cost in indian rupees and time to implement.
* What precautionary measures can be taken to avoid such defects in future.
* The report generated should be in the word format.
* show the data in bullet points and tabular format wherever possible.
* Make sure that the report does not exceeds 3 pages. '''

if st.button('Generate Report'):
        if uploaded_image is None:
            st.error('Please upload an image first')
        else:
            with st.spinner('Generating Report...'):
                response = model.generate_content([prompt,image],generation_config={'temperature':0.5})
                st.write(response.text)
        
            st.download_button(
                label='Download Report',
                data = response.text,
                file_name='structural_defect_report.txt',
                mime = 'text/plain')