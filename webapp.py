import google.generativeai as genai
import os
import streamlit as st
from pdfextractor import text_extractor_pdf
from docxextractor import text_extractor_docx
from imageextractor import extract_text_image

# 🔑 Configure the model
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# 📂 Upload the file in sidebar
user_text = None
st.sidebar.title('📤 :orange[Upload your MOM notes here:]')
st.sidebar.subheader('📝 :blue[Please upload your MOM notes only in PDF, DOCX, or image format:]')
user_file = st.sidebar.file_uploader("📎 Upload a file", type=["pdf", "docx", "jpg", "jpeg", "png"])

if user_file is not None:
    if user_file.type == 'application/pdf':
        user_text = text_extractor_pdf(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = text_extractor_docx(user_file)
    elif user_file.type in ['image/jpeg', 'image/png', 'image/jpg']:
        user_text = extract_text_image(user_file)
    else:
        st.error("❌ Unsupported file type.")

# 🏠 Main page
st.title('📑 :blue[Extracted MOM Notes] :orange[— AI assisted MOM generator in a standardized format]')
tips = '''💡 **Tips to use this application:**
- 📂 Upload your meeting notes in **PDF, DOCX, or image** format from the sidebar.  
- ⚡ Click on the **"Generate MOM"** button to get the standardized MOM document.  
'''
st.write(tips)

# ▶️ Generate MOM button
if st.button("🚀 Generate MOM"):
    if user_text is None:
        st.error('⚠️ Text extraction failed and not generated. Please try again.')
    else:
        with st.spinner('⏳ Processing your data...'):
            prompt = f'''Assume you are expert in creating MOM (Minutes of Meeting). User has provided notes of the meeting in text format.
            Using this data you need to create a standardized minutes of meeting for the user. 
            The data provided by the user is as follows:
            {user_text}
            Keep the format strictly as mentioned below
            📌 Title : Title of Meeting
            📌 Heading : Meeting Agenda
            📌 Subheading : Name of Attendees (If attendees are not mentioned keep it N/A)
            📌 Subheading : Date and Place of the Meeting (place means name of the conference / meeting room. If not provided keep it Online.)
            
            📝 Body : The body must follow the sequence of the meeting discussion points.
            - Key points discussed  
            - Highlight any decisions that were finalized  
            - Mention actionable items  
            - Any additional notes or comments  
            - Any deadlines that were discussed  
            - Next meeting date (If not provided → N/A)  
            - 📌 2–3 line summary of the meeting  
            - ✅ Use bullet points for clarity and highlight important information/keywords.  

            The data provided by the user is as follows:
            {user_text}
            '''
            response = model.generate_content(prompt)
            mom_output = response.text

            st.subheader("📄 Generated MOM")
            st.write(mom_output)

            # 📥 Download button
            st.download_button(
                label="📥 Download MOM as Text",
                data=mom_output,
                file_name="minutes_of_meeting.txt",
                mime="text/plain"
            )
