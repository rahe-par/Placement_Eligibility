from faker import Faker
import sqlite3
import random

class StudentDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.conn = None
        self.cursor = None
        
    def initialize_database(self):
        """Initialize the database connection and create tables"""
        self.conn = sqlite3.connect('placement.db')
        self.cursor = self.conn.cursor()
        self._create_tables()
        
    def _create_tables(self):
        """Create all necessary tables in the database"""
        self._create_students_table()
        self._create_programming_table()
        self._create_soft_skills_table()
        self._create_placements_table()
        
    def _create_students_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT,
            phone TEXT,
            enrollment_year INTEGER,
            course_batch TEXT,
            city TEXT,
            graduation_year INTEGER
        )
        ''')
    
    def _create_programming_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS programming (
            programming_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            language TEXT,
            problems_solved INTEGER,
            assessments_completed INTEGER,
            mini_projects INTEGER,
            certifications_earned INTEGER,
            latest_project_score INTEGER,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
        ''')
    
    def _create_soft_skills_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS soft_skills (
            soft_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            communication INTEGER,
            teamwork INTEGER,
            presentation INTEGER,
            leadership INTEGER,
            critical_thinking INTEGER,
            interpersonal_skills INTEGER,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
        ''')
    
    def _create_placements_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS placements (
            placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            mock_interview_score INTEGER,
            internships_completed INTEGER,
            placement_status TEXT,
            company_name TEXT,
            placement_package INTEGER,
            interview_rounds_cleared INTEGER,
            placement_date TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
        ''')
    
    def generate_student(self):
        """Generate a single student record with all related data"""
        # Insert student data
        self.cursor.execute('''
        INSERT INTO students (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.fake.name(),
            random.randint(18, 25),
            random.choice(['Male', 'Female', 'Other']),
            self.fake.email(),
            self.fake.phone_number(),
            random.randint(2018, 2022),
            random.choice(['Batch A', 'Batch B']),
            self.fake.city(),
            random.randint(2022, 2025)
        ))
        student_id = self.cursor.lastrowid
        
        # Generate programming skills
        self._generate_programming_data(student_id)
        
        # Generate soft skills
        self._generate_soft_skills_data(student_id)
        
        # Generate placement data
        self._generate_placement_data(student_id)
        
    def _generate_programming_data(self, student_id):
        self.cursor.execute('''
        INSERT INTO programming (student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            random.choice(['Python', 'SQL', 'Java']),
            random.randint(20, 150),
            random.randint(1, 10),
            random.randint(0, 5),
            random.randint(0, 3),
            random.randint(50, 100)
        ))
    
    def _generate_soft_skills_data(self, student_id):
        self.cursor.execute('''
        INSERT INTO soft_skills (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            random.randint(40, 100),
            random.randint(40, 100),
            random.randint(40, 100),
            random.randint(40, 100),
            random.randint(40, 100),
            random.randint(40, 100)
        ))
    
    def _generate_placement_data(self, student_id):
        self.cursor.execute('''
        INSERT INTO placements (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            random.randint(30, 100),
            random.randint(0, 3),
            random.choice(['Ready', 'Not Ready', 'Placed']),
            self.fake.company() if random.choice([True, False]) else None,
            random.randint(300000, 1500000),
            random.randint(1, 5),
            self.fake.date_this_decade().isoformat()
        ))
    
    def generate_sample_data(self, count=100):
        """Generate multiple student records"""
        for _ in range(count):
            self.generate_student()
        self.conn.commit()
    
    def close_connection(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

# Main execution
if __name__ == "__main__":
    generator = StudentDataGenerator()
    generator.initialize_database()
    generator.generate_sample_data(100)
    generator.close_connection()
    print("Database generation complete!")