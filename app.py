import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

# Configure Google Generative AI API key
genai.configure(api_key=("AIzaSyAZarp2Q0239gRowkUdvgH1D9j_lztDAI0"))

# Load YouTube API Key
YOUTUBE_API_KEY = ("AIzaSyBVoLBRlr2K-IV9q21SoQk7eUf6CKVWQec")

interest_to_jobs = {
    'Technology': ['Software Developer', 'Data Scientist', 'Cybersecurity Analyst', 'UX/UI Designer', 'Artificial Intelligence Engineer', 'Cloud Architect', 'DevOps Engineer', 'Mobile App Developer', 'Quality Assurance Engineer', 'Network Engineer', 'Game Developer', 'Blockchain Developer', 'Machine Learning Engineer', 'Web Developer', 'Database Administrator'],
    'Healthcare': ['Registered Nurse', 'Medical Technologist', 'Physician Assistant', 'Pharmacist', 'Physical Therapist', 'Occupational Therapist', 'Speech-Language Pathologist', 'Nurse Practitioner', 'Medical Doctor (MD)', 'Radiologic Technologist', 'Dental Hygienist', 'Respiratory Therapist', 'Emergency Medical Technician (EMT)', 'Clinical Research Coordinator', 'Medical Laboratory Technician'],
    'Business': ['Marketing Specialist', 'Financial Analyst', 'Human Resources Manager', 'Operations Manager', 'Business Development Manager', 'Management Consultant', 'Supply Chain Manager', 'Risk Analyst', 'Project Manager', 'Data Analyst', 'Entrepreneur', 'Sales Manager', 'Accountant', 'Market Research Analyst', 'Logistics Coordinator'],
    'Education': ['Teacher', 'School Counselor', 'Education Administrator', 'Curriculum Developer', 'Special Education Teacher', 'Educational Psychologist', 'Instructional Designer', 'School Principal', 'Librarian', 'Educational Technologist', 'Admissions Counselor', 'Career Counselor', 'Academic Advisor', 'Student Affairs Coordinator', 'Online Course Developer'],
    'Engineering': ['Mechanical Engineer', 'Information Technology', 'Electrical Engineer', 'Civil Engineer', 'Aerospace Engineer', 'Chemical Engineer', 'Industrial Engineer', 'Environmental Engineer', 'Petroleum Engineer', 'Structural Engineer', 'Robotics Engineer'],
    'Finance': ['Investment Banker', 'Financial Advisor', 'Portfolio Manager', 'Actuary', 'Financial Controller', 'Credit Analyst', 'Treasury Analyst', 'Equity Research Analyst', 'Hedge Fund Manager', 'Insurance Underwriter'],
    'Creative Arts': ['Graphic Designer', 'Animator', 'Illustrator', 'Art Director', 'Creative Director', 'Film Director', 'Musician', 'Photographer', 'Copywriter', 'Content Creator'],
    'Science': ['Biologist', 'Chemist', 'Physicist', 'Environmental Scientist', 'Geologist', 'Marine Biologist', 'Astronomer', 'Epidemiologist', 'Pharmacologist', 'Neuroscientist'],
    'Hospitality and Tourism': ['Hotel Manager', 'Event Planner', 'Travel Agent', 'Tour Guide', 'Concierge', 'Restaurant Manager', 'Cruise Director', 'Resort Manager', 'Food and Beverage Manager', 'Hospitality Consultant']
}

def get_recommended_videos(query, max_results=3):
    """Fetch recommended YouTube videos dynamically based on user interest."""
    if not YOUTUBE_API_KEY:
        return []

    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q=f"{query} career guidance",
            part="snippet",
            maxResults=max_results,
            type="video"
        ).execute()

        video_links = [
            f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            for item in search_response.get("items", [])
        ]
        return video_links
    except Exception as e:
        if 'quotaExceeded' in str(e):
            st.error("YouTube API quota exceeded. Please try again later.")
        else:
            st.error(f"Error fetching videos: {e}")
        return []

def generate_roadmap(selected_job, current_stage):
    try:
        prompt = f"Create a detailed step-by-step roadmap for becoming a {selected_job}, starting from the {current_stage} stage. Include key educational requirements, skills to develop, certifications, and career progression steps."

        model = genai.GenerativeModel('gemini-pro') 
        response = model.generate_content(prompt)

        roadmap_text = response.text
        roadmap_with_headings = f"**Roadmap to Become a {selected_job}**\n\n"
        roadmap_with_headings += f"**Current Stage:** {current_stage}\n\n"
        roadmap_with_headings += "**Personalized Roadmap:**\n"
        roadmap_with_headings += roadmap_text

        return roadmap_with_headings
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def estimate_time_to_achieve(current_stage):
    time_estimations = {
        'High School': '4-6 years',
        'College': '2-4 years',
        'Entry-Level Professional': '1-3 years',
        'Mid-Level Professional': '3-5 years',
        'Senior Professional': '5+ years'
    }
    return time_estimations.get(current_stage, 'Unknown')

def main():
    st.set_page_config(page_title="Career Guidance Project", page_icon=":mortar_board:", layout="wide")

    st.title('Career Guidance')

    page = st.sidebar.radio("Navigation", ["Select Area of Interest", "Select Job", "Current Stage Details"])

    # Dynamic video section based on selected interest
    st.sidebar.markdown("### Top Career-Related Videos")
    
    area_of_interest = st.session_state.get('area_of_interest', None)
    video_query = area_of_interest if area_of_interest else "career guidance"
    video_links = get_recommended_videos(video_query)
    
    for link in video_links:
        st.sidebar.video(link)

    if page == "Select Area of Interest":
        area_of_interest = st.selectbox('Area of Interest', list(interest_to_jobs.keys()))
        if area_of_interest:
            st.session_state['area_of_interest'] = area_of_interest
            st.sidebar.radio("Navigation", ["Select Job", "Current Stage Details"])

    elif page == "Select Job":
        suggested_jobs = interest_to_jobs.get(st.session_state.get('area_of_interest', ''), [])
        job_chunks = [suggested_jobs[i:i+4] for i in range(0, len(suggested_jobs), 4)]
        for chunk in job_chunks:
            cols = st.columns(len(chunk))
            for col, job in zip(cols, chunk):
                if col.button(job, key=job):
                    st.session_state['selected_job'] = job
                    st.sidebar.radio("Navigation", ["Current Stage Details"])

    elif page == "Current Stage Details":
        selected_job = st.session_state.get('selected_job', None)
        if selected_job:
            st.subheader(f'Selected Job: {selected_job}')
            current_stage = st.selectbox('Current Stage', ['High School', 'College', 'Entry-Level Professional', 'Mid-Level Professional', 'Senior Professional'])
            if st.button('Generate Roadmap'):
                roadmap = generate_roadmap(selected_job, current_stage)
                if roadmap:
                    st.write("Roadmap:")
                    st.markdown(roadmap, unsafe_allow_html=True)
                    st.write(f"Estimated time to achieve: {estimate_time_to_achieve(current_stage)}")
                else:
                    st.warning("Roadmap could not be generated.")
        else:
            st.write("Please select a job first from the 'Select Job' page.")

if __name__ == "__main__":
    main()