import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('job_tracker.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    position TEXT,
    salary TEXT,
    location TEXT,
    status TEXT,
    date TEXT,
    link TEXT,
    notes TEXT
)
""")
conn.commit()

# Function to add a new job to the database
def add_job():
    # Gather job details from the user
    company = input("Enter company name: ")
    position = input("Enter position: ")
    salary = input("Enter salary: ")
    location = input("Enter location: ")
    status = input("Enter job application status (e.g., Applied, Interview, Offer): ")
    date = input("Enter the date you applied (YYYY-MM-DD): ")  # Date input
    link = input("Enter job listing link (optional): ")  # Link input
    notes = input("Enter any notes (optional): ")  # Notes input

    # Insert the job into the database
    cursor.execute("""
        INSERT INTO jobs (company, position, salary, location, status, date, link, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (company, position, salary, location, status, date, link, notes))
    
    # Commit changes to the database
    conn.commit()
    print(f"Job at {company} added successfully!")

# Function to update the status of a job
def update_job_status():
    job_id = input("Enter the ID of the job to update: ")
    new_status = input("Enter the new status: ")

    # Update job status in the database
    cursor.execute("""
        UPDATE jobs
        SET status = ?
        WHERE id = ?
    """, (new_status, job_id))
    
    conn.commit()
    print(f"Job status updated to {new_status}.")

# Function to delete a job from the database
def delete_job():
    job_id = input("Enter the ID of the job to delete: ")

    # Delete job from the database
    cursor.execute("""
        DELETE FROM jobs
        WHERE id = ?
    """, (job_id,))
    
    conn.commit()
    print("Job deleted successfully.")

# Function to filter jobs by salary or company
def filter_jobs():
    filter_type = input("Filter by (1) Salary or (2) Company: ")
    if filter_type == "1":
        salary_filter = input("Enter the salary to filter by: ")
        cursor.execute("""
            SELECT * FROM jobs WHERE salary = ?
        """, (salary_filter,))
    elif filter_type == "2":
        company_filter = input("Enter the company to filter by: ")
        cursor.execute("""
            SELECT * FROM jobs WHERE company = ?
        """, (company_filter,))
    else:
        print("Invalid filter option.")
        return

    jobs = cursor.fetchall()
    for job in jobs:
        print(f"ID: {job[0]}, Company: {job[1]}, Position: {job[2]}, Salary: {job[3]}, Location: {job[4]}, Status: {job[5]}, Date: {job[6]}, Link: {job[7]}, Notes: {job[8]}")

# Function to export job data to an Excel file
def export_to_excel():
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    # Convert jobs to a DataFrame
    df = pd.DataFrame(jobs, columns=["ID", "Company", "Position", "Salary", "Location", "Status", "Date", "Link", "Notes"])

    # Export to Excel
    df.to_excel("jobs_export.xlsx", index=False)
    print("Jobs exported to jobs_export.xlsx")

# Function to visualize job data with Matplotlib
def visualize_jobs():
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    # Extract company names and job counts
    companies = [job[1] for job in jobs]
    company_counts = {company: companies.count(company) for company in set(companies)}

    # Plot the number of jobs per company
    plt.bar(company_counts.keys(), company_counts.values())
    plt.title('Jobs by Company')
    plt.xlabel('Company')
    plt.ylabel('Number of Jobs')
    plt.xticks(rotation=90)
    plt.show()

# Menu function to provide options to the user
def menu():
    while True:
        print("\nJob Tracker Menu:")
        print("1. Add a new job")
        print("2. Update job status")
        print("3. Delete a job")
        print("4. Filter jobs by salary/company")
        print("5. Export jobs to Excel")
        print("6. Visualize job data")
        print("7. Exit")
        
        # Get user input for menu options
        choice = input("Choose an option: ")

        if choice == "1":
            add_job()
        elif choice == "2":
            update_job_status()
        elif choice == "3":
            delete_job()
        elif choice == "4":
            filter_jobs()
        elif choice == "5":
            export_to_excel()
        elif choice == "6":
            visualize_jobs()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

# Run the menu
menu()

# Close the connection when done
conn.close()
