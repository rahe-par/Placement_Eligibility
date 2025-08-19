# Placement Data Management System

# Overview

This project provides a comprehensive solution for generating, analyzing, and managing student placement data. It consists of three main components:

1. **Data Generator**: Creates synthetic placement data using Faker library
2. **Dashboard**: Streamlit-based web interface for analyzing placement data
3. **Data Exporter**: Utility to export SQLite data to CSV files

# Components

# 1. Data Generator (`data.py`)

Generates realistic student placement data including:
- Student profiles
- Programming skills
- Soft skills assessments
- Placement records

*Features:*
- Creates SQLite database with proper table relationships
- Generates 100+ synthetic student records
- Configurable data ranges for all metrics

# 2. Dashboard (`main.py`)

Interactive web dashboard for placement analysis:

*Features:*
- Eligibility criteria filtering
- Multiple analytics tabs
- Data visualization
- Export functionality

*Sections:*
- Student eligibility checker
- Programming skills analysis
- Soft skills evaluation
- Placement statistics
- Batch comparisons

# 3. Data Exporter (`export.py`)

Utility to export SQLite data to CSV format:

*Features:*
- Exports all tables to separate CSV files
- Maintains data relationships
- Includes validation checks
- Configurable output directory

# Installation

pip install -r requirements.txt
python data_generator.py
python data_exporter.py
streamlit run dashboard.py


This project is for educational purposes as part of the GUVI Artificial Intelligence and Machine Learning program.
