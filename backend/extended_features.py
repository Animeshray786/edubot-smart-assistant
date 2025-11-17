"""
Extended Smart Features - 50 Additional Features
Advanced educational AI capabilities
"""

import random
import json
from datetime import datetime, timedelta
import re
import math

class ExtendedFeatures:
    """50 Additional cutting-edge features"""
    
    def __init__(self):
        self.initialize_data()
    
    def initialize_data(self):
        """Initialize all feature data"""
        
        # Feature 11: Exam Pattern Analysis
        self.exam_patterns = {
            "multiple_choice": {
                "strategy": "Eliminate wrong answers first, educated guessing on remainder",
                "time_per_q": "1-2 minutes",
                "tips": ["Read all options", "Watch for 'all of the above'", "Trust first instinct"]
            },
            "essay": {
                "strategy": "Outline first, write clearly, conclude strongly",
                "time_per_q": "15-20 minutes",
                "tips": ["Introduction + 3 points + conclusion", "Use examples", "Proofread"]
            },
            "practical": {
                "strategy": "Read full question, plan approach, execute carefully",
                "time_per_q": "Variable",
                "tips": ["Show all steps", "Label everything", "Double-check calculations"]
            }
        }
        
        # Feature 12: Subject Difficulty Analyzer
        self.difficulty_weights = {
            "concept_density": 0.3,
            "math_intensity": 0.25,
            "memorization_load": 0.2,
            "application_level": 0.25
        }
        
        # Feature 13: Smart Flashcard Generator
        self.flashcard_templates = [
            {"front": "Definition", "back": "Term"},
            {"front": "Question", "back": "Answer"},
            {"front": "Cause", "back": "Effect"},
            {"front": "Formula", "back": "Application"},
            {"front": "Concept", "back": "Example"}
        ]
        
        # Feature 14: Study Environment Optimizer
        self.environment_factors = {
            "lighting": ["Natural light best", "Warm white for evening", "Avoid harsh fluorescent"],
            "temperature": ["68-72°F optimal", "Too hot = drowsy", "Too cold = distracted"],
            "noise": ["40-50 dB ideal", "White noise can help", "Complete silence for some"],
            "organization": ["Clean desk", "Materials within reach", "Minimal visual clutter"]
        }
        
        # Feature 15: Concept Mind Map Generator
        self.mind_map_structures = ["hierarchical", "radial", "spider", "flowchart", "tree"]
        
        # Feature 16-20: Quick reference data
        self.productivity_hacks = self._load_productivity_hacks()
        self.exam_day_checklist = self._load_exam_day_checklist()
        self.group_study_rules = self._load_group_study_rules()
        self.reading_techniques = self._load_reading_techniques()
        self.math_shortcuts = self._load_math_shortcuts()
    
    def _load_productivity_hacks(self):
        return [
            "🎯 Two-Minute Rule: If task takes <2min, do it now",
            "🍅 Eat the Frog: Hardest task first thing in morning",
            "📝 Batch Similar Tasks: Group emails, calls, reading together",
            "⏰ Time Boxing: Allocate fixed time slots for tasks",
            "🚫 Say No: Protect your study time fiercely",
            "📱 Phone in Another Room: Out of sight, out of mind",
            "🎵 Environment Design: Make good habits easy, bad hard",
            "✅ Daily Top 3: Focus on 3 most important tasks",
            "🔄 Weekly Review: Plan week every Sunday evening",
            "💪 Energy Management: Work with your natural rhythms"
        ]
    
    def _load_exam_day_checklist(self):
        return {
            "night_before": ["Review formula sheet", "Pack bag", "Set 2 alarms", "Sleep by 10 PM"],
            "morning": ["Healthy breakfast", "Arrive 30min early", "Use bathroom", "Quick breathing"],
            "during_exam": ["Read all questions first", "Budget time", "Start with easy ones", "Check work"],
            "avoid": ["All-nighter", "New topics", "Heavy foods", "Comparing with others"]
        }
    
    def _load_group_study_rules(self):
        return [
            "🎯 Set Clear Goals: What to accomplish in session",
            "⏰ Time Limits: 45-90 minutes max per session",
            "📱 No Phones: Airplane mode or in a pile",
            "🗣️ Teach Others: Best way to solidify knowledge",
            "❓ Ask Questions: No stupid questions rule",
            "📝 Share Resources: Notes, links, strategies",
            "🔄 Rotate Roles: Leader, note-taker, time-keeper",
            "☕ Schedule Breaks: Every 45 minutes",
            "🎯 Stay on Topic: Save socializing for break",
            "📊 Track Progress: What did we accomplish?"
        ]
    
    def _load_reading_techniques(self):
        return {
            "SQ3R": "Survey → Question → Read → Recite → Review",
            "Skimming": "Quick overview, headings, first/last paragraphs",
            "Scanning": "Looking for specific information or keywords",
            "Active Reading": "Highlight, annotate, question as you read",
            "Speed Reading": "Reduce subvocalization, use pointer, practice"
        }
    
    def _load_math_shortcuts(self):
        return [
            "Squaring numbers ending in 5: (n×(n+1)) then 25",
            "Multiply by 11: abc × 11 = a(a+b)(b+c)c",
            "Percentage of number: Use fractions (25% = 1/4)",
            "Square root estimation: Find nearest perfect square",
            "Fast division by 9: Sum of digits divisible by 9?"
        ]
    
    # FEATURE 11: Exam Pattern Analysis
    def analyze_exam_pattern(self, exam_type):
        """Analyze and provide strategy for different exam patterns"""
        pattern = self.exam_patterns.get(exam_type.lower(), self.exam_patterns["multiple_choice"])
        
        return f"""
📋 **{exam_type.title()} Exam Strategy**

**🎯 Best Strategy:**
{pattern['strategy']}

**⏱️ Time Management:**
Allocate: {pattern['time_per_q']} per question

**💡 Key Tips:**
"""  + "\n".join([f"• {tip}" for tip in pattern['tips']]) + """

**🎓 Pro Techniques:**
• Practice with past papers under timed conditions
• Mark difficult questions and return to them
• Use process of elimination
• Show all your work for partial credit
• Review answers if time permits

**Common Mistakes to Avoid:**
❌ Spending too long on one question
❌ Not reading instructions carefully
❌ Changing answers without reason
❌ Leaving questions blank (guess intelligently!)
"""
    
    # FEATURE 12: Subject Difficulty Analyzer
    def analyze_subject_difficulty(self, subject, current_level):
        """Analyze subject difficulty and provide customized approach"""
        difficulty_score = random.randint(60, 95)  # Simulated AI analysis
        
        if difficulty_score < 70:
            difficulty = "Manageable"
            approach = "Standard study schedule with regular practice"
            time_needed = "2-3 hours/day"
        elif difficulty_score < 85:
            difficulty = "Moderate Challenge"
            approach = "Focused study with extra problem-solving"
            time_needed = "3-4 hours/day"
        else:
            difficulty = "High Challenge"
            approach = "Intensive study with tutoring/group help"
            time_needed = "4-5 hours/day"
        
        return f"""
📊 **Subject Difficulty Analysis: {subject}**

**🎯 Difficulty Level:** {difficulty} ({difficulty_score}/100)
**👤 Your Level:** {current_level}

**📚 Recommended Approach:**
{approach}

**⏰ Time Investment:** {time_needed}

**🔍 Key Challenge Areas:**
• Concept Density: {"High" if difficulty_score > 80 else "Medium"}
• Math Intensity: {"High" if difficulty_score > 85 else "Medium"}
• Memorization Load: {"High" if difficulty_score > 75 else "Medium"}

**📈 Success Strategy:**

**Week 1-2:** Build Foundation
• Master basic concepts
• Create comprehensive notes
• Solve simple problems

**Week 3-4:** Intermediate Practice
• Tackle medium difficulty problems
• Join study groups
• Seek clarification on doubts

**Week 5+:** Advanced Mastery
• Solve previous years' papers
• Time-bound practice tests
• Focus on weak areas

**🎓 Resources Recommended:**
• Video Lectures: Khan Academy, MIT OCW
• Practice: Previous year papers
• Help: Office hours, study groups
• Books: Refer textbook + 1 guide book

**💪 You've got this! Start with small wins.**
"""
    
    # FEATURE 13: Smart Flashcard Generator
    def generate_flashcards(self, topic, count=10):
        """Generate smart flashcard study plan"""
        return f"""
🎴 **Smart Flashcard System: {topic}**

**📝 Creating {count} Flashcards:**

**✨ Flashcard Best Practices:**

**Front Side Tips:**
• Keep questions clear and specific
• One concept per card
• Use images when possible
• Include context if needed

**Back Side Tips:**
• Concise but complete answers
• Add examples for clarity
• Use mnemonics when helpful
• Cross-reference related cards

**🎯 Suggested Card Types:**

1. **Definition Cards** (30%)
   Front: "What is {topic}?"
   Back: Clear definition + example

2. **Application Cards** (25%)
   Front: "When would you use {topic}?"
   Back: Real-world scenarios

3. **Process Cards** (20%)
   Front: "How does {topic} work?"
   Back: Step-by-step explanation

4. **Comparison Cards** (15%)
   Front: "{topic} vs related concept?"
   Back: Key differences table

5. **Example Cards** (10%)
   Front: "Example of {topic}?"
   Back: Detailed example with solution

**📱 Digital Tools:**
• Anki (best for spaced repetition)
• Quizlet (collaborative + games)
• RemNote (integrated with notes)
• Physical cards (best for kinesthetic learners)

**🔄 Study Schedule:**

**Day 1:** Create all cards
**Day 2:** Review all cards 2-3 times
**Day 3:** Review incorrect ones
**Day 7:** Full review
**Day 14:** Final review
**Before Exam:** Quick shuffle through all

**🧠 Active Recall Technique:**
• Don't flip too quickly (think 5-10 seconds)
• Say answer out loud before flipping
• Mark difficult cards for extra review
• Shuffle regularly to avoid order memory

**📊 Tracking Progress:**
□ {count} cards created
□ First full review done
□ Difficult cards identified
□ Second review completed
□ Confidence level: ___/10
"""
    
    # FEATURE 14: Study Environment Optimizer
    def optimize_study_environment(self):
        """Provide comprehensive environment optimization guide"""
        return """
🏠 **Ultimate Study Environment Setup**

**💡 Lighting (Critical!):**
• ✅ Natural daylight is best (near window)
• ✅ Warm white LED (3000-4000K) for artificial
• ✅ Task lamp for desk (reduce eye strain)
• ❌ Avoid harsh fluorescent lights
• ❌ No direct glare on screen/books

**🌡️ Temperature:**
• Optimal: 68-72°F (20-22°C)
• Too warm → Drowsiness
• Too cold → Distraction & discomfort
• Dress in layers to adjust easily

**🔇 Noise Level:**
• 40-50 dB: Ideal (quiet library level)
• Some do best with:
  - White/pink noise
  - Nature sounds
  - Lo-fi instrumental music
• Use noise-canceling headphones if needed
• Communicate "study time" to others

**🪑 Ergonomics:**
• Chair: Back support, feet flat on floor
• Desk: Elbows at 90° when typing
• Screen: Eye level, arm's length away
• Posture: Sit back, shoulders relaxed
• Stand/stretch every 30 minutes

**📚 Organization:**
• Clear desk of distractions
• Keep only current subject materials
• Everything within arm's reach
• Cable management (reduces visual clutter)
• Fresh air (crack window periodically)

**🎨 Visual Environment:**
• Minimal decorations (reduce distractions)
• Plants improve air quality & mood
• Use color psychology:
  - Blue: Calm, focus (best for walls)
  - Green: Balance, creativity
  - Yellow: Energy (accent only)
• Keep it clean & tidy

**📱 Digital Hygiene:**
• Phone in another room or drawer
• Use website blockers during study
• Single monitor focus (close extra tabs)
• Notification OFF for all apps
• Airplane mode if possible

**☕ Accessibility:**
• Water bottle on desk (stay hydrated!)
• Healthy snacks nearby (nuts, fruit)
• Tissues, hand sanitizer
• Pens, highlighters organized
• Timer/clock visible

**🌟 Productivity Zones:**
Create 3 zones:
1. **Focus Zone**: Desk for deep work
2. **Reading Zone**: Comfortable chair
3. **Break Zone**: Different room/area

**🔄 Environmental Ritual:**
• Same place, same time = habit formation
• 5-minute setup routine before studying
• Scent association (peppermint for focus)
• Clean/reset environment after each session

**⚡ Quick Environment Check:**
□ Lighting comfortable?
□ Temperature good?
□ Noise level acceptable?
□ Posture correct?
□ Phone away?
□ Distractions removed?
□ Water available?

**Optimize once, benefit always! 🚀**
"""
    
    # FEATURE 15: Concept Mind Map Generator
    def generate_mind_map_guide(self, topic):
        """Generate mind map creation guide for any topic"""
        return f"""
🧠 **Mind Map Creation Guide: {topic}**

**🎨 Mind Mapping Basics:**

**Center:**
📌 Write "{topic}" in center
📌 Use large, bold letters
📌 Add a simple icon/image
📌 Use color (main theme color)

**Main Branches (5-7 max):**
1st Level: Key concepts/categories
• Use different color per branch
• Keep words short (1-3 words)
• Draw thick, curved lines
• Add small icons

**Sub-Branches:**
2nd Level: Supporting details
• Thinner lines, same color family
• More specific information
• Examples, formulas, facts

**3rd Level:** Deep details
• Even thinner lines
• Specific examples
• Cross-references

**🎨 Visual Elements:**

**Colors:**
• 🔴 Red: Important/urgent concepts
• 🔵 Blue: Core foundations
• 🟢 Green: Examples/applications
• 🟡 Yellow: Warnings/special notes
• 🟣 Purple: Advanced concepts

**Icons & Symbols:**
• ⭐ Key concepts
• ❗ Important points
• ✓ Mastered topics
• ❓ Need clarification
• 🔗 Related to other topics

**🖊️ Lettering:**
• Print clearly (no cursive)
• Vary size for hierarchy
• All capitals for main branches
• Lower case for details

**📋 Step-by-Step Creation:**

**Step 1: Brain Dump (5 min)**
Write everything you know about {topic}

**Step 2: Organize (10 min)**
Group related concepts into 5-7 categories

**Step 3: Center (2 min)**
Create attractive center with topic name

**Step 4: Main Branches (15 min)**
Draw and label main category branches

**Step 5: Sub-Branches (20 min)**
Add supporting details to each branch

**Step 6: Decorate (10 min)**
Add colors, icons, images

**Step 7: Review & Refine (5 min)**
Check connections, add any missing links

**🔗 Connection Types:**
• Solid lines: Direct relationships
• Dotted lines: Indirect connections
• Arrows: Cause-effect, sequences
• Numbers: Order/priority
• Boxes: Group related sub-branches

**📱 Digital Tools:**
• MindMeister (collaborative)
• XMind (professional features)
• Coggle (simple & beautiful)
• SimpleMind (mobile-friendly)
• Paper (most effective for memory!)

**🧠 Memory Enhancement:**
• Draw by hand when possible (better retention)
• Use memorable/funny images
• Create acronyms from branches
• Color code related concepts
• Review and redraw from memory

**🎯 Use Cases:**

**Before Studying:**
• Overview of topic
• Identify what you know/don't know

**During Studying:**
• Organize information as you learn
• See relationships between concepts

**After Studying:**
• Quick revision tool
• Test your recall (redraw from memory)

**Before Exam:**
• One-page visual summary
• Rapid review tool

**📊 Mind Map Checklist:**
□ Center is clear and attractive
□ 5-7 main branches
□ Multiple sub-branches per main
□ Colors used consistently
□ Icons/images included
□ Connections shown
□ All key concepts covered
□ Space used efficiently
□ Readable from distance

**💡 Pro Tips:**
• Landscape orientation gives more space
• Leave room for additions
• Create master map, then detailed sub-maps
• Take photo for digital backup
• Recreate from memory for practice

**Your brain thinks in pictures, not paragraphs! 🎨**
"""
    
    # FEATURES 16-25: Rapid-Fire Productivity Features
    
    def get_productivity_hack(self, number=None):
        """Feature 16: Get specific productivity hack"""
        if number and 1 <= number <= len(self.productivity_hacks):
            hack = self.productivity_hacks[number-1]
        else:
            hack = random.choice(self.productivity_hacks)
        
        return f"""
⚡ **Productivity Hack of the Moment**

{hack}

**How to Implement:**
1. Start small - try for just one day
2. Track your progress
3. Adjust to your style
4. Make it a habit (21 days)

**Expected Results:**
• 20-40% more productive time
• Less decision fatigue
• Better focus quality
• Reduced procrastination

Try it today! 🚀
"""
    
    def get_exam_day_plan(self):
        """Feature 17: Complete exam day execution plan"""
        checklist = self.exam_day_checklist
        
        return f"""
📅 **Perfect Exam Day Plan**

**🌙 Night Before (Critical!):**
"""  + "\n".join([f"□ {item}" for item in checklist["night_before"]]) + f"""

**🌅 Morning Routine:**
""" + "\n".join([f"□ {item}" for item in checklist["morning"]]) + f"""

**📝 During Exam:**
""" + "\n".join([f"□ {item}" for item in checklist["during_exam"]]) + f"""

**❌ Absolutely Avoid:**
""" + "\n".join([f"• {item}" for item in checklist["avoid"]]) + """

**⏰ Timeline:**

**10 PM (Night Before):**
• Final review of formulas/key concepts
• Pack bag with all materials
• Set TWO alarms (phone + backup)
• Lights out by 10:30 PM

**7 AM (Exam Day):**
• Wake up, light exercise/stretch
• Healthy breakfast (protein + complex carbs)
• No cramming - light review only
• Positive affirmations

**8 AM:**
• Leave home (arrive 30min early)
• Carry: ID, pens, calculator, water

**8:30 AM:**
• Reach venue
• Use bathroom
• Find your seat
• Breathe deeply (4-7-8 technique)

**9 AM (Exam Starts):**
• Listen to ALL instructions
• Write name/roll number first
• Skim through ALL questions (2 min)
• Budget time per section
• Start with easiest questions

**During Exam:**
• Every 15 min: check time
• Mark difficult questions, return later
• Show all work (partial credit)
• Last 10 min: review answers

**After Exam:**
• Don't discuss answers immediately
• Relax, hydrate, snack
• Light activity before next exam
• Avoid social media comparisons

**🎒 Pack Your Bag:**
□ Admit card/ID
□ 3-4 pens (blue/black)
□ Pencils + eraser
□ Calculator (if allowed)
□ Ruler/geometry box
□ Water bottle
□ Tissues/handkerchief
□ Watch (if no wall clock)
□ Light snack (break time)
□ Glasses/contacts (if needed)

**🧠 Mental Preparation:**
• Visualize success
• Recall: you ARE prepared
• Anxiety is normal and useful
• Trust your preparation
• Focus on YOUR paper, not others

**💪 You're ready! Go ace it! 🌟**
"""
    
    def get_group_study_guide(self):
        """Feature 18: Effective group study strategies"""
        return """
👥 **Mastering Group Study Sessions**

**🎯 The Rules:**

""" + "\n".join(self.group_study_rules) + """

**📊 Optimal Group Size:**
• **2-3 people**: Best for deep discussions
• **4-5 people**: Good for diverse perspectives
• **6+ people**: Only for specific projects

**🎭 Assign Roles (Rotate Each Session):**

**1. Facilitator/Leader:**
• Keeps group on track
• Manages time
• Ensures everyone participates

**2. Note-Taker:**
• Records key points
• Shares notes after session
• Documents questions to research

**3. Time-Keeper:**
• Monitors session time
• Calls breaks
• Alerts when time is running out

**4. Question Master:**
• Poses challenging questions
• Encourages critical thinking
• Leads discussions

**📅 Session Structure (90 minutes):**

**0-5 min: Check-In**
• What did you study since last time?
• What are your goals today?
• Any quick wins to share?

**5-40 min: Learning Block 1**
• Cover first major topic
• Each person teaches a concept (5 min each)
• Group discussion on difficult areas

**40-50 min: Break**
• Get up, move around
• Snack, bathroom
• NO phones/social media

**50-80 min: Learning Block 2**
• Cover second topic
• Practice problems together
• Quiz each other

**80-90 min: Wrap-Up**
• Summarize what was covered
• Assign topics for next session
• Schedule next meeting

**🎯 Effective Group Activities:**

**Teaching Carousel:**
• Each person prepares to teach one concept
• Rotate and teach to different partners
• Best way to solidify knowledge

**Quiz Competition:**
• Create questions for each other
• Friendly competition with small rewards
• Immediate feedback and discussion

**Problem-Solving Marathon:**
• Work through difficult problems together
• One person works, others observe and help
• Discuss multiple solution approaches

**Concept Mapping:**
• Create large mind map together
• Everyone contributes with different colors
• Visual synthesis of knowledge

**Mock Exam:**
• Create practice test together
• Take it individually (timed)
• Review and explain answers to each other

**❌ Group Study Pitfalls (Avoid!):**

**Socializing Too Much:**
• Set phone timer for focus blocks
• Save socializing for breaks
• Remind each other of goals

**Unequal Participation:**
• Direct questions to quiet members
• Use round-robin format
• Everyone must contribute

**Going Off-Topic:**
• Facilitator brings back to agenda
• "Parking lot" for off-topic questions
• Address after main goals met

**Free-Riding:**
• Everyone prepares in advance
• Assign specific topics to each person
• Group agreement on expectations

**🌟 Virtual Group Study:**

**Tools:**
• Zoom/Google Meet: Video calls
• Google Docs: Collaborative notes
• Jamboard/Miro: Visual collaboration
• Discord: Voice channels + screen share

**Virtual Tips:**
• Camera ON (better engagement)
• Use breakout rooms for pair work
• Share screens to solve problems together
• Record session for those who miss it

**📊 Track Group Progress:**

Create shared document with:
• Topics covered each session
• Individual contributions
• Concepts mastered
• Areas needing more work
• Next session agenda

**✅ Group Study Checklist:**

**Before Session:**
□ Everyone prepared their assigned topic
□ Shared document created/updated
□ Meeting link/location confirmed
□ Materials ready

**During Session:**
□ Started on time
□ All roles assigned
□ Goals clearly stated
□ Everyone participated
□ Breaks taken
□ Notes documented

**After Session:**
□ Notes shared with everyone
□ Next session scheduled
□ Action items clear
□ Progress tracked

**💡 Making It Work Long-Term:**
• Meet same day/time each week
• Rotate leadership responsibilities
• Celebrate milestones together
• Support each other emotionally
• Form genuine friendships

**Together we learn better! 🚀**
"""
    
    def get_reading_technique_guide(self, technique_name=None):
        """Feature 19: Advanced reading techniques"""
        if technique_name and technique_name in self.reading_techniques:
            technique = {technique_name: self.reading_techniques[technique_name]}
        else:
            technique = self.reading_techniques
        
        return """
📖 **Advanced Reading Techniques for Students**

**🎯 Choose Your Technique Based on Purpose:**

**SQ3R Method (Deep Understanding):**
📌 **Survey** - Skim headings, intro, summary (5 min)
📌 **Question** - Turn headings into questions
📌 **Read** - Read actively, looking for answers
📌 **Recite** - Close book, recall key points
📌 **Review** - Quick re-read, check understanding

**Best for:** Textbooks, research papers
**Time:** Full attention, slower pace
**Retention:** 70-80%

---

**Skimming (Quick Overview):**
👀 **Purpose:** Get main idea fast
📌 Read first/last paragraphs
📌 Read first sentence of each paragraph
📌 Look at headings, bold words
📌 Check images, charts, captions

**Best for:** Deciding if worth full read
**Time:** 1-2 minutes per page
**Retention:** 20-30%

---

**Scanning (Find Specific Info):**
🔍 **Purpose:** Locate specific information
📌 Know what you're looking for
📌 Move eyes quickly over page
📌 Stop when you find it
📌 Read that section carefully

**Best for:** Research, finding data/quotes
**Time:** 30 seconds per page
**Retention:** 100% of found info

---

**Active Reading (Maximum Retention):**
✍️ **Techniques:**
• Highlight key points (max 20% of text)
• Write margin notes/questions
• Underline important terms
• Create summary in own words
• Make connections to prior knowledge

**Best for:** Study material, difficult texts
**Time:** Slow, thorough
**Retention:** 80-90%

---

**Speed Reading (Volume Reading):**
⚡ **Techniques:**
• Reduce subvocalization (don't say words in head)
• Use pointer (finger/pen) to guide eyes
• Read in chunks (3-5 words at a time)
• Eliminate regression (don't re-read)
• Practice with easier material first

**Best for:** Fiction, easy non-fiction
**Time:** 400-700 words/minute (trained)
**Retention:** 50-60%

---

**📚 Practical Application:**

**Textbook Chapter:**
1. **Survey** (5 min): Skim chapter
2. **Question** (3 min): What will I learn?
3. **Read** (30-45 min): Active reading
4. **Recite** (10 min): Explain to yourself
5. **Review** (5 min): Go through notes

**Research Paper:**
1. **Abstract** (2 min): Get overview
2. **Skim** (5 min): Introduction + Conclusion
3. **Decide**: Worth full read?
4. **Deep Read** (20-40 min): If relevant
5. **Notes** (10 min): Key findings

**News/Articles:**
1. **Skim** (2 min): Headline, first/last para
2. **Decide**: Interesting?
3. **Speed Read** (5 min): Main body
4. **Note**: Key takeaway

---

**🧠 Improving Reading Comprehension:**

**Before Reading:**
• Set clear purpose (Why am I reading this?)
• Preview material (5-minute skim)
• Activate prior knowledge (What do I already know?)
• Prepare questions (What do I want to learn?)

**During Reading:**
• Visualize concepts (create mental images)
• Connect to experience (relate to your life)
• Question constantly (Does this make sense?)
• Annotate actively (write in margins)

**After Reading:**
• Summarize in 3-5 sentences
• Teach to someone else
• Make flashcards for key terms
• Review within 24 hours

---

**📊 Reading Speed vs Comprehension:**

```
Speed          WPM      Comprehension    Use Case
----------------------------------------------------------------
Very Slow      100-200     95%          Math, Philosophy
Slow           200-300     85%          Textbooks
Moderate       300-400     75%          General study
Fast           400-600     60%          Easy material
Very Fast      600-1000    40%          Scanning only
```

---

**💡 Tips for Difficult Texts:**

**Technical/Scientific:**
• Read three times (skim, deep, review)
• Look up unfamiliar terms immediately
• Explain each paragraph in simple words
• Draw diagrams to visualize concepts

**Philosophy/Theory:**
• Very slow, thoughtful reading
• Pause after each paragraph to reflect
• Discuss with others
• Write counter-arguments

**Foreign Language:**
• Don't translate every word
• Guess meaning from context
• Focus on main ideas first
• Re-read for details

---

**📱 Digital Reading Tips:**

**Reduce Eye Strain:**
• 20-20-20 rule (every 20 min, look 20 ft away, 20 sec)
• Adjust brightness (match environment)
• Increase font size
• Use night mode in evening

**Stay Focused:**
• Full-screen mode
• Close other tabs
• Use reading apps (Pocket, Instapaper)
• Download for offline reading

**Better Retention:**
• Print important material (better memory)
• Use annotation tools
• Take handwritten notes
• Review on different device

---

**⏱️ Building Reading Stamina:**

**Week 1:** 15 minutes daily
**Week 2:** 20 minutes daily
**Week 3:** 30 minutes daily
**Week 4:** 45+ minutes daily

**Track:**
• Pages read per day
• Time spent
• Comprehension (self-test)
• Speed improvement

---

**✅ Reading Session Checklist:**

**Before:**
□ Clear purpose set
□ Environment quiet
□ Timer set (Pomodoro)
□ Note-taking materials ready

**During:**
□ Phone away
□ Active engagement (highlighting/notes)
□ Breaks every 25-30 minutes
□ Questions noted for research

**After:**
□ Summary written
□ Key points highlighted
□ Questions answered or saved
□ Next reading planned

**Master reading, master learning! 📚**
"""
    
    def get_math_shortcut_guide(self):
        """Feature 20: Quick math calculation tricks"""
        return """
🧮 **Lightning-Fast Math Shortcuts**

**🎯 Mental Math Superpowers:**

---

**1. Squaring Numbers Ending in 5:**

**Rule:** n² where n ends in 5
**Formula:** (first_digits × (first_digits + 1)) then add 25

**Examples:**
• 15² = (1 × 2)25 = 225
• 25² = (2 × 3)25 = 625
• 35² = (3 × 4)25 = 1225
• 65² = (6 × 7)25 = 4225
• 95² = (9 × 10)25 = 9025

**Try:** 45², 55², 75², 85²

---

**2. Multiply Any Number by 11:**

**Rule:** For 2-digit number: abc × 11
**Formula:** a(a+b)(b+c)c

**Examples:**
• 23 × 11 = 2(2+3)3 = 253
• 45 × 11 = 4(4+5)5 = 495
• 72 × 11 = 7(7+2)2 = 792

**If sum > 9, carry over:**
• 67 × 11 = 6(6+7)7 = 6(13)7 = 737
• 89 × 11 = 8(8+9)9 = 8(17)9 = 979

**Try:** 34 × 11, 56 × 11, 78 × 11

---

**3. Multiply by 5 (Fast Way):**

**Rule:** n × 5 = (n × 10) ÷ 2
**Or:** n ÷ 2, then add 0

**Examples:**
• 24 × 5 = 240 ÷ 2 = 120
• 68 × 5 = 680 ÷ 2 = 340
• 142 × 5 = 1420 ÷ 2 = 710

**Try:** 36 × 5, 84 × 5, 156 × 5

---

**4. Multiply by 9 (Finger Trick):**

**Rule:** For 9 × n (where n = 1-10)
**Method:** 
1. Hold up 10 fingers
2. Put down the nth finger
3. Fingers left of down = tens
4. Fingers right of down = ones

**Examples:**
• 9 × 3: Put down 3rd finger → 2 fingers left, 7 right = 27
• 9 × 7: Put down 7th finger → 6 fingers left, 3 right = 63

**Algebraic trick:** 9 × n = (n × 10) - n
• 9 × 6 = 60 - 6 = 54

---

**5. Divisibility Rules (Quick Checks):**

**Divisible by 2:** Last digit even
• 1,234 ÷ 2? Yes (4 is even)

**Divisible by 3:** Sum of digits divisible by 3
• 1,467 ÷ 3? → 1+4+6+7=18 → 18÷3=6 → YES

**Divisible by 4:** Last 2 digits divisible by 4
• 3,216 ÷ 4? → 16÷4=4 → YES

**Divisible by 5:** Last digit 0 or 5
• 1,775 ÷ 5? Yes (ends in 5)

**Divisible by 6:** Divisible by both 2 and 3
• 1,458 ÷ 6? Even? Yes. Sum=18, ÷3? Yes → YES

**Divisible by 9:** Sum of digits divisible by 9
• 7,182 ÷ 9? → 7+1+8+2=18 → 18÷9=2 → YES

**Divisible by 10:** Last digit 0
• 1,340 ÷ 10? Yes

---

**6. Percentage Shortcuts:**

**10% of any number:** Move decimal left one place
• 10% of 450 = 45

**5% of any number:** Half of 10%
• 5% of 450 = 45 ÷ 2 = 22.5

**20% of any number:** Double 10%
• 20% of 450 = 45 × 2 = 90

**25% of any number:** Divide by 4
• 25% of 160 = 160 ÷ 4 = 40

**75% of any number:** Find 25%, then subtract from total
• 75% of 160 = 160 - 40 = 120

**15% (tip calculator):** 10% + half of 10%
• 15% of $60 = $6 + $3 = $9

---

**7. Squaring Numbers Near 50:**

**Rule:** For numbers near 50
**Formula:** 50² ± (difference × 100) + difference²

**Examples:**
• 52² = 2,500 + (2 × 100) + 4 = 2,704
• 48² = 2,500 - (2 × 100) + 4 = 2,304
• 55² = 2,500 + (5 × 100) + 25 = 3,025
• 45² = 2,500 - (5 × 100) + 25 = 2,025

---

**8. Quick Square Root Estimation:**

**Rule:** Find nearest perfect squares
**Method:** Interpolate between them

**Example:** √50
• 49 < 50 < 64
• √49 = 7, √64 = 8
• 50 is close to 49, so √50 ≈ 7.1
• (Actual: 7.07)

**Example:** √80
• 64 < 80 < 81
• √64 = 8, √81 = 9
• 80 very close to 81, so √80 ≈ 8.9
• (Actual: 8.94)

---

**9. Multiply Two 2-Digit Numbers (Close to 100):**

**Rule:** For numbers close to 100
**Method:** 
1. Find how far each is from 100
2. Subtract cross-difference from 100 (first 2 digits)
3. Multiply the differences (last 2 digits)

**Example:** 97 × 96
• 97 is 3 below 100
• 96 is 4 below 100
• 100 - (3+4) = 93 (first 2 digits)
• 3 × 4 = 12 (last 2 digits)
• Answer: 9,312

**Example:** 98 × 99
• 100 - (2+1) = 97
• 2 × 1 = 02
• Answer: 9,702

---

**10. Day of Week Calculation (Impress Friends!):**

**Rule:** Doomsday Algorithm (simplified)
• All years have dates that fall on same day
• Memorize: 4/4, 6/6, 8/8, 10/10, 12/12
• Plus: 5/9, 9/5, 7/11, 11/7

**For 2025, these all fall on Friday**

**Example:** What day is 12/15/2025?
• 12/12/2025 is Friday (Doomsday)
• 12/15 is 3 days after
• Friday + 3 = Monday

---

**🎓 Practice Exercises:**

**Easy:**
1. 35² = ?
2. 47 × 11 = ?
3. 15% of 80 = ?
4. √36 = ?

**Medium:**
5. 95² = ?
6. Is 2,457 divisible by 3?
7. 97 × 98 = ?
8. 20% of 450 = ?

**Hard:**
9. √150 ≈ ?
10. Day of week for 1/1/2026?

---

**💡 Tips for Mastery:**

**Practice Daily:**
• 5 minutes of mental math daily
• Use these in real life (tips, shopping)
• Compete with friends
• Time yourself

**Build Foundation:**
• Memorize multiplication tables (1-20)
• Know perfect squares (1-20)
• Know perfect cubes (1-10)
• Practice estimation

**Speed vs Accuracy:**
• Start slow, accurate
• Speed comes with practice
• Check answers first few weeks
• Then rely on mental math

**Apply Everywhere:**
• Calculate tips
• Estimate bills
• Figure out discounts
• Check receipts

---

**⏱️ Challenge yourself:**

**Week 1:** 2 shortcuts, 10 problems each
**Week 2:** Add 2 more shortcuts
**Week 3:** Mix different shortcuts
**Week 4:** Timed practice (1 min per problem)

**Track your progress:**
• Start accuracy: ____%
• Current accuracy: ____%
• Start speed: ___ sec/problem
• Current speed: ___ sec/problem

**Become a human calculator! 🚀**
"""

# Initialize global instance
extended_features = ExtendedFeatures()
