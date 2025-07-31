import streamlit as st
import sqlite3
import pandas as pd
from typing import List, Dict, Tuple, Optional

class PlacementDashboard:
    def __init__(self):
        self.initialize_page_config()
        self.db_connection = sqlite3.connect("placement.db")
        
    def initialize_page_config(self):
        """Initialize Streamlit page configuration"""
        st.set_page_config(
            page_title="Placement Dashboard",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.title("Placement Eligibility Checker")
    
    def run_query(self, query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        return pd.read_sql_query(query, self.db_connection, params=params)
    
    def display_criteria_section(self) -> Dict:
        """Display and collect placement criteria from user"""
        criteria = {}
        
        with st.expander("Set Placement Eligibility Criteria", expanded=True):
            # Programming Skills Criteria
            col1, col2, col3 = st.columns(3)
            with col1:
                criteria['problems_solved'] = st.slider(
                    "Minimum Problems Solved", 0, 200, 50, 
                    help="Number of coding problems solved"
                )
            with col2:
                criteria['assessments'] = st.slider(
                    "Minimum Assessments Completed", 0, 10, 3, 
                    help="Technical assessments completed"
                )
            with col3:
                criteria['project_score'] = st.slider(
                    "Minimum Latest Project Score", 0, 100, 70, 
                    help="Score out of 100 for latest project"
                )

            # Soft Skills Criteria
            col4, col5, col6 = st.columns(3)
            with col4:
                criteria['communication'] = st.slider(
                    "Minimum Communication Score", 0, 100, 70
                )
            with col5:
                criteria['teamwork'] = st.slider(
                    "Minimum Teamwork Score", 0, 100, 70
                )
            with col6:
                criteria['presentation'] = st.slider(
                    "Minimum Presentation Score", 0, 100, 70
                )

            # Placement Criteria
            col7, col8 = st.columns(2)
            with col7:
                criteria['mock_score'] = st.slider(
                    "Minimum Mock Interview Score", 0, 100, 60
                )
            with col8:
                criteria['internships'] = st.slider(
                    "Minimum Internships Completed", 0, 5, 1
                )
        
        return criteria
    
    def get_eligible_students(self, criteria: Dict) -> pd.DataFrame:
        """Query database for students matching the criteria"""
        query = '''
        SELECT s.student_id, s.name, s.email, p.problems_solved, p.assessments_completed, 
               p.latest_project_score, ss.communication, ss.teamwork, ss.presentation, 
               pl.mock_interview_score, pl.internships_completed
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE 
            p.problems_solved >= ? AND
            p.assessments_completed >= ? AND
            p.latest_project_score >= ? AND
            ss.communication >= ? AND
            ss.teamwork >= ? AND
            ss.presentation >= ? AND
            pl.mock_interview_score >= ? AND
            pl.internships_completed >= ?
        '''
        return self.run_query(query, tuple(criteria.values()))
    
    def display_eligible_students(self, df: pd.DataFrame):
        """Display results of eligible students"""
        if not df.empty:
            st.success(f" {len(df)} student(s) match your criteria!")
            st.dataframe(df.style.highlight_max(axis=0))
            
            st.download_button(
                label="Download Eligible Students Data",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='eligible_students.csv',
                mime='text/csv'
            )
        else:
            st.warning("No students found matching the criteria.")
    
    def display_analytics_tabs(self):
        """Display various analytics tabs"""
        st.markdown("## Placement Analytics")
        
        with st.container():
            tabs = st.tabs([
                " Avg Problems", " Top Students", " Soft Skills", 
                " Mock Scores", " Top Packages", " Internships", 
                " Batch Skills", " Certifications", " Interview Rounds", " City Stats"
            ])
            
            self.display_tab_content(tabs)
    
    def display_tab_content(self, tabs: List):
        """Display content for each analytics tab"""
        with tabs[0]:
            st.caption("Average coding problems solved by each batch")
            df = self.run_query("""
                SELECT course_batch, AVG(problems_solved) AS avg_problems_solved
                FROM programming
                JOIN students ON programming.student_id = students.student_id
                GROUP BY course_batch;
            """)
            st.dataframe(df)

        with tabs[1]:
            st.caption("Top 5 students marked as 'Ready' for placements")
            df = self.run_query("""
                SELECT s.name, p.mock_interview_score, p.placement_status
                FROM students s
                JOIN placements p ON s.student_id = p.student_id
                WHERE p.placement_status = 'Ready'
                ORDER BY p.mock_interview_score DESC
                LIMIT 5;
            """)
            st.dataframe(df)

        with tabs[2]:
            st.caption("Distribution of soft skills across all students")
            df = self.run_query("""
                SELECT communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills
                FROM soft_skills;
            """)
            st.dataframe(df)

        with tabs[3]:
            st.caption("Average mock interview scores by graduation year")
            df = self.run_query("""
                SELECT graduation_year, AVG(mock_interview_score) AS avg_mock_score
                FROM placements
                JOIN students ON placements.student_id = students.student_id
                GROUP BY graduation_year;
            """)
            st.dataframe(df)

        with tabs[4]:
            st.caption("Highest placement packages achieved")
            df = self.run_query("""
                SELECT s.name, p.company_name, p.placement_package
                FROM placements p
                JOIN students s ON s.student_id = p.student_id
                WHERE p.placement_status = 'Placed'
                ORDER BY p.placement_package DESC
                LIMIT 5;
            """)
            st.dataframe(df)

        with tabs[5]:
            st.caption("Average internships completed by batch")
            df = self.run_query("""
                SELECT course_batch, AVG(internships_completed) AS avg_internships
                FROM placements
                JOIN students ON placements.student_id = students.student_id
                GROUP BY course_batch;
            """)
            st.dataframe(df)

        with tabs[6]:
            st.caption("Average soft skills scores by batch")
            df = self.run_query("""
                SELECT course_batch,
                       AVG(communication) AS avg_communication,
                       AVG(teamwork) AS avg_teamwork,
                       AVG(presentation) AS avg_presentation
                FROM soft_skills
                JOIN students ON soft_skills.student_id = students.student_id
                GROUP BY course_batch;
            """)
            st.dataframe(df)

        with tabs[7]:
            st.caption("Certifications earned per student")
            df = self.run_query("""
                SELECT s.name, SUM(certifications_earned) AS total_certifications
                FROM programming
                JOIN students s ON programming.student_id = s.student_id
                GROUP BY s.student_id
                ORDER BY total_certifications DESC;
            """)
            st.dataframe(df)

        with tabs[8]:
            st.caption("Students who cleared more than 3 interview rounds")
            df = self.run_query("""
                SELECT s.name, p.interview_rounds_cleared
                FROM placements p
                JOIN students s ON s.student_id = p.student_id
                WHERE interview_rounds_cleared > 3;
            """)
            st.dataframe(df)

        with tabs[9]:
            st.caption("Student distribution by city")
            df = self.run_query("""
                SELECT city, COUNT(*) AS total_students
                FROM students
                GROUP BY city;
            """)
            st.dataframe(df)
    
    def run(self):
        """Main method to run the dashboard"""
        criteria = self.display_criteria_section()
        
        if st.button("Show Eligible Students", type="primary"):
            df = self.get_eligible_students(criteria)
            self.display_eligible_students(df)
        
        self.display_analytics_tabs()
        self.db_connection.close()

if __name__ == "__main__":
    dashboard = PlacementDashboard()
    dashboard.run()