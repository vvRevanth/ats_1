
import streamlit as st
import pandas as pd
import google.generativeai as genai
import PyPDF2 as pdf
import json
from pydataset import data

# Define your Google API Key
API_KEY = "AIzaSyD2oLQHkz9sYQvKZN6VaZ7ZI2t2N79wefQ"

# Function to configure Gemini AI model with the provided API key
def configure_gemini_api(api_key):
    genai.configure(api_key=api_key)

# Function to get response from Gemini AI
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Load job postings data
@st.cache_data
def load_job_postings():
    job_postings = pd.read_csv("job_postings.csv")
    return job_postings


# Add your contact information
def contact_us():
    st.markdown("<h2 id='contact'>Contact Us</h2>", unsafe_allow_html=True)
    st.write("""
        ## Contact Information
        Email: info@careernest.com
        Phone: +1 (123) 456-7890
        Address: 123 Career St, Dream City, USA
        """)

# Streamlit app configuration
st.set_page_config(layout="wide")
# Add home and contact buttons in the top right corner

col1, col2 = st.columns([1, 0.1])
with col1:
    if st.button("Home"):
        st.experimental_set_query_params(tab="home")
with col2:
    if st.button("Contact"):
        st.experimental_set_query_params(tab="contact")

st.title("Career Nest - Resume Checker")
tabs = ["home", "contact"]
# Main Banner

video_url = "https://drive.google.com/file/d/1YFHx0KYocweBYNTm_c1fIi0OZm-J3V59/preview"
iframe_code = f'<iframe src="{video_url}" width="640" height="480" allow="autoplay"></iframe>'

st.write(iframe_code, unsafe_allow_html=True)
st.write("""
    # Unlock more interview opportunities by optimizing your resume with Career Nest
    ## Find your dream career
    """)


# Add "Scan Your Resume" Button
if st.button("Scan Your Resume"):
    # Scroll to the "Submit Your Resume" section
    st.markdown("""<div id='submit'></div>""", unsafe_allow_html=True)

# Our Goals section
st.write("""
    ## Our Goals
    A job recommendation website streamlines job search by offering personalized, relevant job opportunities.
    It uses algorithms to match job seekers with employment options based on their qualifications, preferences, and career objectives.
    The website aims to deliver accurate job listings, ensure diversity across industries, and enhance user engagement through intuitive navigation and interactive features.
    It saves time and effort for job seekers, maximizing the likelihood of finding suitable employment options. It also prioritizes long-term career development by providing resources and networking opportunities. Monetization strategies like job postings and premium memberships sustain the website's operations.
    """)

# Our Work section
st.write("""
    ## Our Work
    Career Nest is a platform that uses advanced algorithms and data analytics to transform the job search process. It provides personalized job suggestions that match each user's skills, preferences, and career aspirations.
    The platform empowers job seekers of all backgrounds and experience levels to navigate the job market confidently, offering tools for resume building, interview preparation, networking, and career development.
    Career Nest is committed to accuracy and relevance, continuously refining its recommendation engine to ensure the delivery of the most suitable opportunities
    """)

# Our Passion section
st.write("""
    ## Our Passion
    Our career guidance platform is dedicated to assisting individuals in discovering their ideal career paths.
    Through a thoughtfully curated selection of images, we illustrate career achievements, personal growth, and networking opportunities. Our commitment to inclusivity ensures equal access to a diverse array of job opportunities spanning various industries.
    Embracing innovation and technology, our platform showcases cutting-edge tools and futuristic landscapes. With a mission to inspire and connect with users on their career journeys, our platform endeavors to empower individuals to pursue fulfilling and rewarding professional paths.
    """)

# Scanner Section
st.title("Resume Matcher ATS")

# Load job postings data
job_postings = load_job_postings()

# Filter job titles
selected_job_titles = st.multiselect("Select Job Titles", job_postings['title'].unique())
if not selected_job_titles:
    st.info("Please select at least one job title.")
    st.stop()

# Select Job Description Source
description_source = st.radio("Select Job Description Source:", ("From CSV File", "Enter Manually"))
selected_job_title = None
jd = None

if description_source == "From CSV File":
    selected_job_title = selected_job_titles[0]
    jd = job_postings[job_postings['title'] == selected_job_title]['description'].values[0]
elif description_source == "Enter Manually":
    jd = st.text_area("Enter Job Description:")

# Show job description for the selected job title
if jd is not None:
    st.subheader("Job Description:")
    st.write(jd)

# Submit Your Resume Section
st.markdown("<h2 id='submit'>Submit Your Resume</h2>", unsafe_allow_html=True)

# Streamlit app
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input_prompt = f"""
        Hey Act Like a skilled or very experienced ATS (Application Tracking System)
        with a deep understanding of the tech field, software engineering, data science, data analyst
        and big data engineering. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive and you should provide the 
        best assistance for improving the resumes. Assign the percentage Matching based 
        on JD and the missing keywords with high accuracy.
        resume:{text}
        description:{jd}
        
        I want the response in one single string having the structure
        {{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
        """
        configure_gemini_api(API_KEY)
        response = get_gemini_response(input_prompt)
        st.subheader("Response:")
        parsed_response = json.loads(response)
        for key, value in parsed_response.items():
            st.write(f"**{key}:** {value}")

# Reasoning Section
st.write("""
    # Why Use Resume Check?
    Resume checking is a crucial step in the recruitment process, enabling recruiters to efficiently identify qualified candidates, reduce bias, and focus on
    relevant candidates. Automated systems filter resumes based on keywords, skills, experience, and qualifications, reducing
    human error and bias. They also maintain objectivity by applying predefined criteria uniformly to all applicants, ensuring fair
    consideration. This time-saving tool allows recruiters to prioritize their review process and engage with promising candidates. Additionally,
    it enhances the candidate experience by providing quicker feedback and ensuring
    compliance with legal and organizational policies.
    """)

# Call to Action
st.write("""
    # Send Us a Message
    "Innovation. Excellence. Your satisfaction, our priority.
""")


















'''import streamlit as st
import pandas as pd
import google.generativeai as genai
import PyPDF2 as pdf
import json

# Define your Google API Key
API_KEY = "AIzaSyD2oLQHkz9sYQvKZN6VaZ7ZI2t2N79wefQ"

# Function to configure Gemini AI model with the provided API key
def configure_gemini_api(api_key):
    genai.configure(api_key=api_key)

# Function to get response from Gemini AI
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Load job postings data
@st.cache_data
def load_job_postings():
    job_postings = pd.read_csv("ResumeMatcher-ATS-main/data/job_p.csv")
    return job_postings


# Add your contact information
def contact_us():
    st.markdown("<h2 id='contact'>Contact Us</h2>", unsafe_allow_html=True)
    st.write("""
        ## Contact Information
        Email: info@careernest.com
        Phone: +1 (123) 456-7890
        Address: 123 Career St, Dream City, USA
        """)

# Streamlit app configuration
st.set_page_config(layout="wide")
# Add home and contact buttons in the top right corner

col1, col2 = st.columns([1, 0.1])
with col1:
    if st.button("Home"):
        st.experimental_set_query_params(tab="home")
with col2:
    if st.button("Contact"):
        st.experimental_set_query_params(tab="contact")

st.title("Career Nest - Resume Checker")
tabs = ["home", "contact"]
# Main Banner
#st.video('video.mp4')
st.write("""
    # Unlock more interview opportunities by optimizing your resume with Career Nest
    ## Find your dream career
    """)
# Add "Scan Your Resume" Button
if st.button("Scan Your Resume"):
    # Scroll to the "Submit Your Resume" section
    st.markdown("""<div id='submit'></div>""", unsafe_allow_html=True)

# Our Goals section
st.write("""
    ## Our Goals
    A job recommendation website streamlines job search by offering personalized, relevant job opportunities.
    It uses algorithms to match job seekers with employment options based on their qualifications, preferences, and career objectives.
    The website aims to deliver accurate job listings, ensure diversity across industries, and enhance user engagement through intuitive navigation and interactive features.
    It saves time and effort for job seekers, maximizing the likelihood of finding suitable employment options. It also prioritizes long-term career development by providing resources and networking opportunities. Monetization strategies like job postings and premium memberships sustain the website's operations.
    """)

# Our Work section
st.write("""
    ## Our Work
    Career Nest is a platform that uses advanced algorithms and data analytics to transform the job search process. It provides personalized job suggestions that match each user's skills, preferences, and career aspirations.
    The platform empowers job seekers of all backgrounds and experience levels to navigate the job market confidently, offering tools for resume building, interview preparation, networking, and career development.
    Career Nest is committed to accuracy and relevance, continuously refining its recommendation engine to ensure the delivery of the most suitable opportunities
    """)

# Our Passion section
st.write("""
    ## Our Passion
    Our career guidance platform is dedicated to assisting individuals in discovering their ideal career paths.
    Through a thoughtfully curated selection of images, we illustrate career achievements, personal growth, and networking opportunities. Our commitment to inclusivity ensures equal access to a diverse array of job opportunities spanning various industries.
    Embracing innovation and technology, our platform showcases cutting-edge tools and futuristic landscapes. With a mission to inspire and connect with users on their career journeys, our platform endeavors to empower individuals to pursue fulfilling and rewarding professional paths.
    """)

# Scanner Section
st.title("Resume Matcher ATS")

# Load job postings data
job_postings = load_job_postings()

# Filter job titles
selected_job_titles = st.multiselect("Select Job Titles", job_postings['title'].unique())
if not selected_job_titles:
    st.info("Please select at least one job title.")
    st.stop()

# Select Job Description Source
description_source = st.radio("Select Job Description Source:", ("From CSV File", "Enter Manually"))
selected_job_title = None
jd = None

if description_source == "From CSV File":
    selected_job_title = selected_job_titles[0]
    jd = job_postings[job_postings['title'] == selected_job_title]['description'].values[0]
elif description_source == "Enter Manually":
    jd = st.text_area("Enter Job Description:")

# Show job description for the selected job title
if jd is not None:
    st.subheader("Job Description:")
    st.write(jd)

# Submit Your Resume Section
st.markdown("<h2 id='submit'>Submit Your Resume</h2>", unsafe_allow_html=True)

# Streamlit app
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input_prompt = f"""
        Hey Act Like a skilled or very experienced ATS (Application Tracking System)
        with a deep understanding of the tech field, software engineering, data science, data analyst
        and big data engineering. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive and you should provide the 
        best assistance for improving the resumes. Assign the percentage Matching based 
        on JD and the missing keywords with high accuracy.
        resume:{text}
        description:{jd}
        
        I want the response in one single string having the structure
        {{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
        """
        configure_gemini_api(API_KEY)
        response = get_gemini_response(input_prompt)
        st.subheader("Response:")
        parsed_response = json.loads(response)
        for key, value in parsed_response.items():
            st.write(f"**{key}:** {value}")

# Reasoning Section
st.write("""
    # Why Use Resume Check?
    Resume checking is a crucial step in the recruitment process, enabling recruiters to efficiently identify qualified candidates, reduce bias, and focus on
    relevant candidates. Automated systems filter resumes based on keywords, skills, experience, and qualifications, reducing
    human error and bias. They also maintain objectivity by applying predefined criteria uniformly to all applicants, ensuring fair
    consideration. This time-saving tool allows recruiters to prioritize their review process and engage with promising candidates. Additionally,
    it enhances the candidate experience by providing quicker feedback and ensuring
    compliance with legal and organizational policies.
    """)

# Call to Action
st.write("""
    # Send Us a Message
    "Innovation. Excellence. Your satisfaction, our priority.
""")
'''
