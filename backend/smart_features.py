"""
Smart Features Module for EduBot
Advanced AI capabilities and unique features
"""

import random
import json
from datetime import datetime, timedelta
import re

class SmartFeatures:
    """Advanced features to make EduBot unique"""
    
    def __init__(self):
        self.study_tips = [
            "🧠 Try the Pomodoro Technique: 25 min study + 5 min break",
            "📚 Active recall is 3x more effective than re-reading",
            "✍️ Teach someone else - best way to learn",
            "🎯 Set specific goals: 'Complete 10 problems' not 'Study math'",
            "🌙 Sleep 7-8 hours - consolidates memory by 40%",
            "💧 Stay hydrated - even 2% dehydration reduces cognitive performance",
            "🏃 Exercise 20 mins before studying - boosts brain function",
            "📝 Handwriting notes improves retention vs typing",
            "🎵 Classical/lo-fi music can enhance focus for some learners",
            "⏰ Study most difficult subjects when you're most alert"
        ]
        
        self.motivational_quotes = [
            "💪 'Success is not final, failure is not fatal' - Churchill",
            "🌟 'The expert in anything was once a beginner' - Helen Hayes",
            "🚀 'Believe you can and you're halfway there' - Roosevelt",
            "📚 'Education is the passport to the future' - Malcolm X",
            "🎯 'Small progress is still progress' - Keep going!",
            "💡 'The only way to do great work is to love what you do' - Jobs",
            "🏆 'Hard work beats talent when talent doesn't work hard'",
            "🌈 'Every expert was once a beginner' - Stay patient",
            "⚡ 'Your limitation is only your imagination'",
            "🔥 'Dream big, start small, act now' - Robin Sharma"
        ]
        
    def get_study_tip(self):
        """Get a random study tip"""
        return random.choice(self.study_tips)
    
    def get_motivation(self):
        """Get motivational quote"""
        return random.choice(self.motivational_quotes)
    
    def calculate_study_schedule(self, exam_date_str, hours_per_day=3):
        """
        Feature 1: Smart Study Planner
        Calculate personalized study schedule based on exam date
        """
        try:
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
            today = datetime.now()
            days_left = (exam_date - today).days
            
            if days_left <= 0:
                return "⚠️ The exam date has passed or is today! Focus on last-minute revision."
            
            total_hours = days_left * hours_per_day
            
            schedule = {
                "days_remaining": days_left,
                "total_study_hours": total_hours,
                "daily_hours": hours_per_day,
                "suggested_breakdown": {
                    "Week 1": "📖 Cover all topics (overview)",
                    "Week 2": "🎯 Deep dive into difficult topics",
                    "Week 3": "✍️ Practice problems & mock tests",
                    "Last 3 days": "📝 Quick revision & formula sheets"
                },
                "daily_routine": [
                    "⏰ Morning (2 hrs): New concepts",
                    "🌅 Afternoon (1 hr): Practice problems",
                    "🌙 Evening (30 min): Quick revision"
                ]
            }
            
            response = f"""
📅 **Smart Study Plan for Your Exam**

🎯 Days Remaining: **{days_left} days**
⏱️ Total Study Time: **{total_hours} hours**
📚 Daily Target: **{hours_per_day} hours**

**📋 Week-by-Week Breakdown:**
"""
            for week, task in schedule["suggested_breakdown"].items():
                response += f"\n{week}: {task}"
            
            response += "\n\n**⏰ Suggested Daily Routine:**"
            for routine in schedule["daily_routine"]:
                response += f"\n• {routine}"
            
            response += f"\n\n💡 **Tip:** {self.get_study_tip()}"
            
            return response
            
        except ValueError:
            return "❌ Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-31)"
    
    def pomodoro_timer(self, sessions=4):
        """
        Feature 2: Pomodoro Study Timer
        Generate pomodoro study session plan
        """
        total_time = sessions * 30  # 25 min + 5 min break
        
        response = f"""
🍅 **Pomodoro Study Session Plan**

📊 Sessions: {sessions}
⏱️ Total Time: {total_time} minutes ({total_time//60}h {total_time%60}m)

**📋 Your Schedule:**
"""
        
        for i in range(1, sessions + 1):
            response += f"\n\n**Session {i}:**"
            response += f"\n  🎯 Focus: 25 minutes"
            response += f"\n  ☕ Break: 5 minutes"
            
            if i % 4 == 0:
                response += f"\n  🌟 Long break: 15-30 minutes (Completed {i} sessions!)"
        
        response += """

**✨ Pomodoro Tips:**
• 📱 Turn off notifications
• 💧 Keep water nearby
• 🪑 Sit comfortably
• 🎯 One task per session
• ✅ Track completed sessions

Ready to start? Say 'Start pomodoro'!
"""
        return response
    
    def exam_stress_reliever(self):
        """
        Feature 3: Quick Stress Relief Techniques
        """
        techniques = [
            {
                "name": "4-7-8 Breathing",
                "steps": [
                    "1. Breathe in for 4 seconds",
                    "2. Hold for 7 seconds",
                    "3. Exhale for 8 seconds",
                    "4. Repeat 4 times"
                ],
                "benefit": "Reduces anxiety in 60 seconds"
            },
            {
                "name": "5-4-3-2-1 Grounding",
                "steps": [
                    "1. Name 5 things you can see",
                    "2. Name 4 things you can touch",
                    "3. Name 3 things you can hear",
                    "4. Name 2 things you can smell",
                    "5. Name 1 thing you can taste"
                ],
                "benefit": "Brings you to present moment"
            },
            {
                "name": "Progressive Muscle Relaxation",
                "steps": [
                    "1. Tense face muscles (5 sec)",
                    "2. Release and relax",
                    "3. Move down: neck → shoulders → arms",
                    "4. Continue to legs and feet"
                ],
                "benefit": "Releases physical tension"
            }
        ]
        
        technique = random.choice(techniques)
        
        response = f"""
😌 **Quick Stress Relief: {technique['name']}**

📋 **Steps:**
"""
        for step in technique['steps']:
            response += f"\n{step}"
        
        response += f"""

✨ **Benefit:** {technique['benefit']}

💡 **Bonus Tips:**
• 🎵 Listen to calming music
• 🚶 Take a 5-minute walk
• 💧 Drink a glass of water
• 🌞 Get some sunlight
• 😊 Smile (tricks brain to feel better!)

{self.get_motivation()}
"""
        return response
    
    def smart_note_taking_guide(self, subject):
        """
        Feature 4: Subject-Specific Note-Taking Strategies
        """
        strategies = {
            "math": {
                "method": "Cornell Method + Practice",
                "tips": [
                    "📐 Write formulas in color",
                    "✍️ Work through examples step-by-step",
                    "🎯 Create formula sheet separately",
                    "🔄 Redo problems without looking",
                    "📊 Draw diagrams for geometry/graphs"
                ]
            },
            "science": {
                "method": "Mind Mapping + Diagrams",
                "tips": [
                    "🔬 Draw and label diagrams",
                    "🔗 Connect concepts with arrows",
                    "📝 Use mnemonics for lists",
                    "🎨 Color-code different topics",
                    "💡 Write in your own words"
                ]
            },
            "history": {
                "method": "Timeline + Story Method",
                "tips": [
                    "📅 Create visual timelines",
                    "📖 Make story connections",
                    "🗺️ Use maps for geography",
                    "👥 Character profiles for key figures",
                    "🔗 Link cause and effect"
                ]
            },
            "languages": {
                "method": "Active Practice + Flashcards",
                "tips": [
                    "🗣️ Speak aloud while writing",
                    "📇 Use flashcards for vocabulary",
                    "📚 Read texts and underline patterns",
                    "✍️ Write short paragraphs daily",
                    "🎧 Listen to native speakers"
                ]
            },
            "programming": {
                "method": "Code + Comment Method",
                "tips": [
                    "💻 Type code, don't copy-paste",
                    "📝 Comment every function",
                    "🐛 Note common errors",
                    "🔄 Rewrite from scratch",
                    "🎯 Build mini-projects"
                ]
            }
        }
        
        subject_key = subject.lower()
        strategy = strategies.get(subject_key, strategies["science"])
        
        response = f"""
📚 **Smart Note-Taking for {subject.title()}**

✨ **Best Method:** {strategy['method']}

**📋 Top Tips:**
"""
        for tip in strategy['tips']:
            response += f"\n• {tip}"
        
        response += """

**🎯 Universal Note-Taking Rules:**
1. ✍️ Handwrite when possible (better retention)
2. 📊 Use headings and subheadings
3. 🎨 Add visual elements (boxes, arrows, highlights)
4. ⏰ Review notes within 24 hours
5. 📝 Summarize each page in 2-3 sentences

💡 Pro tip: Teach your notes to someone (even imaginary)!
"""
        return response
    
    def memory_techniques(self, topic):
        """
        Feature 5: Advanced Memory Techniques
        """
        techniques = {
            "acronyms": {
                "name": "Acronyms & Acrostics",
                "example": "PEMDAS (Please Excuse My Dear Aunt Sally) for math order",
                "how": "Create memorable phrases from first letters"
            },
            "palace": {
                "name": "Memory Palace",
                "example": "Visualize walking through your house, placing facts in rooms",
                "how": "Link info to familiar physical locations"
            },
            "story": {
                "name": "Story Method",
                "example": "Create silly story connecting unrelated items",
                "how": "Brain remembers stories better than lists"
            },
            "chunking": {
                "name": "Chunking",
                "example": "Break phone number 9876543210 → 987-654-3210",
                "how": "Group info into smaller meaningful chunks"
            },
            "linking": {
                "name": "Link Method",
                "example": "Create visual links between concepts",
                "how": "Connect each item to the next with vivid images"
            }
        }
        
        technique = random.choice(list(techniques.values()))
        
        response = f"""
🧠 **Memory Technique: {technique['name']}**

📖 **What is it?**
{technique['how']}

💡 **Example:**
{technique['example']}

**🎯 How to Use for "{topic}":**
1. Break down the topic into key points
2. Apply the {technique['name']} method
3. Practice recalling without notes
4. Test yourself after 1 hour, 1 day, 1 week

**🌟 Bonus Memory Boosters:**
• 😴 Sleep after studying (consolidates memory)
• 🏃 Exercise before learning (increases blood flow)
• 🍎 Eat brain foods (nuts, berries, fish)
• 💧 Stay hydrated (dehydration = poor memory)
• 🔄 Space out study sessions (spaced repetition)

{self.get_study_tip()}
"""
        return response
    
    def career_path_advisor(self, interest):
        """
        Feature 6: AI Career Path Suggestions
        """
        careers = {
            "technology": [
                "💻 Software Engineer",
                "🤖 AI/ML Engineer",
                "☁️ Cloud Architect",
                "🔒 Cybersecurity Analyst",
                "📊 Data Scientist"
            ],
            "business": [
                "📈 Business Analyst",
                "💼 Management Consultant",
                "🎯 Product Manager",
                "💰 Financial Analyst",
                "🚀 Entrepreneur"
            ],
            "creative": [
                "🎨 UX/UI Designer",
                "✍️ Content Creator",
                "🎬 Digital Marketing",
                "📸 Multimedia Artist",
                "🎮 Game Designer"
            ],
            "science": [
                "🔬 Research Scientist",
                "🧬 Biotechnology",
                "🌍 Environmental Scientist",
                "⚕️ Healthcare Professional",
                "🧪 Data Analyst"
            ]
        }
        
        interest_key = interest.lower()
        career_list = careers.get(interest_key, careers["technology"])
        
        response = f"""
🎯 **Career Paths in {interest.title()}**

**🌟 Top Opportunities:**
"""
        for career in career_list:
            response += f"\n• {career}"
        
        response += """

**📚 Skills to Develop:**
• 💡 Problem-solving
• 🤝 Communication
• 💻 Technical skills (specific to field)
• 🎯 Project management
• 🌐 Adaptability & learning

**🚀 Next Steps:**
1. 📖 Research each career in detail
2. 👥 Connect with professionals (LinkedIn)
3. 🎓 Take online courses (Coursera, Udemy)
4. 🏢 Seek internships/projects
5. 🔨 Build portfolio projects

💼 **Resources:**
• LinkedIn Learning
• Coursera Career Academy
• GitHub (for tech)
• Behance (for creative)

Want specific info about any career? Just ask!
"""
        return response
    
    def quick_revision_generator(self, subject, topics):
        """
        Feature 7: Smart Quick Revision Sheet
        """
        response = f"""
⚡ **Quick Revision Sheet: {subject}**

📅 **Generated:** {datetime.now().strftime("%B %d, %Y")}

**🎯 Topics to Cover:**
"""
        topic_list = topics.split(",") if "," in topics else [topics]
        
        for i, topic in enumerate(topic_list, 1):
            response += f"""

**{i}. {topic.strip()} ⭐⭐⭐**
   • Key concepts: _______________
   • Important formulas: _______________
   • Common mistakes: _______________
   • Practice problems: _______________
"""
        
        response += """

**📝 Revision Checklist:**
□ Read through all topics once
□ Test yourself without notes
□ Solve 5 practice problems per topic
□ Review mistakes and weak areas
□ Do a full mock test
□ Sleep well before exam

**⏰ Last-Minute Tips (Day Before Exam):**
• ✅ DO: Review formula sheets
• ✅ DO: Solve previous year papers
• ✅ DO: Get 8 hours sleep
• ❌ DON'T: Start new topics
• ❌ DON'T: Panic or cram
• ❌ DON'T: Stay up all night

🌟 You've got this! Stay confident!
"""
        return response
    
    def focus_mode_challenge(self):
        """
        Feature 8: Gamified Focus Challenges
        """
        challenges = [
            {
                "name": "📚 30-Minute Deep Work",
                "task": "Study without checking phone for 30 mins",
                "reward": "🏆 +50 Focus Points",
                "bonus": "✨ Treat yourself to favorite snack"
            },
            {
                "name": "🎯 Problem Solver",
                "task": "Complete 10 practice problems in a row",
                "reward": "🏆 +75 Achievement Points",
                "bonus": "🎮 15 min gaming break earned"
            },
            {
                "name": "📝 Note Master",
                "task": "Make 5 pages of detailed notes",
                "reward": "🏆 +60 Study Points",
                "bonus": "☕ Coffee break reward"
            },
            {
                "name": "🧠 Quick Recall",
                "task": "Test yourself on 20 concepts without peeking",
                "reward": "🏆 +80 Memory Points",
                "bonus": "🎵 Music break earned"
            }
        ]
        
        challenge = random.choice(challenges)
        
        response = f"""
🎮 **Focus Challenge of the Day!**

🎯 **Challenge:** {challenge['name']}

**📋 Your Mission:**
{challenge['task']}

**🏆 Rewards:**
• {challenge['reward']}
• {challenge['bonus']}

**⏰ Start Timer:**
Say "start challenge" when ready!

**💪 Leaderboard (This Week):**
1. 🥇 Rahul - 450 points
2. 🥈 Priya - 380 points
3. 🥉 Amit - 350 points
👤 You - 0 points (Start earning!)

**✨ Weekly Rewards:**
• 🏆 500+ points: Certificate of Achievement
• 🎁 300+ points: Study tips ebook
• ⭐ 100+ points: Motivational wallpaper

Accept this challenge? Let's go! 💪
"""
        return response
    
    def study_buddy_matcher(self):
        """
        Feature 9: Virtual Study Group Finder
        """
        response = """
👥 **Find Your Study Buddy!**

🎯 **Benefits of Study Groups:**
• 📚 Learn from different perspectives
• 💪 Stay motivated and accountable
• 🤝 Share resources and notes
• ❓ Ask and answer questions
• 🎯 Practice teaching (best learning method)

**🔍 Study Buddy Matching:**

**Available Study Partners (Online Now):**
1. 👤 Priya - Engineering Mathematics
   📍 Online | ⏰ Available: 6-8 PM
   
2. 👤 Rahul - Data Structures & Algorithms
   📍 Library | ⏰ Available: 4-6 PM
   
3. 👤 Sneha - Digital Electronics
   📍 Online | ⏰ Available: Evening

**💡 How to Start:**
1. Choose your subject/topic
2. Set study goals
3. Schedule meeting time
4. Use video call/chat
5. Share screen for doubts

**🎯 Study Group Rules:**
• ✅ Stay on topic
• ✅ Respect everyone's time
• ✅ Share helpful resources
• ✅ Be supportive
• ❌ No distractions

Want to create/join a study group? Say "create study group"!
"""
        return response
    
    def exam_performance_predictor(self, current_score, target_score, days_left):
        """
        Feature 10: Smart Performance Predictor
        """
        score_gap = target_score - current_score
        daily_improvement = score_gap / days_left if days_left > 0 else 0
        
        if score_gap <= 0:
            status = "🎉 You're already at your target!"
            recommendation = "Focus on maintaining and exceeding your current level."
        elif daily_improvement <= 2:
            status = "✅ Achievable with consistent effort"
            recommendation = "Study 2-3 hours daily with focused practice."
        elif daily_improvement <= 5:
            status = "⚠️ Challenging but possible"
            recommendation = "Dedicate 4-5 hours daily, prioritize weak areas."
        else:
            status = "🔥 Requires intense effort"
            recommendation = "Consider extending deadline or adjusting target."
        
        response = f"""
📊 **Exam Performance Prediction**

**📈 Your Stats:**
• Current Score: {current_score}%
• Target Score: {target_score}%
• Days Left: {days_left}
• Gap to Cover: {score_gap}%
• Required Daily Improvement: {daily_improvement:.1f}%

**🎯 Assessment:** {status}

**💡 Recommendation:**
{recommendation}

**📚 Suggested Study Plan:**

**Week 1:** 
• 📖 Cover weak topics (identify using mock tests)
• ⏱️ 3-4 hours daily

**Week 2:**
• 🎯 Practice previous year papers
• ⏱️ 4-5 hours daily

**Last 3 Days:**
• 📝 Quick revision only
• 😴 Prioritize sleep

**🔥 Success Factors:**
• ✅ Consistency beats intensity
• ✅ Quality > Quantity of study hours
• ✅ Test yourself regularly
• ✅ Learn from mistakes
• ✅ Stay positive & confident

**📊 Probability of Success:** {100 - min(int(daily_improvement * 10), 40)}%

{self.get_motivation()}

Need a detailed study plan? Just ask!
"""
        return response

# Initialize global instance
smart_features = SmartFeatures()
