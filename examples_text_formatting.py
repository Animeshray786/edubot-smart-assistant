"""
Example: How to use TextFormatter in your bot responses
"""

from backend.text_formatter import TextFormatter, fmt_header, fmt_list, fmt_success
from datetime import datetime

# Example 1: Format exam schedule
def format_exam_schedule(exams):
    formatter = TextFormatter()
    
    response = formatter.header("UPCOMING EXAMS", "box")
    response += formatter.alert("Prepare well! Good luck! 🍀", "tip")
    
    for exam in exams:
        response += formatter.schedule_item(
            time=exam['date'],
            title=exam['subject'],
            location=exam['room'],
            details=f"Duration: {exam['duration']} | Total Marks: {exam['marks']}"
        )
    
    response += formatter.quick_buttons(["Study Tips", "Past Papers", "Exam Rules"])
    
    return response


# Example 2: Format course details
def format_course_info(course):
    formatter = TextFormatter()
    
    response = formatter.card(
        title=course['name'],
        icon="📚",
        content=f"Code: {course['code']}\nCredits: {course['credits']}\nInstructor: {course['instructor']}",
        footer=f"Enrolled: {course['students']} students"
    )
    
    response += fmt_header("Course Topics")
    response += fmt_list(course['topics'], icon="✓")
    
    return response


# Example 3: Format results/grades
def format_grades(student_name, grades):
    formatter = TextFormatter()
    
    response = formatter.header(f"Grade Report - {student_name}", "bold")
    
    # Create table
    headers = ["Subject", "Marks", "Grade"]
    rows = [[g['subject'], g['marks'], g['grade']] for g in grades]
    response += formatter.table(headers, rows)
    
    # Calculate average
    avg = sum(g['marks'] for g in grades) / len(grades)
    response += f"\n📊 Average: {avg:.2f}%\n"
    response += formatter.progress_bar(int(avg))
    
    if avg >= 85:
        response += "\n" + fmt_success("Outstanding Performance! 🎉")
    elif avg >= 70:
        response += "\n" + formatter.badge("Good Work!", "green")
    
    return response


# Example 4: Format assignment list
def format_assignments(assignments):
    formatter = TextFormatter()
    
    response = formatter.header("YOUR ASSIGNMENTS", "simple")
    
    pending = [a for a in assignments if not a['submitted']]
    completed = [a for a in assignments if a['submitted']]
    
    if pending:
        response += "\n⏳ **PENDING**\n"
        for a in pending:
            days_left = (a['due_date'] - datetime.now()).days
            status = "🔥 URGENT" if days_left <= 2 else f"📅 Due in {days_left} days"
            response += f"  • {a['title']} - {status}\n"
    
    if completed:
        response += "\n✅ **COMPLETED**\n"
        response += formatter.list_items([a['title'] for a in completed], 'checked')
    
    return response


# Example 5: Format college info
def format_college_info():
    formatter = TextFormatter()
    
    response = formatter.card(
        title="Nalanda Institute",
        icon="🏛️",
        content="Premier Educational Institution\nEst. 1995 | NAAC A+ Accredited\n5000+ Students | 200+ Faculty",
        footer="🌐 www.thenalanda.com"
    )
    
    response += fmt_header("Quick Info")
    
    info = {
        "Location": "Bangalore, India",
        "Courses": "Engineering, Management, Science",
        "Campus Size": "25 Acres",
        "Placement Rate": "95%"
    }
    
    response += formatter.key_value(info)
    
    response += formatter.quick_buttons([
        "Admissions",
        "Courses",
        "Campus Tour",
        "Contact Us"
    ])
    
    return response


# Example 6: Step-by-step guides
def format_admission_process():
    formatter = TextFormatter()
    
    steps = [
        "Visit website and click 'Apply Now'",
        "Fill application form with personal details",
        "Upload required documents (10th, 12th marksheets)",
        "Pay application fee (₹500)",
        "Wait for entrance exam date (sent via email)",
        "Attend entrance exam at campus",
        "Check results online after 1 week",
        "If selected, complete admission formalities"
    ]
    
    response = formatter.header("ADMISSION PROCESS", "box")
    response += formatter.step_by_step(steps)
    response += formatter.alert("Application deadline: July 31st", "warning")
    
    return response


# Example 7: Format faculty contact
def format_faculty_contact(faculty):
    formatter = TextFormatter()
    
    response = formatter.contact_card(
        name=faculty['name'],
        role=faculty['designation'],
        email=faculty['email'],
        phone=faculty['phone'],
        office=faculty['office']
    )
    
    response += fmt_list(faculty['specializations'], icon="🎓")
    response += f"\n📅 Available: {faculty['availability']}\n"
    
    return response
