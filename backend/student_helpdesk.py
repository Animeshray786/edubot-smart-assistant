"""
EduBot - Student Helpdesk Module
Specialized assistant for educational institutions
Handles academic queries, campus info, and student services
"""
from datetime import datetime, timedelta
import json


class StudentHelpdeskBot:
    """Smart Student Assistant with comprehensive educational features"""
    
    def __init__(self):
        self.categories = {
            'academic': self.handle_academic,
            'campus': self.handle_campus,
            'administrative': self.handle_administrative,
            'career': self.handle_career,
            'exam': self.handle_exam,
            'assignment': self.handle_assignment,
            'library': self.handle_library,
            'events': self.handle_events
        }
        
        # Sample data - In production, fetch from database
        self.courses_data = self._load_courses_data()
        self.exam_schedule = self._load_exam_schedule()
        self.assignments = self._load_assignments()
        self.events_calendar = self._load_events()
    
    def process_query(self, query, user_id=None):
        """Process student query and return appropriate response"""
        query_lower = query.lower()
        
        # Detect query category
        category = self._detect_category(query_lower)
        
        if category:
            handler = self.categories.get(category)
            if handler:
                return handler(query_lower, user_id)
        
        # Default response if no specific handler found
        return {
            'response': self._get_help_message(),
            'category': 'help',
            'quick_actions': ['Courses', 'Exams', 'Assignments', 'Campus Info']
        }
    
    def _detect_category(self, query):
        """Detect query category using keywords"""
        keywords_map = {
            'academic': ['course', 'syllabus', 'subject', 'class', 'lecture', 'semester', 'credit'],
            'exam': ['exam', 'test', 'quiz', 'marks', 'results', 'score', 'grade'],
            'assignment': ['assignment', 'homework', 'project', 'submission', 'deadline'],
            'library': ['library', 'book', 'borrow', 'return', 'reading'],
            'campus': ['hostel', 'canteen', 'transport', 'bus', 'gym', 'sports'],
            'administrative': ['fees', 'attendance', 'certificate', 'leave', 'admission'],
            'career': ['placement', 'internship', 'job', 'company', 'package', 'interview'],
            'events': ['event', 'fest', 'competition', 'workshop', 'seminar', 'conference']
        }
        
        for category, keywords in keywords_map.items():
            if any(keyword in query for keyword in keywords):
                return category
        
        return None
    
    def handle_academic(self, query, user_id):
        """Handle academic-related queries"""
        if 'course' in query or 'subject' in query:
            return self._get_courses_info()
        elif 'syllabus' in query:
            return self._get_syllabus_info()
        elif 'semester' in query:
            return self._get_semester_info()
        elif 'credit' in query:
            return self._get_credit_info()
        else:
            return self._get_courses_info()
    
    def handle_exam(self, query, user_id):
        """Handle exam-related queries"""
        if 'schedule' in query or 'date' in query:
            return self._get_exam_schedule_info()
        elif 'result' in query or 'marks' in query:
            return self._get_results_info()
        elif 'preparation' in query or 'tips' in query:
            return self._get_exam_tips()
        else:
            return self._get_exam_schedule_info()
    
    def handle_assignment(self, query, user_id):
        """Handle assignment-related queries"""
        if 'pending' in query or 'due' in query:
            return self._get_pending_assignments(user_id)
        elif 'submit' in query:
            return self._get_submission_info()
        elif 'guidelines' in query:
            return self._get_assignment_guidelines()
        else:
            return self._get_pending_assignments(user_id)
    
    def handle_library(self, query, user_id):
        """Handle library-related queries"""
        if 'timing' in query or 'hours' in query:
            return self._get_library_timings()
        elif 'search' in query or 'find' in query:
            return self._get_book_search_info()
        elif 'issue' in query or 'borrow' in query:
            return self._get_issue_info()
        else:
            return self._get_library_info()
    
    def handle_campus(self, query, user_id):
        """Handle campus facility queries"""
        if 'hostel' in query:
            return self._get_hostel_info()
        elif 'canteen' in query or 'food' in query:
            return self._get_canteen_info()
        elif 'transport' in query or 'bus' in query:
            return self._get_transport_info()
        elif 'gym' in query or 'sports' in query:
            return self._get_sports_info()
        else:
            return self._get_campus_overview()
    
    def handle_administrative(self, query, user_id):
        """Handle administrative queries"""
        if 'fees' in query:
            return self._get_fees_info()
        elif 'attendance' in query:
            return self._get_attendance_info(user_id)
        elif 'certificate' in query:
            return self._get_certificate_info()
        elif 'leave' in query:
            return self._get_leave_info()
        else:
            return self._get_admin_help()
    
    def handle_career(self, query, user_id):
        """Handle career and placement queries"""
        if 'placement' in query or 'job' in query:
            return self._get_placement_info()
        elif 'internship' in query:
            return self._get_internship_info()
        elif 'resume' in query or 'cv' in query:
            return self._get_resume_tips()
        elif 'interview' in query:
            return self._get_interview_tips()
        else:
            return self._get_placement_info()
    
    def handle_events(self, query, user_id):
        """Handle events and activities queries"""
        return self._get_upcoming_events()
    
    # ==================== Data Retrieval Methods ====================
    
    def _get_courses_info(self):
        """Get courses information"""
        return {
            'response': """
📚 **Available Courses at Our Institution**

**Engineering Programs:**
1️⃣ Computer Science & Engineering (CSE)
   • Duration: 4 Years (8 Semesters)
   • Intake: 120 Students
   • CGPA Required: 6.0+

2️⃣ Information Technology (IT)
   • Duration: 4 Years (8 Semesters)
   • Intake: 90 Students
   • CGPA Required: 6.0+

3️⃣ Electronics & Communication (ECE)
   • Duration: 4 Years (8 Semesters)
   • Intake: 60 Students
   • CGPA Required: 6.0+

4️⃣ Mechanical Engineering (ME)
   • Duration: 4 Years (8 Semesters)
   • Intake: 60 Students
   • CGPA Required: 6.0+

**Specializations Available:**
• Artificial Intelligence & Machine Learning
• Data Science
• Cyber Security
• Cloud Computing
• IoT & Embedded Systems

Would you like detailed syllabus for any specific course?
            """,
            'category': 'academic',
            'quick_actions': ['CSE Syllabus', 'IT Syllabus', 'Specializations', 'Fee Structure']
        }
    
    def _get_exam_schedule_info(self):
        """Get exam schedule"""
        return {
            'response': """
📅 **Upcoming Examination Schedule**

**Mid-Semester Exams (November 2025):**
• Dates: 20th - 25th November 2025
• Time: 10:00 AM - 1:00 PM
• Mode: Offline (On-Campus)
• Admit Card: Available on student portal

**Detailed Schedule:**
📖 Monday, Nov 20: Database Management Systems
📖 Tuesday, Nov 21: Operating Systems
📖 Wednesday, Nov 22: Computer Networks
📖 Thursday, Nov 23: Software Engineering
📖 Friday, Nov 25: Web Technologies

**End-Semester Exams:**
• Dates: 15th - 22nd December 2025
• Time: 10:00 AM - 1:00 PM
• Seating arrangement will be displayed 2 days prior

**Important Notes:**
⚠️ Carry your ID card and admit card
⚠️ Report 30 minutes before exam
⚠️ No electronic devices allowed

📥 Download detailed schedule from: portal.college.edu/exams
            """,
            'category': 'exam',
            'quick_actions': ['Exam Tips', 'Study Material', 'Previous Papers', 'Results']
        }
    
    def _get_pending_assignments(self, user_id):
        """Get pending assignments"""
        return {
            'response': """
📝 **Your Pending Assignments**

**Urgent - Due This Week:**

1️⃣ **Database Management Systems**
   📅 Due: November 18, 2025 (2 days left)
   📌 Topic: ER Diagram Design for Hospital Management
   📊 Marks: 20
   📤 Submit at: assignments.portal.edu

2️⃣ **Web Technologies**
   📅 Due: November 20, 2025 (4 days left)
   📌 Topic: Responsive Portfolio Website
   📊 Marks: 25
   📤 Submit: GitHub Repository Link

3️⃣ **Machine Learning**
   📅 Due: November 22, 2025 (6 days left)
   📌 Topic: Classification Model Implementation
   📊 Marks: 30
   📤 Submit: Jupyter Notebook + Report

**Next Week:**

4️⃣ **Software Engineering**
   📅 Due: November 28, 2025
   📌 Topic: SRS Document Preparation
   📊 Marks: 20

**Assignment Statistics:**
✅ Completed: 12
⏳ Pending: 4
📊 Average Score: 87.5%

Need help with any assignment? I can provide guidelines and resources!
            """,
            'category': 'assignment',
            'quick_actions': ['Submit Assignment', 'Guidelines', 'Past Assignments', 'Extensions']
        }
    
    def _get_library_info(self):
        """Get library information"""
        return {
            'response': """
📖 **Library Information & Services**

**Library Timings:**
🕐 Monday - Friday: 8:00 AM - 8:00 PM
🕐 Saturday: 9:00 AM - 5:00 PM
🕐 Sunday & Holidays: Closed

**Services Available:**
✅ Book Issue/Return (Max 5 books for 14 days)
✅ Digital Library Access (IEEE, Springer, ACM)
✅ E-Journals & Research Papers
✅ Reading Room (100+ seats)
✅ Photocopy & Printing Services
✅ Group Study Rooms (Bookable)

**Popular Collections:**
📚 Technical Books: 50,000+
📰 Magazines & Journals: 200+
💻 E-Books: 10,000+
🎓 Reference Books: 5,000+

**How to Search Books:**
1. Visit: library.college.edu
2. Login with student ID
3. Search by title/author/ISBN
4. Check availability
5. Reserve online or visit counter

**Current Holdings for Your Course:**
• Database Systems: 150 copies
• Data Structures: 200 copies
• Operating Systems: 180 copies
• Web Development: 120 copies

📞 Contact: library@college.edu | +91-XXXX-XXXXX
            """,
            'category': 'library',
            'quick_actions': ['Search Books', 'Renew Books', 'Reading Room Booking', 'Digital Access']
        }
    
    def _get_placement_info(self):
        """Get placement information"""
        response = """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <h2 style="margin: 0; font-size: 24px;">💼 PLACEMENT & CAREER OPPORTUNITIES 2024-25</h2>
</div>

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #28a745;">
    <h3 style="color: #28a745; margin-top: 0;">📊 Placement Statistics (Academic Year 2024-25)</h3>
    <ul style="list-style: none; padding-left: 0;">
        <li style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">✓ <strong>Students Placed:</strong> 450+ out of 500 (90%)</li>
        <li style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">✓ <strong>Average Package:</strong> ₹6.8 LPA</li>
        <li style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">✓ <strong>Highest Package:</strong> ₹45 LPA (Google)</li>
        <li style="padding: 8px 0;">✓ <strong>Companies Visited:</strong> 180+</li>
    </ul>
</div>

<div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #ffc107;">
    <h3 style="color: #856404; margin-top: 0;">🏢 Top Recruiters</h3>
    
    <div style="margin-bottom: 15px;">
        <strong style="color: #dc3545;">TIER-1 COMPANIES (₹20+ LPA):</strong>
        <ul style="columns: 2; -webkit-columns: 2; -moz-columns: 2;">
            <li>Google</li>
            <li>Microsoft</li>
            <li>Amazon</li>
            <li>Adobe</li>
            <li>Oracle</li>
            <li>Flipkart</li>
        </ul>
    </div>
    
    <div style="margin-bottom: 15px;">
        <strong style="color: #0056b3;">TIER-2 COMPANIES (₹6-15 LPA):</strong>
        <ul style="columns: 2; -webkit-columns: 2; -moz-columns: 2;">
            <li>TCS</li>
            <li>Infosys</li>
            <li>Wipro</li>
            <li>Cognizant</li>
            <li>Accenture</li>
            <li>HCL</li>
        </ul>
    </div>
    
    <div>
        <strong style="color: #17a2b8;">FAST-GROWING STARTUPS (₹8-25 LPA):</strong>
        <ul style="columns: 2; -webkit-columns: 2; -moz-columns: 2;">
            <li>Razorpay</li>
            <li>CRED</li>
            <li>Meesho</li>
            <li>Urban Company</li>
            <li>PhonePe</li>
            <li>Swiggy</li>
        </ul>
    </div>
</div>

<h3 style="color: #667eea;">📅 Upcoming Placement Drives</h3>

<div style="background: white; border: 2px solid #dc3545; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <div style="background: #dc3545; color: white; padding: 10px; margin: -15px -15px 15px -15px; border-radius: 8px 8px 0 0;">
        <strong>Nov 18, 2025 - AMAZON</strong>
    </div>
    <p style="margin: 10px 0;"><strong>Role:</strong> SDE-1 (Software Development Engineer)</p>
    <p style="margin: 10px 0;"><strong>Package:</strong> ₹22 LPA + Signing Bonus</p>
    <p style="margin: 10px 0;"><strong>Eligibility:</strong> 7.0+ CGPA, No backlogs</p>
    <p style="margin: 10px 0;"><strong>Registration Deadline:</strong> Nov 16, 2025</p>
    <div style="background: #fff3cd; padding: 10px; border-radius: 5px; margin-top: 10px; text-align: center;">
        <strong>🔥 HOT OPPORTUNITY - Apply Now!</strong>
    </div>
</div>

<div style="background: white; border: 2px solid #0056b3; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <div style="background: #0056b3; color: white; padding: 10px; margin: -15px -15px 15px -15px; border-radius: 8px 8px 0 0;">
        <strong>Nov 22, 2025 - MICROSOFT</strong>
    </div>
    <p style="margin: 10px 0;"><strong>Role:</strong> Software Engineer</p>
    <p style="margin: 10px 0;"><strong>Package:</strong> ₹28 LPA + Relocation Assistance</p>
    <p style="margin: 10px 0;"><strong>Eligibility:</strong> 7.5+ CGPA, Strong DSA skills</p>
    <p style="margin: 10px 0;"><strong>Registration Deadline:</strong> Nov 19, 2025</p>
    <div style="background: #fff3cd; padding: 10px; border-radius: 5px; margin-top: 10px; text-align: center;">
        <strong>⭐ PREMIUM OPPORTUNITY</strong>
    </div>
</div>

<div style="background: white; border: 2px solid #28a745; border-radius: 10px; padding: 15px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <div style="background: #28a745; color: white; padding: 10px; margin: -15px -15px 15px -15px; border-radius: 8px 8px 0 0;">
        <strong>Nov 25, 2025 - TCS NINJA</strong>
    </div>
    <p style="margin: 10px 0;"><strong>Role:</strong> Assistant Systems Engineer</p>
    <p style="margin: 10px 0;"><strong>Package:</strong> ₹3.6 LPA (Service Bond: 2 years)</p>
    <p style="margin: 10px 0;"><strong>Eligibility:</strong> 6.0+ CGPA, All branches welcome</p>
    <p style="margin: 10px 0;"><strong>Registration:</strong> OPEN - Apply anytime</p>
    <div style="background: #d4edda; padding: 10px; border-radius: 5px; margin-top: 10px; text-align: center;">
        <strong>🟢 MASS HIRING - High Selection Rate</strong>
    </div>
</div>

<div style="background: #e8f5e9; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #4caf50;">
    <h3 style="color: #2e7d32; margin-top: 0;">✅ Eligibility Requirements</h3>
    <p><strong>Academic:</strong></p>
    <ul>
        <li>Minimum 60% aggregate (all semesters)</li>
        <li>No active backlogs at time of interview</li>
        <li>Consistent academic performance</li>
    </ul>
    <p><strong>Pre-Placement:</strong></p>
    <ul>
        <li>Updated resume on placement portal</li>
        <li>Attend mandatory training sessions</li>
        <li>Complete mock interviews</li>
        <li>Pass aptitude screening test</li>
    </ul>
</div>

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #2196f3;">
    <h3 style="color: #1565c0; margin-top: 0;">📚 Preparation Resources</h3>
    
    <p><strong>CODING PRACTICE:</strong></p>
    <ul>
        <li>LeetCode (Solve 200+ problems)</li>
        <li>HackerRank (Data Structures & Algorithms)</li>
        <li>GeeksforGeeks (Company-wise questions)</li>
        <li>CodeChef/Codeforces (Competitions)</li>
    </ul>
    
    <p><strong>INTERVIEW PREPARATION:</strong></p>
    <ul>
        <li>InterviewBit (System Design + Coding)</li>
        <li>Pramp (Mock peer interviews)</li>
        <li>CareerCup (Real interview experiences)</li>
        <li>YouTube (CS Dojo, TechLead)</li>
    </ul>
    
    <p><strong>APTITUDE & REASONING:</strong></p>
    <ul>
        <li>IndiaBIX (Quantitative + Logical)</li>
        <li>Freshersworld (Company test papers)</li>
        <li>Aon Assessment (Practice tests)</li>
    </ul>
    
    <p><strong>RESUME BUILDING:</strong></p>
    <ul>
        <li>Workshops every Friday (4-6 PM)</li>
        <li>One-on-one resume reviews</li>
        <li>ATS-friendly template library</li>
        <li>LinkedIn profile optimization</li>
    </ul>
</div>

<div style="background: #f3e5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #9c27b0;">
    <h3 style="color: #6a1b9a; margin-top: 0;">📧 Contact Placement Cell</h3>
    <ul style="list-style: none; padding-left: 0;">
        <li style="padding: 5px 0;"><strong>Email:</strong> placements@nalanda.edu</li>
        <li style="padding: 5px 0;"><strong>Portal:</strong> careers.nalanda.edu</li>
        <li style="padding: 5px 0;"><strong>Phone:</strong> +91-80-2345-6789</li>
        <li style="padding: 5px 0;"><strong>Office:</strong> Admin Block, 2nd Floor</li>
        <li style="padding: 5px 0;"><strong>Hours:</strong> Mon-Fri: 9:00 AM - 5:30 PM</li>
    </ul>
</div>

<div style="background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%); color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <h3 style="margin-top: 0;">💡 Pro Tips for Success</h3>
    <ol style="line-height: 1.8;">
        <li>Start preparing 6 months before placements</li>
        <li>Focus on Data Structures & Algorithms</li>
        <li>Build 2-3 strong projects for resume</li>
        <li>Practice mock interviews weekly</li>
        <li>Network with alumni in target companies</li>
        <li>Maintain GitHub profile with clean code</li>
        <li>Learn system design basics</li>
        <li>Polish communication & soft skills</li>
    </ol>
</div>

<p style="text-align: center; margin-top: 20px; color: #667eea; font-weight: bold;">🎯 Use Quick Actions Below 👇</p>
        """
        
        return {
            'response': response.strip(),
            'category': 'career',
            'quick_actions': ['Apply for Drive', 'Resume Tips', 'Interview Prep', 'Coding Practice']
        }
    
    def _get_campus_overview(self):
        """Get campus facilities overview"""
        return {
            'response': """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <h2 style="margin: 0;">🏫 Campus Facilities & Amenities</h2>
</div>

<div style="background: #fff3e0; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #ff9800;">
    <h3 style="color: #e65100; margin-top: 0;">🏛️ Academic Facilities</h3>
    <ul>
        <li>Central Library (3 floors, 500+ seats)</li>
        <li>Computer Labs (10 labs, 600+ systems)</li>
        <li>Smart Classrooms (All AC, projector-equipped)</li>
        <li>Research Labs & Innovation Center</li>
        <li>Seminar Halls (Capacity: 300-500)</li>
    </ul>
</div>

<div style="background: #e8f5e9; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #4caf50;">
    <h3 style="color: #2e7d32; margin-top: 0;">🏠 Residential</h3>
    <ul>
        <li>Boys Hostel: 800 rooms (AC & Non-AC)</li>
        <li>Girls Hostel: 600 rooms (AC & Non-AC)</li>
        <li>24/7 Security & CCTV surveillance</li>
        <li>WiFi connectivity (100 Mbps)</li>
        <li>Mess with multi-cuisine options</li>
    </ul>
</div>

<div style="background: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #2196f3;">
    <h3 style="color: #1565c0; margin-top: 0;">⚽ Recreation & Sports</h3>
    <ul style="columns: 2; -webkit-columns: 2; -moz-columns: 2;">
        <li>Football & Cricket grounds</li>
        <li>Basketball & Volleyball courts</li>
        <li>Swimming pool (Olympic size)</li>
        <li>Indoor badminton & table tennis</li>
        <li>Fully-equipped gymnasium</li>
        <li>Gaming & Recreation room</li>
    </ul>
</div>

<div style="background: #fce4ec; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #e91e63;">
    <h3 style="color: #880e4f; margin-top: 0;">🏥 Medical & Wellness</h3>
    <ul>
        <li>Health Center (24/7)</li>
        <li>Ambulance service</li>
        <li>Counseling center</li>
        <li>Yoga & meditation center</li>
    </ul>
</div>

<div style="background: #fff8e1; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #ffc107;">
    <h3 style="color: #f57c00; margin-top: 0;">🍕 Food & Dining</h3>
    <ul>
        <li>Main Canteen (Veg & Non-veg)</li>
        <li>Coffee House & Juice Bar</li>
        <li>Food Court (Multiple cuisines)</li>
        <li>Bakery & Ice Cream Parlor</li>
    </ul>
</div>

<div style="background: #f3e5f5; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #9c27b0;">
    <h3 style="color: #6a1b9a; margin-top: 0;">🏦 Banking & Services</h3>
    <ul>
        <li>ATM (3 machines)</li>
        <li>Bank branch (on campus)</li>
        <li>Post office</li>
        <li>Photocopy & Printing centers</li>
        <li>College transport (15 routes)</li>
    </ul>
</div>

<div style="background: #e0f2f1; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #009688;">
    <h3 style="color: #00695c; margin-top: 0;">📚 Student Amenities</h3>
    <ul style="columns: 2; -webkit-columns: 2; -moz-columns: 2;">
        <li>Stationery shop</li>
        <li>Laundry services</li>
        <li>Mobile recharge & services</li>
        <li>General store</li>
    </ul>
</div>

<p style="text-align: center; color: #667eea; font-weight: bold;">Need specific information about any facility? Use Quick Actions! 👇</p>
            """,
            'category': 'campus',
            'quick_actions': ['Hostel Info', 'Canteen Menu', 'Transport Routes', 'Sports Booking']
        }
    
    def _get_help_message(self):
        """Get help message"""
        return """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <h1 style="margin: 0; font-size: 28px;">👋 Welcome to EduBot!</h1>
    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.95;">Your AI-Powered Study Companion 🚀</p>
</div>

<div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
    
    <!-- Academics Section -->
    <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(to right, #f8f9fa, #e9ecef); border-radius: 10px; border-left: 5px solid #667eea;">
        <h3 style="color: #667eea; margin: 0 0 15px 0; font-size: 20px;">
            <span style="font-size: 24px;">📚</span> ACADEMICS - Master Your Courses
        </h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 2;">
            <li>📋 Course syllabi & credit details</li>
            <li>👨‍🏫 Faculty profiles & office hours</li>
            <li>🕐 Class schedules & room locations</li>
            <li>🎯 Subject prerequisites & learning outcomes</li>
        </ul>
    </div>

    <!-- Examinations Section -->
    <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(to right, #fff3e0, #ffe0b2); border-radius: 10px; border-left: 5px solid #ff9800;">
        <h3 style="color: #ff9800; margin: 0 0 15px 0; font-size: 20px;">
            <span style="font-size: 24px;">📅</span> EXAMINATIONS - Ace Your Tests
        </h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 2;">
            <li>📆 Exam timetables & hall tickets</li>
            <li>⚡ Results & grade reports (instant access!)</li>
            <li>🔄 Re-evaluation & reappear procedures</li>
            <li>💡 Smart exam preparation strategies</li>
        </ul>
    </div>

    <!-- Assignments Section -->
    <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(to right, #e8f5e9, #c8e6c9); border-radius: 10px; border-left: 5px solid #4caf50;">
        <h3 style="color: #4caf50; margin: 0 0 15px 0; font-size: 20px;">
            <span style="font-size: 24px;">📝</span> ASSIGNMENTS - Stay On Track
        </h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 2;">
            <li>⏰ Pending assignments & deadlines tracker</li>
            <li>📤 Submission portals & accepted formats</li>
            <li>🙋 Extension request procedures</li>
            <li>💼 Project guidance & helpful resources</li>
        </ul>
    </div>

    <!-- Library Section -->
    <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(to right, #e3f2fd, #bbdefb); border-radius: 10px; border-left: 5px solid #2196f3;">
        <h3 style="color: #2196f3; margin: 0 0 15px 0; font-size: 20px;">
            <span style="font-size: 24px;">📖</span> LIBRARY - Access Knowledge
        </h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 2;">
            <li>🔍 Search 10,000+ books instantly</li>
            <li>⚡ Issue/return books in 30 seconds</li>
            <li>💻 Digital library with 24/7 access</li>
            <li>🪑 Study room reservations</li>
        </ul>
    </div>

    <!-- Campus Life Section -->
    <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(to right, #fce4ec, #f8bbd0); border-radius: 10px; border-left: 5px solid #e91e63;">
        <h3 style="color: #e91e63; margin: 0 0 15px 0; font-size: 20px;">
            <span style="font-size: 24px;">🏫</span> CAMPUS LIFE - Live Better
        </h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 2;">
            <li>🏠 Hostel facilities & mess menu</li>
            <li>🚌 Transport schedules & routes</li>
            <li>⚽ Sports complex bookings</li>
            <li>🏥 Medical center timings & services</li>
        </ul>
    </div>

    <!-- Administration Section -->
    <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(to right, #f3e5f5, #e1bee7); border-radius: 10px; border-left: 5px solid #9c27b0;">
        <h3 style="color: #9c27b0; margin: 0 0 15px 0; font-size: 20px;">
            <span style="font-size: 24px;">💰</span> ADMIN - Handle Paperwork Fast
        </h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 2;">
            <li>💳 Fee payment & instant receipts</li>
            <li>📊 Attendance tracker (75% alerts!)</li>
            <li>📜 Certificates issued in 48 hours</li>
            <li>📋 Leave applications made easy</li>
        </ul>
    </div>

    <!-- Career Section -->
    <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(to right, #fff9c4, #fff59d); border-radius: 10px; border-left: 5px solid #fbc02d;">
        <h3 style="color: #f57f17; margin: 0 0 15px 0; font-size: 20px;">
            <span style="font-size: 24px;">💼</span> CAREER - Launch Your Future
        </h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 2;">
            <li>📈 Placement statistics & top recruiters</li>
            <li>🏢 Upcoming company drives & openings</li>
            <li>🎤 Mock interviews & preparation sessions</li>
            <li>💼 Internship opportunities & guidance</li>
        </ul>
    </div>

    <!-- Events Section -->
    <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(to right, #e0f2f1, #b2dfdb); border-radius: 10px; border-left: 5px solid #009688;">
        <h3 style="color: #009688; margin: 0 0 15px 0; font-size: 20px;">
            <span style="font-size: 24px;">🎉</span> EVENTS - Never Miss Out
        </h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 2;">
            <li>🎭 Campus fests & cultural nights</li>
            <li>💻 Tech workshops & hackathons</li>
            <li>🏆 Competitions with exciting prizes</li>
            <li>🎨 Club activities & social gatherings</li>
        </ul>
    </div>

    <!-- Smart Features Highlight -->
    <div style="margin-top: 30px; padding: 25px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); border-radius: 12px; text-align: center; box-shadow: 0 3px 12px rgba(0,0,0,0.15);">
        <h3 style="margin: 0 0 15px 0; font-size: 22px; color: white;">
            ✨ PLUS: 30+ Smart Study Features! ✨
        </h3>
        <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 8px; text-align: left;">
            <ul style="margin: 0; padding-left: 20px; line-height: 2.2; color: #333;">
                <li>🎯 <strong>Study Planner</strong> - Personalized schedules</li>
                <li>⏰ <strong>Pomodoro Timer</strong> - Focused study sessions</li>
                <li>🧠 <strong>Memory Techniques</strong> - Ace any subject</li>
                <li>🗺️ <strong>Mind Maps</strong> - Visual learning tools</li>
                <li>📊 <strong>Exam Anxiety Help</strong> - Stay calm & confident</li>
                <li>⚡ <strong>Speed Learning</strong> - Learn 2x faster</li>
                <li>🎵 <strong>Study Music</strong> - Perfect focus playlist</li>
                <li>💪 <strong>Focus Hacks</strong> - Beat distractions</li>
            </ul>
            <p style="margin: 15px 0 0 0; text-align: center; color: #667eea; font-weight: bold;">
                💡 Type <strong>"Smart Study"</strong> to see all features!
            </p>
        </div>
    </div>

    <!-- Quick Start Section -->
    <div style="margin-top: 30px; padding: 25px; background: #f5f5f5; border-radius: 10px; border: 2px dashed #667eea;">
        <h3 style="color: #667eea; margin: 0 0 20px 0; text-align: center; font-size: 20px;">
            🎯 Quick Start - Try These Commands:
        </h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div style="background: white; padding: 12px; border-radius: 8px; border-left: 3px solid #4caf50;">
                💬 "Show pending assignments"
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border-left: 3px solid #ff9800;">
                💬 "When is next exam?"
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border-left: 3px solid #2196f3;">
                💬 "Library timings"
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border-left: 3px solid #9c27b0;">
                💬 "Placement drives this month"
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border-left: 3px solid #e91e63;">
                💬 "Study plan for tomorrow"
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border-left: 3px solid #009688;">
                💬 "I'm stressed about exams"
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border-left: 3px solid #f57f17;">
                💬 "Math shortcuts"
            </div>
            <div style="background: white; padding: 12px; border-radius: 8px; border-left: 3px solid #d32f2f;">
                💬 "Memory technique"
            </div>
        </div>
    </div>

    <!-- Footer CTA -->
    <div style="margin-top: 25px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; text-align: center; color: white;">
        <p style="margin: 0; font-size: 18px; font-weight: bold;">
            🔥 Type anything to get started! I understand natural language. 🔥
        </p>
        <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">
            Just ask your question in plain English - I'm here to help! 😊
        </p>
    </div>

</div>
        """
    
    def _get_exam_tips(self):
        """Get exam preparation tips"""
        return {
            'response': """
💡 **Exam Preparation Tips for Success**

**1. Time Management:**
⏰ Start preparation 2 weeks before
⏰ Create a study timetable
⏰ Allocate time based on difficulty
⏰ Include breaks every 90 minutes

**2. Study Strategy:**
📖 Read theory from textbooks
📝 Make short notes & mind maps
💻 Practice problems & coding
🔄 Revise daily (last 3 days)
❓ Solve previous year papers

**3. Important Topics (Based on weightage):**
✅ Database: Normalization, SQL, Transactions
✅ OS: Process scheduling, Deadlocks, Memory
✅ Networks: OSI Model, TCP/IP, Routing
✅ Software Engineering: SDLC, UML diagrams
✅ Web Tech: HTML/CSS/JS, React basics

**4. During Exam:**
📋 Read all questions first (5 mins)
✏️ Attempt easy questions first
⏱️ Manage time per question
✅ Review answers before submitting

**5. Resources:**
📚 Lecture notes (available on LMS)
📚 Previous year papers (library website)
📚 Reference books (check library)
📚 Online tutorials (YouTube playlists)

**6. Last Minute Tips:**
🎯 Revise formulas & concepts
🎯 Don't study new topics
🎯 Get 7-8 hours sleep
🎯 Eat healthy breakfast
🎯 Reach 30 mins early

**Need subject-specific guidance?** Just ask!

Good luck! 🍀 You've got this! 💪
            """,
            'category': 'exam',
            'quick_actions': ['Study Material', 'Previous Papers', 'Time Table', 'Notes']
        }
    
    def _load_courses_data(self):
        """Load courses data (mock data)"""
        return {}
    
    def _load_exam_schedule(self):
        """Load exam schedule (mock data)"""
        return {}
    
    def _load_assignments(self):
        """Load assignments (mock data)"""
        return {}
    
    def _load_events(self):
        """Load events calendar (mock data)"""
        return {}
    
    def _get_syllabus_info(self):
        """Get syllabus information"""
        return self._get_courses_info()
    
    def _get_semester_info(self):
        """Get semester information"""
        return self._get_courses_info()
    
    def _get_credit_info(self):
        """Get credit information"""
        return self._get_courses_info()
    
    def _get_results_info(self):
        """Get results information"""
        return self._get_exam_schedule_info()
    
    def _get_submission_info(self):
        """Get assignment submission info"""
        return self._get_pending_assignments(None)
    
    def _get_assignment_guidelines(self):
        """Get assignment guidelines"""
        return self._get_pending_assignments(None)
    
    def _get_library_timings(self):
        """Get library timings"""
        return self._get_library_info()
    
    def _get_book_search_info(self):
        """Get book search info"""
        return self._get_library_info()
    
    def _get_issue_info(self):
        """Get book issue info"""
        return self._get_library_info()
    
    def _get_hostel_info(self):
        """Get hostel information"""
        return self._get_campus_overview()
    
    def _get_canteen_info(self):
        """Get canteen information"""
        return self._get_campus_overview()
    
    def _get_transport_info(self):
        """Get transport information"""
        return self._get_campus_overview()
    
    def _get_sports_info(self):
        """Get sports facilities info"""
        return self._get_campus_overview()
    
    def _get_fees_info(self):
        """Get fees information"""
        return {
            'response': "Fee information available. Contact administration.",
            'category': 'administrative',
            'quick_actions': ['Pay Fees', 'Fee Receipt', 'Scholarship']
        }
    
    def _get_attendance_info(self, user_id):
        """Get attendance information"""
        return {
            'response': "Attendance details available on student portal.",
            'category': 'administrative',
            'quick_actions': ['View Attendance', 'Leave Request']
        }
    
    def _get_certificate_info(self):
        """Get certificate information"""
        return {
            'response': "Certificate requests can be submitted online.",
            'category': 'administrative',
            'quick_actions': ['Request Certificate', 'Track Status']
        }
    
    def _get_leave_info(self):
        """Get leave information"""
        return {
            'response': "Leave applications available on portal.",
            'category': 'administrative',
            'quick_actions': ['Apply Leave', 'Check Status']
        }
    
    def _get_admin_help(self):
        """Get administrative help"""
        return {
            'response': "Administrative services available. How can I help?",
            'category': 'administrative',
            'quick_actions': ['Fees', 'Attendance', 'Certificates', 'Leave']
        }
    
    def _get_internship_info(self):
        """Get internship information"""
        return {
            'response': "Internship opportunities available. Check careers portal.",
            'category': 'career',
            'quick_actions': ['View Internships', 'Apply', 'Guidelines']
        }
    
    def _get_resume_tips(self):
        """Get resume tips"""
        return {
            'response': "Resume building workshops every Friday.",
            'category': 'career',
            'quick_actions': ['Resume Template', 'Workshop', 'Review']
        }
    
    def _get_interview_tips(self):
        """Get interview tips"""
        return {
            'response': "Interview preparation resources available.",
            'category': 'career',
            'quick_actions': ['Mock Interview', 'Tips', 'Common Questions']
        }
    
    def _get_upcoming_events(self):
        """Get upcoming events"""
        return {
            'response': """
🎉 **Upcoming Events & Activities**

**This Week:**
📅 Nov 18 - Technical Quiz Competition
📅 Nov 20 - Guest Lecture on AI/ML
📅 Nov 22 - Cultural Night

**This Month:**
📅 Nov 25 - Annual Tech Fest
📅 Nov 28 - Sports Day

More events on: events.college.edu
            """,
            'category': 'events',
            'quick_actions': ['Register', 'View All Events', 'Calendar']
        }
