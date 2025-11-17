"""
Nalanda Institute of Technology - College Database
Complete information for student queries
"""

COLLEGE_INFO = {
    "name": "Nalanda Institute of Technology (NIT Nalanda)",
    "location": {
        "address": "Buddhist Villa, Chandaka, Bhubaneswar, Odisha 751024",
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
        "pin_code": "751024",
        "maps_link": "https://www.google.com/maps/dir//Nalanda+Institute+of+Technology"
    },
    "contact": {
        "phone": "+91 99371 65074",
        "email": "info@thenalanda.com",
        "website": "https://www.thenalanda.com"
    },
    "social_media": {
        "facebook": "https://www.facebook.com/share/1AG6TvcnQi/",
        "twitter": "https://x.com/NALANDABHUBANE1",
        "instagram": "https://www.instagram.com/nalandabbsr",
        "linkedin": "https://www.linkedin.com/company/nalanda-institute-of-technology-bhubaneswar/",
        "youtube": "https://youtube.com/@nalandabhubaneswar4971"
    },
    "accreditation": "NAAC A+ Accredited",
    "statistics": {
        "total_students": "15,000+",
        "alumni": "50,000+",
        "programs": "150+",
        "establishment_year": "Not specified"
    }
}

DEPARTMENTS = [
    {
        "name": "Computer Science & Engineering",
        "type": "Engineering",
        "programs": ["B.Tech", "M.Tech", "PhD"],
        "specializations": ["AI & ML", "Data Science", "Cyber Security", "Cloud Computing"],
        "labs": ["Programming Lab", "AI/ML Lab", "Networks Lab", "Database Lab"]
    },
    {
        "name": "Electronics & Communication Engineering",
        "type": "Engineering",
        "programs": ["B.Tech", "M.Tech"],
        "specializations": ["VLSI Design", "Embedded Systems", "IoT", "Signal Processing"],
        "labs": ["Digital Electronics Lab", "Communication Lab", "Microprocessor Lab"]
    },
    {
        "name": "Mechanical Engineering",
        "type": "Engineering",
        "programs": ["B.Tech", "M.Tech"],
        "specializations": ["Robotics", "CAD/CAM", "Thermal Engineering", "Manufacturing"],
        "labs": ["Workshop", "CAD Lab", "Thermal Lab", "Fluid Mechanics Lab"]
    },
    {
        "name": "Civil Engineering",
        "type": "Engineering",
        "programs": ["B.Tech", "M.Tech"],
        "specializations": ["Structural Engineering", "Transportation", "Environmental", "Geotechnical"],
        "labs": ["Concrete Testing Lab", "Surveying Lab", "Soil Mechanics Lab"]
    },
    {
        "name": "Electrical Engineering",
        "type": "Engineering",
        "programs": ["B.Tech", "M.Tech"],
        "specializations": ["Power Systems", "Control Systems", "Renewable Energy", "Electric Vehicles"],
        "labs": ["Power Systems Lab", "Control Lab", "Machines Lab", "Energy Lab"]
    },
    {
        "name": "Information Technology",
        "type": "Engineering",
        "programs": ["B.Tech", "M.Tech"],
        "specializations": ["Web Development", "Mobile Apps", "DevOps", "Blockchain"],
        "labs": ["IT Lab", "Software Engineering Lab", "Mobile App Lab"]
    },
    {
        "name": "Artificial Intelligence & Data Science",
        "type": "Engineering",
        "programs": ["B.Tech", "M.Tech"],
        "specializations": ["Deep Learning", "NLP", "Computer Vision", "Big Data Analytics"],
        "labs": ["AI Lab", "Data Science Lab", "ML Lab", "Analytics Lab"]
    }
]

FACILITIES = {
    "academic": [
        "Central Library with 50,000+ books and e-resources",
        "Digital Library with IEEE, ACM, Springer access",
        "50+ Modern Computer Labs with latest software",
        "Research & Innovation Center",
        "Smart Classrooms with projectors and AV systems",
        "Seminar Halls (capacity 200-500)",
        "Specialized Laboratories for all departments",
        "Maker Space for prototyping and innovation",
        "Language Lab for communication skills",
        "E-learning platforms and MOOCs access"
    ],
    "campus_life": [
        "Separate AC/Non-AC Hostels for Boys and Girls",
        "24x7 Wi-Fi enabled campus with 1Gbps internet",
        "Multi-cuisine Cafeteria and Dining Halls",
        "Medical Center with resident doctor and ambulance",
        "ATM and Banking facilities on campus",
        "Stationery and Photocopy center",
        "Transportation facilities to city",
        "Guest House for parents and visitors",
        "24/7 CCTV surveillance and security",
        "Laundry services in hostels"
    ],
    "sports": [
        "Football Ground",
        "Cricket Ground",
        "Basketball Courts",
        "Volleyball Courts",
        "Badminton Courts (indoor)",
        "Table Tennis facility",
        "Gymnasium with modern equipment",
        "Indoor game room (Chess, Carrom)",
        "Athletics Track",
        "Yoga and Meditation center"
    ],
    "student_activities": [
        "Student Creativity Hub for art, music, photography",
        "Technical Club (coding, robotics, electronics)",
        "Cultural Club (dance, drama, music)",
        "Literary Club (writing, debate, quiz)",
        "Entrepreneurship Cell (E-Cell)",
        "NSS (National Service Scheme)",
        "Student Council and committees",
        "Annual Technical Festival",
        "Annual Cultural Festival",
        "Sports Meet and competitions",
        "Hackathons and coding competitions",
        "Industry visits and guest lectures"
    ],
    "technology": [
        "Enterprise Resource Planning (ERP) system",
        "Online attendance system",
        "Digital assignment submission portal",
        "Virtual classrooms and online exams",
        "Mobile app for students",
        "Biometric attendance",
        "SMS and email alerts to parents"
    ]
}

ADMISSIONS = {
    "process": [
        "Step 1: Online Application through official website (www.thenalanda.com/admissions)",
        "Step 2: Entrance Exam based admission (JEE Main for B.Tech, GATE for M.Tech)",
        "Step 3: Merit-based selection and counseling",
        "Step 4: Document verification (original certificates required)",
        "Step 5: Fee payment and admission confirmation",
        "Step 6: Hostel allocation (if required)"
    ],
    "eligibility": {
        "B.Tech": {
            "qualification": "10+2 or equivalent with Physics, Chemistry, Mathematics (PCM)",
            "minimum_marks": "50% aggregate (45% for SC/ST)",
            "entrance_exam": "JEE Main / State CET",
            "age_limit": "No age limit"
        },
        "M.Tech": {
            "qualification": "B.Tech/BE in relevant discipline from recognized university",
            "minimum_marks": "55% aggregate (50% for SC/ST)",
            "entrance_exam": "GATE score / University entrance test",
            "age_limit": "No age limit"
        },
        "PhD": {
            "qualification": "M.Tech/ME with valid GATE score or equivalent",
            "minimum_marks": "60% aggregate in postgraduation",
            "entrance_exam": "Research aptitude test + Interview",
            "age_limit": "As per UGC norms"
        }
    },
    "fee_structure": {
        "B.Tech_per_year": "₹80,000 - ₹1,20,000 (varies by category)",
        "M.Tech_per_year": "₹60,000 - ₹90,000",
        "hostel_per_year": "₹40,000 - ₹60,000 (AC/Non-AC)",
        "mess_charges": "₹25,000 - ₹30,000 per year",
        "one_time_charges": "₹15,000 (admission + caution deposit)",
        "payment_modes": "Online payment, Demand Draft, Cash (at counter)"
    },
    "important_dates": {
        "application_start": "Usually March/April",
        "application_deadline": "June/July",
        "counseling": "July/August",
        "classes_begin": "August/September",
        "note": "Check website for exact dates"
    },
    "documents_required": [
        "10th & 12th Mark sheets and certificates",
        "JEE Main / GATE scorecard",
        "Transfer Certificate from previous institution",
        "Migration Certificate (if applicable)",
        "Category certificate (SC/ST/OBC)",
        "Income certificate (for fee concession)",
        "Aadhar card copy",
        "Passport size photographs (10 copies)",
        "Medical fitness certificate"
    ],
    "scholarships_available": [
        "Merit-based scholarships (top performers)",
        "Government scholarships (SC/ST/OBC/Minority)",
        "Fee waiver for economically weaker sections",
        "Sports quota scholarships",
        "Girl child education scholarships",
        "Alumni sponsored scholarships"
    ],
    "contact_admissions": {
        "email": "admissions@thenalanda.com",
        "phone": "+91 99371 65074",
        "helpdesk": "Available on student portal"
    },
    "important_pages": [
        "Admissions: https://www.thenalanda.com/admissions",
        "Student Portal: https://www.thenalanda.com/student-portal",
        "Fee Payment: https://www.thenalanda.com/fees"
    ]
}

ACADEMICS = {
    "resources": [
        "Academic Calendar",
        "Examination Portal",
        "Results Portal",
        "Faculty Information",
        "Course Materials",
        "Online Learning Resources"
    ],
    "important_links": {
        "departments": "https://www.thenalanda.com/departments",
        "faculty": "https://www.thenalanda.com/faculty",
        "library": "https://www.thenalanda.com/library",
        "calendar": "https://www.thenalanda.com/calendar",
        "examination": "https://www.thenalanda.com/examination",
        "results": "https://www.thenalanda.com/results"
    }
}

PLACEMENT = {
    "statistics": {
        "placement_rate": "85-90% annually",
        "highest_package": "₹45 LPA (2024)",
        "average_package": "₹6.5 LPA",
        "median_package": "₹5.2 LPA",
        "companies_visited": "150+ companies annually"
    },
    "top_recruiters": [
        "TCS, Infosys, Wipro, Tech Mahindra",
        "Amazon, Microsoft, Google, Adobe",
        "Accenture, Capgemini, Cognizant",
        "L&T, Siemens, ABB, Schneider Electric",
        "BHEL, NTPC, Indian Railways, ISRO",
        "Flipkart, Paytm, PhonePe, Swiggy",
        "Deloitte, Ernst & Young, KPMG, PwC"
    ],
    "support_services": [
        "Dedicated Training & Placement Cell",
        "Aptitude and reasoning training",
        "Technical skill development workshops",
        "Soft skills and communication training",
        "Resume building and LinkedIn profile workshops",
        "Mock interviews with industry experts",
        "Group discussion and presentation practice",
        "Internship opportunities with stipend",
        "Industry projects and live assignments",
        "Career counseling sessions"
    ],
    "internship_programs": {
        "duration": "2-6 months",
        "companies": "200+ companies offer internships",
        "stipend_range": "₹5,000 - ₹50,000 per month",
        "conversion_rate": "40% interns get PPO (Pre-Placement Offer)"
    },
    "training_programs": [
        "C, C++, Java, Python programming",
        "Data Structures & Algorithms",
        "Database Management (SQL, MongoDB)",
        "Web Development (HTML, CSS, JavaScript, React)",
        "Mobile App Development (Android, Flutter)",
        "Cloud Computing (AWS, Azure, Google Cloud)",
        "DevOps and CI/CD",
        "Machine Learning and AI fundamentals",
        "Competitive programming practice",
        "Aptitude and Logical Reasoning"
    ],
    "entrepreneurship": {
        "incubation_center": "Available for student startups",
        "funding_support": "Seed funding up to ₹10 lakhs",
        "mentorship": "Industry mentors and alumni network",
        "success_stories": "15+ student startups launched"
    },
    "higher_studies_support": [
        "GRE/TOEFL/IELTS preparation classes",
        "Statement of Purpose (SOP) guidance",
        "University application assistance",
        "Scholarship information for abroad studies"
    ],
    "page": "https://www.thenalanda.com/placement",
    "contact": {
        "email": "placement@thenalanda.com",
        "phone": "+91 99371 65074",
        "office_hours": "9:00 AM - 5:00 PM (Mon-Sat)"
    }
}

STUDENT_SUPPORT = {
    "scholarships": "https://www.thenalanda.com/scholarships",
    "hostel": "https://www.thenalanda.com/hostel",
    "sports": "https://www.thenalanda.com/sports",
    "clubs": "https://www.thenalanda.com/clubs"
}

RESEARCH = {
    "focus_areas": [
        "Cutting-edge Technology Research",
        "Innovation Labs",
        "Industry Collaborations",
        "Student Research Projects",
        "Faculty Research Publications"
    ],
    "page": "https://www.thenalanda.com/research"
}

ALUMNI = {
    "network": "50,000+ Alumni worldwide",
    "page": "https://www.thenalanda.com/alumni",
    "benefits": [
        "Alumni Network Access",
        "Career Support",
        "Mentorship Programs",
        "Networking Events",
        "Continued Learning Opportunities"
    ]
}

# Quick answers for common queries
QUICK_ANSWERS = {
    "address": "Buddhist Villa, Chandaka, Bhubaneswar, Odisha 751024",
    "phone": "+91 99371 65074",
    "email": "info@thenalanda.com",
    "website": "https://www.thenalanda.com",
    "accreditation": "NAAC A+ Accredited",
    "students": "15,000+ students",
    "alumni": "50,000+ alumni",
    "programs": "150+ programs offered",
    "establishment": "Established in early 2000s",
    "type": "Private Engineering College affiliated to BPUT",
    "ranking": "Among top engineering colleges in Odisha"
}

# Campus Events and Activities Calendar
EVENTS_CALENDAR = {
    "technical_fest": {
        "name": "TechnoNalanda",
        "month": "February",
        "events": ["Coding Marathon", "Robotics Competition", "Project Expo", "Tech Quiz", "Hackathon"],
        "prizes": "Total ₹5 lakhs+ in prizes"
    },
    "cultural_fest": {
        "name": "Nalanda Mahotsav",
        "month": "March",
        "events": ["Dance Competition", "Music Concert", "Drama", "Fashion Show", "Celebrity Night"],
        "participation": "Students from 50+ colleges"
    },
    "sports_events": {
        "name": "Sports Carnival",
        "month": "January & September",
        "events": ["Cricket Tournament", "Football League", "Athletics Meet", "Indoor Games Championship"]
    },
    "workshops_seminars": {
        "frequency": "Monthly",
        "topics": ["Industry 4.0", "AI/ML", "IoT", "Entrepreneurship", "Soft Skills"],
        "speakers": "Industry experts and alumni"
    }
}

# Faculty Information
FACULTY_INFO = {
    "total_faculty": "200+ qualified faculty members",
    "phd_holders": "60%+ faculty with PhD degrees",
    "experience": "Average 10+ years of teaching experience",
    "publications": "500+ research papers published",
    "student_faculty_ratio": "20:1",
    "faculty_development": [
        "Regular FDP (Faculty Development Programs)",
        "Industry internships for faculty",
        "Research grants and support",
        "Conference participation support"
    ]
}

# Alumni Network
ALUMNI_SUCCESS = {
    "network_size": "50,000+ alumni worldwide",
    "placement_companies": ["Google", "Microsoft", "Amazon", "TCS", "Infosys", "Wipro"],
    "higher_studies": ["IITs", "NITs", "IIMs", "Foreign Universities (US, UK, Germany, Canada)"],
    "entrepreneurs": "100+ alumni-founded startups",
    "mentorship": "Alumni mentor current students",
    "events": ["Annual Alumni Meet", "Guest Lectures", "Industry Networking"]
}

# Innovation and Research
INNOVATION_HUB = {
    "research_centers": [
        "AI & Machine Learning Lab",
        "IoT Research Center",
        "Renewable Energy Lab",
        "Robotics & Automation Lab",
        "Materials Science Lab"
    ],
    "patents_filed": "50+ patents by students and faculty",
    "research_grants": "Funded by DST, AICTE, and industry partners",
    "publications": "100+ papers in international journals annually",
    "collaborations": ["IITs", "NITs", "Industry partners", "Foreign universities"]
}

# Student Welfare
STUDENT_WELFARE = {
    "counseling": {
        "services": ["Academic counseling", "Career guidance", "Personal counseling", "Mental health support"],
        "availability": "Professional counselors available on campus",
        "contact": "counseling@thenalanda.com"
    },
    "health_services": {
        "medical_center": "24x7 medical facility with resident doctor",
        "ambulance": "Emergency ambulance service",
        "insurance": "Group medical insurance for students",
        "pharmacy": "On-campus pharmacy"
    },
    "anti_ragging": {
        "policy": "Strict anti-ragging policy enforced",
        "committee": "Anti-Ragging Committee active",
        "helpline": "24x7 helpline number",
        "status": "Ragging-free campus certified"
    },
    "grievance_redressal": {
        "committee": "Student Grievance Committee",
        "online_portal": "Anonymous grievance submission available",
        "response_time": "Within 48 hours"
    }
}

# Transportation
TRANSPORTATION = {
    "bus_service": {
        "routes": "25+ bus routes covering Bhubaneswar and nearby areas",
        "frequency": "Morning and evening services",
        "fare": "Subsidized rates for students"
    },
    "railway_connectivity": {
        "nearest_station": "Bhubaneswar Railway Station (15 km)",
        "major_connections": "Connected to all major cities"
    },
    "airport": {
        "nearest_airport": "Biju Patnaik International Airport (12 km)",
        "connectivity": "Well connected by road"
    }
}

# Food and Dining
DINING_FACILITIES = {
    "mess": {
        "types": "Vegetarian and Non-vegetarian mess",
        "menu": "Weekly rotating menu with variety",
        "hygiene": "FSSAI certified kitchens",
        "special_diet": "Jain food and special dietary requirements available"
    },
    "cafeteria": [
        "Multiple food courts on campus",
        "Popular chains: Dominos, KFC, Cafe Coffee Day",
        "Snacks and beverages available",
        "Student hangout zones"
    ],
    "night_canteen": {
        "timing": "Open till 2 AM",
        "for": "Students during exams and project work"
    }
}

def get_college_info(query_type="all"):
    """
    Get college information based on query type
    
    Args:
        query_type: Type of information requested
            - 'all': Complete information
            - 'contact': Contact details only
            - 'admissions': Admission process
            - 'facilities': Campus facilities
            - 'placement': Placement information
            - 'departments': Department list
    """
    if query_type == "contact":
        return COLLEGE_INFO["contact"]
    elif query_type == "admissions":
        return ADMISSIONS
    elif query_type == "facilities":
        return FACILITIES
    elif query_type == "placement":
        return PLACEMENT
    elif query_type == "departments":
        return DEPARTMENTS
    else:
        return COLLEGE_INFO

def search_college_data(keywords):
    """
    Search college database for specific keywords
    
    Args:
        keywords: List of keywords to search
    
    Returns:
        Relevant information matching keywords
    """
    results = []
    keywords_lower = [k.lower() for k in keywords]
    
    # Check quick answers first
    for key, value in QUICK_ANSWERS.items():
        if any(keyword in key.lower() for keyword in keywords_lower):
            results.append({key: value})
    
    # Check departments
    if any(word in keywords_lower for word in ['department', 'course', 'program', 'branch']):
        results.append({"departments": DEPARTMENTS})
    
    # Check facilities
    if any(word in keywords_lower for word in ['facility', 'hostel', 'library', 'lab', 'campus']):
        results.append({"facilities": FACILITIES})
    
    # Check admissions
    if any(word in keywords_lower for word in ['admission', 'eligibility', 'apply', 'fee']):
        results.append({"admissions": ADMISSIONS})
    
    # Check placement
    if any(word in keywords_lower for word in ['placement', 'job', 'career', 'internship']):
        results.append({"placement": PLACEMENT})
    
    return results if results else [{"info": "No specific match found", "general": COLLEGE_INFO}]
