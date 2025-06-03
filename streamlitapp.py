import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# function for Button's Click Action 
def click_button():
    st.session_state.clicked = True

# SQL Connection
try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',  # Corrected from 'username'
        password='NewStart2025',
        database='guvi'
    )
    mycursor = connection.cursor()
except Error as e:
    st.error(f"Error connecting to MySQL: {e}")

# Streamlit UI Section 1
st.title("Placement Eligibility Application")
st.header("Eligible Students Based on Criteria")
st.sidebar.header("Placement Details")
st.markdown("🎓 ** The Placement Eligibility Application is a digital form used by students to apply for participation in campus recruitment drives. It ensures that applicants meet academic and institutional criteria before being considered for placement opportunities **")

status = ['Ready', 'Not Ready', 'Placed']
choice = st.sidebar.selectbox("Select the status", options=status, index=1)
placement_date = st.sidebar.date_input('Pick a date')

# Streamlit UI Section 2

st.sidebar.header("Set Placement Eligibility Criteria")
problems_solved = st.sidebar.slider("Problems solved", 1, 140)
latest_project_score = st.sidebar.number_input("Latest project score", 15, 210)
softskill = st.sidebar.number_input("Soft skills score", 20, 500)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False
st.sidebar.button('Submit', on_click=click_button)

if connection.is_connected():
        try:
            st.success("SQL Connected")

            # Query the database
            query = f"""
                SELECT 
                    s.Student_id,
                    s.Name,
                    s.Email,
                    pl.mock_interview_score AS InterviewScore,
                    pl.internships_completed AS '#Internship',
                    pl.interview_rounds_cleared AS '#InterviewRounds',
                    pl.company_name,
                    pl.placement_package AS 'Package',
                    pl.placement_date,
                    p.Mini_projects AS '#MiniProjects',
                    (ss.communication + ss.critical_thinking + ss.interpersonal_skills + ss.presentation) AS softskillscore,
                    pl.placement_status,
                    RANK() OVER (ORDER BY pl.placement_package DESC) AS placementrank
                FROM placementeligibility.placements pl
                INNER JOIN placementeligibility.students s ON pl.student_id = s.Student_id
                INNER JOIN placementeligibility.programming p ON p.student_id = s.Student_id
                INNER JOIN placementeligibility.softskills ss ON ss.student_id = s.Student_id
                WHERE pl.placement_status = %s AND pl.placement_date >= %s;
            """
            mycursor.execute(query, (choice,placement_date,))
            result = mycursor.fetchall()

            final_columns = [
                'Student_id', 'Name', 'Email', 'InterviewScore',
                '#Internship', '#InterviewRounds','CompanyName' ,'Package',
                'placement_date', '#MiniProjects', 'softskillscore',
                'placement_status', 'placementrank'
            ]

            result_df = pd.DataFrame(result, columns=final_columns)
            st.write("Here are the students Placement status:")
            st.table(result_df)
        except Error as e:
            st.error(f"MySQL Query Error: {e}")


if st.session_state.clicked:
    # Create a dictionary with the input data
    searchdata = {
        'problems_solved': problems_solved,
        'latest_project_score': latest_project_score,
        'softskill': softskill
    }
    df = pd.DataFrame([searchdata])

    #Execute Query 2 on submit button click

    if connection.is_connected():
        print("SQL Connected")
        #cursor.execute("SELECT * FROM orderdetails where Quantity = df['latest_project_score'];")
        mycursor.execute(f"SELECT s.student_id,s.name,p.Language,Problems_solved,Assessments_completed,Mini_projects,Certifications_earned,Latest_project_score,communication+teamwork+presentation+leadership+critical_thinking+interpersonal_skills as TotalSoftSkillscore  FROM placementeligibility.programming p  inner join  placementeligibility.softskills ss on ss.Student_id =p.Student_id  inner join placementeligibility.students s on s.Student_id =ss.Student_id where  problems_solved >='{problems_solved}' and Latest_project_score >='{latest_project_score}' and Problems_solved >='{softskill}' ;")
        result = mycursor.fetchall()
        final_columns = [
                'Student_id', 'Name', 'Language', 'Problems_solved',
                'Assessments_completed', 'Mini_projects','Certifications_earned' ,'Latest_project_score',
                'TotalSoftSkillscore'
            ]  
        # Create Dataframe
        Result_df = pd.DataFrame(result, columns=final_columns)
        st.write("Here are the Students Placement Eligibility details:")
        st.table(Result_df)