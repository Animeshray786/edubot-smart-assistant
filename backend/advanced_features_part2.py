"""
Extended Features Part 2 - Features 21-50
More advanced educational AI capabilities
"""

import random
from datetime import datetime, timedelta
import json

class AdvancedFeatures:
    """Features 21-50: Advanced educational tools"""
    
    def __init__(self):
        self.initialize_advanced_data()
    
    def initialize_advanced_data(self):
        """Initialize data for features 21-50"""
        
        # Feature 21: Citation Generator
        self.citation_styles = ["APA", "MLA", "Chicago", "Harvard", "IEEE"]
        
        # Feature 22: Research Paper Outliner
        self.paper_structures = {
            "research": ["Abstract", "Introduction", "Literature Review", "Methodology", "Results", "Discussion", "Conclusion"],
            "essay": ["Introduction", "Body Paragraphs (3-5)", "Counter-argument", "Conclusion"],
            "report": ["Executive Summary", "Introduction", "Findings", "Analysis", "Recommendations", "Conclusion"]
        }
        
        # Feature 23-50: Initialize data structures
        self.concentration_boosters = self._load_concentration_techniques()
        self.procrastination_fixes = self._load_procrastination_solutions()
        self.brain_foods = self._load_brain_foods_guide()
        self.sleep_optimization = self._load_sleep_guide()
        self.exercise_study_balance = self._load_exercise_guide()
    
    def _load_concentration_techniques(self):
        return [
            {"technique": "Pomodoro Power-Up", "duration": "25/5", "effectiveness": "95%"},
            {"technique": "Focus Music", "duration": "Continuous", "effectiveness": "80%"},
            {"technique": "Environment Design", "duration": "One-time setup", "effectiveness": "90%"},
            {"technique": "Mindfulness Break", "duration": "5 min", "effectiveness": "85%"},
            {"technique": "Physical Exercise", "duration": "20 min before", "effectiveness": "88%"}
        ]
    
    def _load_procrastination_solutions(self):
        return {
            "immediate": ["5-minute rule", "Just start with easiest part", "Remove all distractions"],
            "short_term": ["Break into tiny tasks", "Set up reward system", "Study buddy accountability"],
            "long_term": ["Understand root cause", "Build habits", "Professional help if needed"]
        }
    
    def _load_brain_foods_guide(self):
        return {
            "focus": ["Blueberries", "Green tea", "Dark chocolate (70%+)", "Avocados"],
            "memory": ["Fatty fish (salmon)", "Walnuts", "Eggs", "Pumpkin seeds"],
            "energy": ["Bananas", "Oats", "Nuts", "Greek yogurt"],
            "avoid": ["Processed sugar", "Energy drinks", "Heavy meals before study"]
        }
    
    def _load_sleep_guide(self):
        return {
            "optimal_hours": "7-9 hours for adults, 8-10 for teens",
            "best_time": "10 PM - 6 AM",
            "pre_sleep_routine": ["No screens 1hr before", "Read light material", "Cool room", "Consistent schedule"],
            "nap_guide": "20-min power nap or 90-min full cycle, avoid 30-60 min naps"
        }
    
    def _load_exercise_guide(self):
        return [
            "Morning: 20-30 min cardio boosts brain for 4-6 hours",
            "Study breaks: 5-10 min stretching/walking",
            "Before difficult topic: 10 min jumping jacks/running",
            "Don't: Heavy workout before important study session"
        ]
    
    # FEATURE 21: Citation Generator
    def generate_citation_guide(self, style="APA"):
        """Generate citation formatting guide"""
        return f"""
📚 **Citation Guide: {style} Style**

**🎯 {style} Citation Formats:**

**Book:**
{style == "APA" and "Author, A. A. (Year). Title of work. Publisher." or 
 style == "MLA" and "Author. Title. Publisher, Year." or
 "Author. Title. City: Publisher, Year."}

**Journal Article:**
{style == "APA" and "Author, A. A. (Year). Title of article. Journal Name, volume(issue), pages. DOI" or
 style == "MLA" and "Author. 'Article Title.' Journal Name, vol. #, no. #, Year, pp. #-#." or
 "Author. 'Article Title.' Journal Name vol. # (Year): pages."}

**Website:**
{style == "APA" and "Author. (Year). Title. Website Name. URL" or
 style == "MLA" and "Author. 'Page Title.' Website, Date, URL." or
 "Author. 'Page Title.' Website. Date Accessed. URL."}

**💡 Key Rules for {style}:**

**In-Text Citations:**
{style == "APA" and """
• (Author, Year)
• (Smith, 2023)
• (Smith & Jones, 2023) for 2 authors
• (Smith et al., 2023) for 3+ authors
• Direct quote: (Smith, 2023, p. 45)
""" or style == "MLA" and """
• (Author Page)
• (Smith 45)
• (Smith and Jones 45) for 2 authors
• (Smith et al. 45) for 3+ authors
""" or """
• Footnotes/endnotes numbered sequentially
• Full citation in note
"""}

**Reference List Formatting:**
• Alphabetical by author's last name
• Hanging indent (2nd line indented)
• Double-spaced
• Title: {"References" if style == "APA" else "Works Cited" if style == "MLA" else "Bibliography"}

**📱 Citation Tools:**
• Zotero (best for research management)
• Mendeley (PDF annotation + citations)
• EasyBib (quick citations)
• Citation Machine
• Your university library website

**✅ Citation Checklist:**
□ All sources cited in-text and in list
□ Format consistent throughout
□ All required information included
□ Alphabetical order maintained
□ Proper punctuation and capitalization
□ Hanging indents applied
□ Double-spaced
□ URLs working (if included)

**⚠️ Common Mistakes:**
❌ Inconsistent formatting
❌ Missing DOI or URL
❌ Wrong punctuation
❌ Forgetting to cite paraphrased content
❌ Using wrong author format
❌ Incorrect date format

**💡 Pro Tips:**
• Start citing as you research (don't wait!)
• Use citation management software
• Keep all source information
• Cite generously (when in doubt, cite)
• Check your professor's specific requirements
• Review examples in your textbook

**When to Cite:**
✅ Direct quotes
✅ Paraphrased ideas
✅ Statistics/data
✅ Specific theories
✅ Others' research findings
✅ Images/figures from sources

**No Citation Needed:**
• Common knowledge
• Your own ideas/analysis
• Your own research data
• General information

**Avoid Plagiarism: Always cite!** 📝
"""
    
    # FEATURE 22: Research Paper Outliner
    def generate_paper_outline(self, paper_type, topic):
        """Generate research paper outline"""
        structure = self.paper_structures.get(paper_type, self.paper_structures["essay"])
        
        return f"""
📄 **Research Paper Outline: {topic}**

**Type:** {paper_type.title()} Paper

**🎯 Standard Structure:**

""" + "\n\n".join([f"""
**{i+1}. {section}**
   • Purpose: [What this section accomplishes]
   • Length: [Suggested word count/pages]
   • Key points to cover:
     - Point 1
     - Point 2
     - Point 3
   • Sources needed: [Number of citations]
""" for i, section in enumerate(structure)]) + f"""

**📊 Detailed Breakdown:**

**Title Page**
• Title: Clear, concise, descriptive
• Your name, course, date
• Instructor name
• Institution

**Abstract** (150-250 words)
• Research question
• Methodology (briefly)
• Main findings
• Conclusion
• Keywords (3-5)

**1. Introduction** (10-15% of paper)
• Hook/attention grabber
• Background context
• Research question/thesis
• Significance of study
• Paper roadmap
• Word count: [Calculate based on total]

**2. Literature Review** (20-25%)
• Current state of research
• Key theories/concepts
• Gaps in existing research
• How your work fills gaps
• Synthesize, don't just summarize
• Group by themes, not by source

**3. Methodology** (15-20%)
• Research design
• Data collection methods
• Sample/participants
• Analysis approach
• Limitations
• Ethical considerations

**4. Results/Findings** (20-25%)
• Present data objectively
• Use tables/figures
• Organize by research questions
• No interpretation yet (save for discussion)

**5. Discussion** (20-25%)
• Interpret results
• Compare with literature
• Explain unexpected findings
• Implications
• Limitations
• Future research directions

**6. Conclusion** (5-10%)
• Restate research question
• Summarize key findings
• Final thoughts
• Call to action (if applicable)
• No new information!

**7. References**
• All cited sources
• Proper format
• Alphabetical order

**📝 Writing Tips:**

**Before Writing:**
□ Research thoroughly
□ Create detailed outline
□ Collect all sources
□ Set deadlines for each section

**During Writing:**
□ Write freely first (edit later)
□ One section at a time
□ Cite as you write
□ Take breaks

**After Writing:**
□ Let it sit for 24 hours
□ Read aloud
□ Check structure/flow
□ Verify citations
□ Proofread multiple times
□ Get peer feedback

**⏰ Timeline (for 10-page paper):**

**Week 1:** Research & outline (10 hours)
**Week 2:** Write Introduction & Literature Review (12 hours)
**Week 3:** Methodology & Results (10 hours)
**Week 4:** Discussion & Conclusion (8 hours)
**Week 5:** Revision & editing (6 hours)
**Week 6:** Final proofreading & formatting (4 hours)

**Total:** ~50 hours over 6 weeks

**💡 Quality Checklist:**

**Content:**
□ Clear thesis/research question
□ Logical flow and organization
□ Strong evidence/data
□ Critical analysis (not just description)
□ Original insights
□ All sources properly cited

**Style:**
□ Academic tone (formal, objective)
□ Clear, concise sentences
□ Varied sentence structure
□ Proper transitions
□ Active voice preferred
□ No contractions or slang

**Format:**
□ Correct citation style throughout
□ Consistent formatting
□ Page numbers
□ Headings/subheadings (if allowed)
□ Tables/figures labeled correctly
□ Meets length requirement

**💪 Your paper will be great! Start early!**
"""
    
    # FEATURES 23-50: Continued rapid-fire features
    
    def concentration_booster_menu(self):
        """Feature 23: Concentration techniques"""
        return """
🎯 **Ultimate Concentration Boosters**

**⚡ Instant Focus Techniques (< 5 min):**

**1. Box Breathing (2 min)**
• Inhale 4 counts
• Hold 4 counts
• Exhale 4 counts
• Hold 4 counts
• Repeat 5 times
**Effect:** Calms nervous system, increases alertness

**2. Cold Water Splash (30 sec)**
• Splash cold water on face
• Or hold ice cube for 30 sec
• Instant alertness boost
**Effect:** Activates dive reflex, increases focus

**3. Power Pose (2 min)**
• Stand like Superman/Wonder Woman
• Hands on hips, chest out
• Hold for 2 minutes
**Effect:** Increases confidence, reduces stress

**4. Desk Push-ups (1 min)**
• 10-15 desk push-ups
• Or 20 jumping jacks
• Gets blood flowing
**Effect:** Oxygen to brain, energy boost

**5. Eye Yoga (3 min)**
• Look up/down (10 times)
• Left/right (10 times)
• Circles (5 each direction)
• Close eyes, relax (30 sec)
**Effect:** Reduces eye strain, refreshes focus

---

**🎵 Focus Music Protocols:**

**For Deep Work:**
• Classical (Mozart, Bach)
• Lo-fi hip hop beats
• Binaural beats (40 Hz for focus)
• Nature sounds (rain, ocean)
• Video game soundtracks

**Volume:** 50-60% (background level)
**Duration:** Match Pomodoro (25 min on, 5 min off)

**Avoid:** Songs with lyrics in your language

---

**🧘 Mindfulness Micro-Breaks:**

**Every 25 Minutes:**
• Stand up
• Stretch arms overhead
• Roll shoulders back
• Take 3 deep breaths
• Resume work

**Every 2 Hours:**
• 5-minute walk
• Fresh air if possible
• Look at distant objects
• Hydrate

---

**📱 Digital Focus Tools:**

**Website Blockers:**
• Freedom (all platforms)
• Cold Turkey (Windows)
• SelfControl (Mac)
• StayFocusd (Chrome)

**Pomodoro Timers:**
• Forest (gamified, plants trees!)
• Be Focused (simple, effective)
• Tomato Timer (web-based)

**Ambient Sound:**
• Brain.fm (science-based)
• Noisli (customizable)
• A Soft Murmur (nature sounds)

---

**🍎 Quick Focus Foods:**

**Immediate Energy:**
• Handful of nuts (almonds, walnuts)
• Apple with peanut butter
• Dark chocolate (70%+ cacao)
• Green tea (L-theanine + caffeine)

**Sustained Focus:**
• Banana
• Oatmeal
• Greek yogurt
• Blueberries

**Avoid:**
• Candy/sweets (crash after 30 min)
• Heavy meals (blood to digestion)
• Too much caffeine (anxiety)

---

**🧠 Mental Warm-Up (5 min before study):**

1. **Brain Dump** (2 min)
   Write everything on your mind on paper

2. **Set Intention** (1 min)
   What exactly will I accomplish?

3. **Visualize Success** (1 min)
   See yourself completing the task

4. **Ready Signal** (30 sec)
   Deep breath, start timer, BEGIN

---

**⚡ Emergency Focus Recovery:**

**When You Can't Focus:**

**Physical:**
• 50 jumping jacks
• 2-minute plank
• Run up/down stairs
• Cold shower

**Mental:**
• Switch subjects
• Change location
• Study with someone
• Take longer break (15-30 min)

**Check:**
□ Am I tired? → Nap or sleep
□ Am I hungry? → Healthy snack
□ Am I worried? → Write it down
□ Am I bored? → Make it a game

---

**📊 Concentration Tracking:**

**Rate Your Focus (1-10):**
• Before session: ___
• After session: ___

**Log What Helped:**
• Time of day: ___
• Location: ___
• Technique used: ___
• Result: ___

**Pattern Recognition:**
• Best time: ___
• Best place: ___
• Best technique: ___

---

**💡 Long-Term Focus Building:**

**Week 1:** 15-minute focus sessions
**Week 2:** 25-minute sessions
**Week 3:** 45-minute sessions
**Week 4:** 60-minute sessions

**Track:** Consecutive days of practice
**Goal:** 30 days = new habit!

**Master focus, master everything! 🚀**
"""
    
    # Continue with more features...
    def procrastination_destroyer(self):
        """Feature 24: Anti-procrastination system"""
        return """
🚫 **Procrastination Destruction System**

**🎯 Understanding Your Procrastination:**

**Type 1: Perfectionist**
• Afraid it won't be perfect
• Never "right time" to start
**Fix:** Embrace "rough draft" mentality

**Type 2: Overwhelmed**
• Task seems too big
• Don't know where to start
**Fix:** Break into tiny pieces

**Type 3: Rebel**
• Don't like being told what to do
• React against deadlines
**Fix:** Reframe as personal choice

**Type 4: Pleasure Seeker**
• Want fun, not work
• Instant gratification
**Fix:** Gamify tasks, reward system

---

**⚡ The 5-Minute Rule (Most Powerful!):**

**Promise yourself:** Just 5 minutes
**Psychology:** Starting is hardest part
**Result:** Usually keep going after 5 min

**How:**
1. Set timer for ONLY 5 minutes
2. Give yourself permission to stop after
3. Start the task
4. 80% of time, you'll continue
5. If you stop, that's okay! Progress made.

---

**🎯 Tiny Task Breakdown:**

**Instead of:** "Write essay"
**Try:**
□ Open document (30 sec)
□ Write title (1 min)
□ Write one sentence (2 min)
□ Write thesis statement (5 min)
□ Outline 3 main points (5 min)
□ Write introduction (15 min)
□ First paragraph (15 min)

**Each tiny win = dopamine hit = motivation!**

---

**🎮 Gamification System:**

**Level 1 Tasks:** 5 XP
• Check email
• Organize desk
• Review notes

**Level 2 Tasks:** 15 XP
• Read one chapter
• Solve 10 problems
• Make flashcards

**Level 3 Tasks:** 30 XP
• Write essay section
• Complete project phase
• Study 2 hours focused

**Level 4 Boss Fight:** 100 XP
• Finish entire project
• Ace exam
• Complete course

**Rewards:**
• 100 XP = 30-min gaming break
• 500 XP = Movie night
• 1000 XP = Day off guilt-free

**Track on spreadsheet or app!**

---

**⏰ Strategic Scheduling:**

**Do Hardest Task:**
• First thing in morning
• When energy highest
• Before checking email/social

**Time Block:**
• 9-11 AM: Deep work (hardest task)
• 11-12 PM: Easier tasks
• 12-1 PM: Break/lunch
• 1-3 PM: Moderate difficulty
• 3-4 PM: Light work/review
• After 4 PM: Admin tasks

---

**👥 Accountability Hacks:**

**Study Buddy Check-ins:**
• Text each other goals (morning)
• Photo of progress (afternoon)
• Summary of what done (evening)

**Public Commitment:**
• Post goals on social media
• Tell friends/family
• Join study group
• Use accountability apps

**Stakes:**
• Bet money with friend
• Donate to charity if fail
• Lose privilege if don't complete

---

**🎯 Remove Temptations:**

**Physical:**
• Phone in another room
• Unplug TV
• Study at library
• Use website blockers

**Digital:**
• Log out of social media
• Delete time-wasting apps
• Use Focus mode
• Grayscale phone screen

**Environmental:**
• Clean desk (remove clutter)
• Face away from distractions
• Door closed
• "Do Not Disturb" sign

---

**💡 Reframing Techniques:**

**Instead of:** "I have to study"
**Think:** "I choose to study for my future"

**Instead of:** "This is boring"
**Think:** "How can I make this interesting?"

**Instead of:** "I'll do it later"
**Think:** "Future me will thank me if I do it now"

**Instead of:** "I can't do this"
**Think:** "I can't do this YET"

---

**🚨 Emergency Anti-Procrastination:**

**When you're stuck:**

1. **60-Second Decision**
   Count backwards 5-4-3-2-1, then START
   No thinking, just move

2. **Worst First**
   Do the thing you're avoiding most
   Everything else feels easy after

3. **Swiss Cheese Method**
   Poke holes in task (do any small part)
   Eventually task is done

4. **Temptation Bundling**
   Only do fun thing while doing hard thing
   Example: Favorite music only while studying

---

**📊 Procrastination Journal:**

**Daily Log:**
• Task I avoided: ___
• Why I avoided it: ___
• Consequence: ___
• How I felt: ___
• What would help: ___

**Weekly Review:**
• Pattern I notice: ___
• Biggest blocker: ___
• What worked: ___
• Next week strategy: ___

---

**✅ Anti-Procrastination Checklist:**

**Before Starting:**
□ Task broken into tiny steps
□ Distractions removed
□ Timer set (5 min minimum)
□ Reward planned
□ Accountability partner notified

**While Working:**
□ Phone away
□ Timer running
□ Taking breaks
□ Celebrating small wins

**After Completing:**
□ Reward claimed
□ Progress logged
□ Next task scheduled

---

**💪 Remember:**
• Procrastination is normal
• You're not lazy, you're stuck
• Start tiny, build momentum
• Progress > Perfection
• You've got this!

**Action beats overthinking! 🚀**
"""
    
    def brain_food_guide(self):
        """Feature 25: Brain-boosting nutrition"""
        return f"""
🧠 **Brain Food & Study Nutrition Guide**

**⚡ Best Foods for Studying:**

**🥇 Top 10 Brain Foods:**

**1. Blueberries** 🫐
• Benefit: Improves memory
• When: Morning/snack
• Serving: 1 cup
• Why: Antioxidants protect brain cells

**2. Fatty Fish** 🐟 (Salmon, Mackerel)
• Benefit: Builds brain cells
• When: Lunch/dinner
• Serving: 3-4 oz, 2x/week
• Why: Omega-3 fatty acids (60% of brain is fat!)

**3. Dark Chocolate** 🍫 (70%+ cacao)
• Benefit: Instant focus boost
• When: Pre-study (30 min before)
• Serving: 1-2 squares
• Why: Flavonoids + caffeine + theobromine

**4. Walnuts** 🌰
• Benefit: Memory enhancement
• When: Snack time
• Serving: Handful (1 oz)
• Why: Highest omega-3 of all nuts

**5. Green Tea** 🍵
• Benefit: Calm alertness
• When: Morning/afternoon
• Serving: 2-3 cups/day
• Why: L-theanine + caffeine combo

**6. Eggs** 🥚
• Benefit: Memory + mood
• When: Breakfast
• Serving: 1-2 eggs
• Why: Choline (makes acetylcholine)

**7. Avocados** 🥑
• Benefit: Sustained focus
• When: Lunch
• Serving: Half avocado
• Why: Healthy fats for blood flow

**8. Broccoli** 🥦
• Benefit: Brain protection
• When: Lunch/dinner
• Serving: 1 cup
• Why: Vitamin K, antioxidants

**9. Pumpkin Seeds** 🎃
• Benefit: Mental sharpness
• When: Snack
• Serving: Small handful
• Why: Zinc, magnesium, iron

**10. Oranges** 🍊
• Benefit: Prevents mental decline
• When: Morning/snack
• Serving: 1 medium orange
• Why: Vitamin C (one orange = daily need)

---

**📅 Optimal Study Day Meal Plan:**

**6:00 AM - Wake Up**
• Glass of water (rehydrate brain)

**7:00 AM - Brain-Boosting Breakfast**
• 2 scrambled eggs
• Oatmeal with blueberries
• Green tea
**Result:** Sustained energy 4-5 hours

**9:00 AM - Study Session 1**
• Water bottle on desk
• Already fueled!

**10:30 AM - Smart Snack**
• Handful of walnuts + almonds
• Apple slices
**Result:** 2-3 hours more focus

**12:30 PM - Power Lunch**
• Grilled salmon or chicken
• Quinoa or brown rice
• Broccoli/spinach salad
• Avocado
**Result:** Peak afternoon performance

**2:30 PM - Study Session 2**
• Green tea
• 2 squares dark chocolate (pre-study boost)

**4:00 PM - Energy Snack**
• Greek yogurt with berries
• Banana
**Result:** Sustained through evening

**6:30 PM - Dinner**
• Lean protein
• Sweet potato
• Mixed vegetables
• Small portion (don't overeat!)

**8:00 PM - Light Study Session**
• Herbal tea (chamomile for calm)
• No heavy foods

---

**🚫 Foods to AVOID Before/During Study:**

**1. Sugary Foods** 🍭
• Candy, cookies, soda
• Why: Spike then crash (30-60 min)
• Replace with: Fruit, dark chocolate

**2. Heavy/Fried Foods** 🍔
• Pizza, burgers, fries
• Why: Blood goes to digestion (brain fog)
• Replace with: Grilled proteins, salads

**3. Energy Drinks** 🥤
• Monster, Red Bull, etc.
• Why: Extreme crash, anxiety, jitters
• Replace with: Green tea, coffee (moderate)

**4. White Bread/Pasta** 🍞
• Simple carbs
• Why: Quick energy spike, then crash
• Replace with: Whole grains, quinoa

**5. Processed Snacks** 🍿
• Chips, crackers
• Why: Empty calories, no brain benefit
• Replace with: Nuts, seeds, fruit

---

**💧 Hydration is KEY:**

**Water Rules:**
• 8-10 glasses per day
• One glass every hour while studying
• Dehydration = 20% reduced cognitive function

**Signs You Need Water:**
• Headache
• Difficulty concentrating
• Fatigue
• Dry mouth

**Infused Water Ideas:**
• Lemon + mint
• Cucumber + lime
• Berries + basil
• Orange + ginger

---

**☕ Caffeine Strategy:**

**Best Practice:**
• Morning: 1-2 cups coffee/tea
• Afternoon: 1 cup green tea (if needed)
• Cut off: 2 PM (affects sleep)

**Caffeine Timing:**
• 30-60 min before peak focus needed
• NOT immediately upon waking (wait 90 min)
• With food (prevents jitters)

**Amount:**
• Max: 400mg/day (4 cups coffee)
• Sweet spot: 200mg (2 cups)

---

**🎯 Pre-Exam Nutrition:**

**Night Before:**
• Complex carbs + protein dinner
• No alcohol
• Herbal tea before bed
• No late-night snacking

**Exam Morning:**
• Wake 2 hours early
• Protein + complex carb breakfast
• Examples:
  - Eggs + oatmeal
  - Greek yogurt + granola + berries
  - Whole grain toast + peanut butter + banana

**During Exam:**
• Water bottle
• If allowed: Nuts, dark chocolate
• Avoid: Heavy snacks, sugary drinks

---

**🥗 Quick Brain-Healthy Snacks:**

**Sweet:**
• Apple + almond butter
• Banana + peanut butter
• Berries + Greek yogurt
• Dark chocolate + strawberries
• Dates + walnuts

**Savory:**
• Hummus + veggies
• Hard-boiled eggs
• Trail mix (nuts + dried fruit)
• Cheese + whole grain crackers
• Edamame

**Prep Time: < 5 minutes each**

---

**📊 Supplement Guide (Optional):**

**Evidence-Based:**
• **Omega-3** (fish oil): 1000mg/day
• **Vitamin D**: 2000 IU/day (if deficient)
• **B-Complex**: Supports energy
• **Magnesium**: Better sleep

**Popular (Less Evidence):**
• Ginkgo biloba
• Bacopa monnieri
• Rhodiola rosea

**Always consult doctor before supplements!**

---

**🍽️ Budget-Friendly Brain Foods:**

**Cheap & Effective:**
• Eggs ($3/dozen)
• Oatmeal ($4/large container)
• Bananas ($2/bunch)
• Peanut butter ($5/jar)
• Frozen berries ($4/bag)
• Canned tuna ($1/can)
• Spinach ($3/bag)
• Brown rice ($3/bag)

**Meal prep = Save money + time**

---

**✅ Daily Brain Nutrition Checklist:**

□ 8-10 glasses water
□ 1-2 servings fatty fish/week OR omega-3 supplement
□ Handful of nuts
□ 1-2 cups berries
□ Leafy greens
□ 2-3 cups green tea
□ Whole grains (not refined)
□ Limit sugar
□ No food 2 hours before bed
□ Protein with every meal

---

**💡 Remember:**
• Food = fuel for your brain
• Eat consistently (no skipping meals)
• 80/20 rule (80% healthy, 20% flexible)
• Prep meals weekly
• Eat before you're starving

**Feed your brain, ace your exams! 🧠✨**
"""
    
    def sleep_optimization_guide(self):
        """Feature 26: Sleep optimization for students"""
        return """
😴 **Ultimate Sleep Optimization for Students**

**🎯 The Sleep-Learning Connection:**

**Why Sleep Matters:**
• Memory consolidation (learning "locks in")
• 20-40% better test performance with good sleep
• Creativity increases
• Problem-solving improves
• Emotional regulation

**Sleep Deprivation Effects:**
• -10 IQ points per night of bad sleep
• 40% slower reaction time
• 30% worse decision making
• Increased stress/anxiety

---

**⏰ Optimal Sleep Schedule:**

**Hours Needed:**
• Ages 13-18: 8-10 hours
• Ages 18-25: 7-9 hours
• Ages 25+: 7-9 hours

**Best Sleep Time:**
• Sleep: 10 PM - 6 AM (ideal)
• Acceptable: 11 PM - 7 AM
• Not ideal: 12 AM - 8 AM
• Bad: 2 AM - 10 AM

**Why 10 PM matters:**
• 10 PM - 2 AM = deepest sleep
• Most growth hormone released
• Best memory consolidation

---

**🌙 Perfect Pre-Sleep Routine (90 min):**

**8:30 PM - Digital Sunset**
□ All screens off (phone, laptop, TV)
□ Blue light = cortisol = awake
□ Use apps: f.lux, Night Shift

**8:45 PM - Light Prep**
□ Pack bag for tomorrow
□ Lay out clothes
□ Review tomorrow's schedule
□ Brain dump worries on paper

**9:00 PM - Hygiene Ritual**
□ Warm shower (not hot)
□ Brush teeth
□ Face wash
□ Change into PJs

**9:15 PM - Calm Activities**
□ Read fiction (not textbooks!)
□ Light stretching/yoga
□ Meditation (10 min)
□ Gratitude journal

**9:45 PM - Bedroom Prep**
□ Room temperature: 60-67°F (16-19°C)
□ Darkness (blackout curtains or eye mask)
□ White noise or silence
□ Comfortable bedding

**10:00 PM - Lights Out**
□ Same time EVERY night (even weekends)
□ No phone in bed
□ If not asleep in 20 min, get up and read

---

**🛏️ Perfect Sleep Environment:**

**Temperature:**
• Ideal: 65°F (18°C)
• Cool = better sleep
• Wear socks if feet cold

**Darkness:**
• Zero light (cover all LEDs)
• Eye mask if needed
• Blackout curtains

**Sound:**
• Quiet or white noise
• Earplugs if noisy
• Apps: White Noise, Rain Rain

**Mattress/Pillow:**
• Comfortable and supportive
• Replace pillow every 1-2 years
• Mattress every 7-10 years

**Air Quality:**
• Fresh air (crack window)
• Plants (snake plant, peace lily)
• Air purifier if allergies

---

**☕ Caffeine Management:**

**Rules:**
• Last caffeine: 2 PM (strict!)
• Caffeine half-life: 5-6 hours
• 2 PM coffee = still 50% at 8 PM

**Alternatives After 2 PM:**
• Herbal tea (chamomile, peppermint)
• Decaf coffee
• Water with lemon
• Just water

---

**📱 Technology & Sleep:**

**Blue Light Problem:**
• Suppresses melatonin
• Tricks brain it's daytime
• Delays sleep 1-2 hours

**Solutions:**
• No screens 1 hour before bed
• Blue light glasses (if must use)
• Enable Night Mode/Night Shift
• Use red light for reading

**Phone Strategy:**
• Charge OUTSIDE bedroom
• Use alarm clock (not phone)
• If must have phone: Airplane mode

---

**😰 Can't Sleep? Try This:**

**If Awake 20+ Minutes:**
1. Get out of bed (don't lie there)
2. Go to another room
3. Read boring book (dim light)
4. Return when sleepy
5. Repeat if needed

**4-7-8 Breathing (Sleep in 2 min):**
• Inhale through nose: 4 counts
• Hold breath: 7 counts
• Exhale through mouth: 8 counts
• Repeat 4 times

**Body Scan Meditation:**
• Lie in bed
• Tense then relax each body part
• Start at toes, move up
• Usually asleep before finishing

---

**🎯 Strategic Napping:**

**Power Nap (20 min):**
• Best time: 1-3 PM
• Benefit: Alertness boost
• No grogginess

**Full Cycle (90 min):**
• Best time: Early afternoon
• Benefit: Memory consolidation
• Complete sleep cycle

**AVOID:**
• 30-60 min naps (wake during deep sleep = groggy)
• Naps after 4 PM (affects night sleep)
• Long naps when not needed

**Nap Strategy:**
• Set alarm (don't risk oversleep)
• Dark, quiet place
• Coffee nap: Drink coffee, then 20-min nap
  (Caffeine kicks in when you wake!)

---

**📚 Sleep & Studying:**

**Before Exam:**
• NEVER all-nighter before exam
• 1 hour sleep > 1 hour cramming
• Sleep = brain organizes info

**After Learning:**
• Sleep within 12 hours
• Memory consolidation happens during sleep
• Study → Sleep → Better recall

**Exam Day:**
• Same wake time (consistency)
• Full night sleep (7-9 hours)
• Wake 2 hours before exam

---

**🌅 Perfect Morning Routine:**

**As Soon As You Wake:**
□ Sunlight (open curtains immediately)
□ Or go outside for 10 min
□ Sunlight = sets circadian rhythm

**First 30 Minutes:**
□ Glass of water (rehydrate)
□ Light movement (stretch, walk)
□ Protein breakfast
□ No phone for 30 min (if possible)

**Consistency:**
• Same wake time every day
• Even weekends (max 1 hour difference)
• Body loves routine

---

**😴 Sleep Hygiene Rules:**

**DO:**
✅ Consistent schedule (even weekends)
✅ Exercise (but not 3 hours before bed)
✅ Sunlight exposure (morning)
✅ Dark, cool, quiet room
✅ Relaxing pre-sleep routine
✅ Use bed ONLY for sleep

**DON'T:**
❌ Caffeine after 2 PM
❌ Heavy meals 3 hours before bed
❌ Alcohol before bed (disrupts sleep quality)
❌ Screens 1 hour before bed
❌ Naps after 4 PM
❌ Worry in bed (brain dump earlier)

---

**🆘 Emergency Sleep Recovery:**

**After Bad Night:**
• Morning sunlight (resets clock)
• Light exercise
• 20-min nap (1-3 PM)
• Extra early to bed (10 PM)
• Hydrate well

**Consistent Bad Sleep? See Doctor:**
• Sleep apnea
• Insomnia
• Restless leg syndrome
• Other disorders

---

**📊 Sleep Tracking:**

**Track:**
• Bedtime
• Wake time
• Total hours
• Quality (1-10)
• Dreams?
• Morning energy (1-10)

**Apps:**
• Sleep Cycle
• Pillow
• Fitbit/Apple Watch

**Weekly Review:**
• Average hours
• Best nights (what did you do?)
• Worst nights (what went wrong?)
• Adjust routine

---

**💊 Natural Sleep Aids:**

**Safe:**
• Melatonin (0.5-3mg, 1 hour before bed)
• Magnesium glycinate (200-400mg)
• L-theanine (100-200mg)
• Chamomile tea

**Consult Doctor First:**
• Valerian root
• 5-HTP
• Prescription sleep aids

---

**✅ Sleep Quality Checklist:**

□ Same sleep/wake time daily
□ 7-9 hours total
□ Fall asleep in < 20 min
□ Wake 0-1 times/night
□ Feel refreshed in morning
□ Alert during day
□ No naps needed

**If 5+ checked: Good sleep! 🎉**
**If < 5: Adjust routine**

---

**🎓 Student Sleep Survival:**

**Exam Week:**
• Prioritize sleep over cramming
• 8 hours minimum
• Consistency crucial
• Review notes before bed (memory boost)

**All-Nighters:**
• AVOID if possible
• If must: Sleep after (not before)
• Recovery: 2-3 nights good sleep

**Dorm Room:**
• Eye mask + earplugs
• Roommate agreement (quiet hours)
• White noise machine
• Sleep schedule sync with roommate

---

**💡 Pro Tips:**

• **10-3-2-1-0 Rule:**
  - 10 hours before: No caffeine
  - 3 hours before: No food/alcohol
  - 2 hours before: No work
  - 1 hour before: No screens
  - 0: Times you hit snooze

• **Military Sleep Technique** (Fall asleep in 2 min):
  1. Relax face muscles
  2. Drop shoulders
  3. Relax arms
  4. Breathe out, relax chest
  5. Relax legs
  6. Clear mind 10 seconds
  7. Visualize peaceful scene

• **Sleep Debt:**
  Can't "catch up" on weekends
  Need consistent 7-9 hours

**Better sleep = Better grades! 😴✨**
"""
    
    def study_music_guide(self):
        """Feature 27: Study music science"""
        return """
🎵 **The Science of Study Music**

**🧠 How Music Affects Learning:**

**Benefits:**
• Improves mood (dopamine release)
• Reduces stress (cortisol reduction)
• Increases focus (masks distractions)
• Enhances memory (context-dependent learning)
• Boosts productivity (rhythm = pace)

**The Problem:**
• Wrong music = distraction
• Lyrics compete with language tasks
• Too loud = cognitive overload

---

**🎯 Best Music by Task Type:**

**📖 Reading/Writing (Language Tasks):**

**BEST:**
• Classical (Mozart, Bach, Vivaldi)
• Ambient (Brian Eno)
• Nature sounds (rain, ocean, forest)
• Binaural beats (40 Hz gamma)

**AVOID:**
• Music with lyrics in your language
• Energetic/changing tempos
• Favorite songs (too distracting)

**Recommendation:**
🎵 "Classical Study Music" playlist
🎵 Ludovico Einaudi
🎵 Max Richter

---

**🧮 Math/Problem-Solving:**

**BEST:**
• Instrumental electronic (study beats)
• Lo-fi hip hop
• Video game soundtracks
• Minimal techno

**Why:** Repetitive beats = sustained focus

**Recommendation:**
🎵 "Lo-fi Beats to Study To"
🎵 Chillhop Music
🎵 Minecraft soundtrack
🎵 Stardew Valley soundtrack

---

**💻 Coding/Programming:**

**BEST:**
• Synthwave
• Electronic (Tycho, Bonobo)
• Post-rock (Explosions in the Sky)
• Trance

**Why:** Rhythmic, predictable, energizing

**Recommendation:**
🎵 "Coding Focus" playlist
🎵 Tycho - Dive album
🎵 Boards of Canada

---

**🎨 Creative Tasks:**

**BEST:**
• Jazz (Miles Davis, Coltrane)
• Indie folk
• World music
• Varied genres

**Why:** Novel sounds = creative thinking

**Recommendation:**
🎵 "Creative Flow" playlist
🎵 Coffee shop jazz
🎵 Bossa nova

---

**📊 Memorization:**

**BEST:**
• Baroque music (60-70 BPM)
• Meditation music
• Alpha wave binaural beats

**Why:** Slower tempo = relaxed focus = better encoding

**Recommendation:**
🎵 Bach - Goldberg Variations
🎵 Pachelbel's Canon

---

**🎵 Music Platforms & Playlists:**

**Spotify:**
• "Deep Focus" (2M+ followers)
• "Peaceful Piano"
• "Instrumental Study"
• "Brain Food"

**YouTube:**
• "Lofi Girl" (24/7 livestream)
• "The Jazz Hop Café"
• "Greenred Productions"
• "Yellow Brick Cinema"

**Apple Music:**
• "Pure Focus"
• "Study Beats"

**Specialized Apps:**
• **Brain.fm** ($$$) - Science-based, 20% productivity boost
• **Focus@Will** ($$) - Neuroscience-designed
• **Noisli** - Custom sound mixer (free)
• **A Soft Murmur** - Nature sounds (free)

---

**🔊 Volume Guidelines:**

**Optimal Level:**
• 50-60% max volume
• Background level (can hear but not focus on it)
• Should be able to hear someone talk to you

**Too Loud Signs:**
• Can't hear thoughts
• Need to raise voice to talk
• Ear ringing/fatigue

**Decibel Range:**
• Ideal: 40-60 dB (quiet library)
• Max: 70 dB (normal conversation)
• Danger: 85+ dB (hearing damage)

---

**⏰ Music Strategy by Time:**

**Morning (High Energy):**
• Classical with strings
• Upbeat instrumentals
• Coffee shop sounds
• Volume: 60%

**Afternoon (Maintaining Focus):**
• Lo-fi hip hop
• Ambient electronic
• Video game scores
• Volume: 50%

**Evening (Calm Study):**
• Minimal piano
• Meditation music
• Nature sounds
• Volume: 40%

**Late Night (Alertness):**
• Moderate tempo instrumentals
• NOT calm music (don't want to sleep!)
• Volume: 55%

---

**🎧 Headphones vs Speakers:**

**Headphones:**
**Pros:**
• Immersive (blocks distractions)
• Better for noisy environments
• Binaural beats work better

**Cons:**
• Ear fatigue after 2 hours
• Can feel isolating
• Heat/pressure discomfort

**Best for:** Library, dorm, public spaces

---

**Speakers:**
**Pros:**
• More natural sound
• No ear fatigue
• Can move around

**Cons:**
• May disturb others
• External noise bleeds in

**Best for:** Private room, home study

---

**🧪 The Mozart Effect:**

**The Science:**
• Listening to Mozart may temporarily boost spatial reasoning
• Effect lasts ~15 minutes
• Not permanent IQ increase
• Works for any music you enjoy

**How to Use:**
• Listen to Mozart before exam (10-15 min)
• Or any music that puts you in good mood
• Boost confidence = better performance

**Best Pieces:**
• Sonata for Two Pianos in D major
• Symphony No. 40
• Piano Concerto No. 21

---

**🎼 Binaural Beats Explained:**

**What Are They:**
• Two slightly different frequencies (left/right ear)
• Brain creates third "beat"
• Supposed to entrain brainwaves

**Types:**
• **Delta (0.5-4 Hz):** Deep sleep
• **Theta (4-8 Hz):** Meditation, creativity
• **Alpha (8-13 Hz):** Relaxed focus
• **Beta (13-30 Hz):** Active thinking
• **Gamma (30-100 Hz):** Peak concentration

**For Studying:**
• Use **Beta** or **Gamma** frequencies
• Wear headphones (must!)
• 40 Hz = memory consolidation

**Caution:**
• Mixed scientific evidence
• May not work for everyone
• Try it, see if it helps you

---

**🎮 Video Game Soundtracks (Underrated!):**

**Why They Work:**
• Designed to maintain focus without distraction
• Often 10+ hours of content
• Energizing but not distracting

**Top Soundtracks:**
1. **The Legend of Zelda** - Adventurous
2. **Stardew Valley** - Calm, pleasant
3. **Minecraft** - Ambient, peaceful
4. **Final Fantasy** - Epic, motivating
5. **Animal Crossing** - Cozy, relaxing
6. **Skyrim** - Atmospheric
7. **Journey** - Emotional, beautiful
8. **FTL** - Electronic, focused
9. **Undertale** - Varied moods
10. **Ori and the Blind Forest** - Orchestral

---

**☕ Coffee Shop Sounds:**

**Why It Works:**
• Moderate ambient noise (70 dB)
• Social presence without interaction
• "Buzz" creates energy

**Apps:**
• Coffitivity (coffee shop sounds)
• I Miss My Café
• Noizio

**DIY:**
• YouTube "coffee shop ambience"
• Spotify "Coffee Shop" playlists

---

**🌧️ Nature Sounds:**

**Best for:**
• High stress
• Anxiety
• Overstimulation

**Options:**
• Rain (most popular)
• Ocean waves
• Forest sounds
• Thunderstorms
• River flowing
• White noise

**Apps:**
• Rain Rain
• Rainy Mood
• A Soft Murmur (mix multiple sounds)

---

**🎵 Lyric Music: When Is It OK?**

**CAN Work For:**
• Repetitive tasks
• Data entry
• Physical organization
• Commute/walking
• Warm-up period

**AVOID For:**
• Reading
• Writing
• Language learning
• Memorization
• Complex problem-solving

**Exception:**
• Music in language you don't understand
• Instrumental versions of lyric songs

---

**📅 Weekly Music Rotation:**

**Monday:** Energetic (Motivational start)
**Tuesday:** Classical (Serious focus)
**Wednesday:** Lo-fi (Mid-week groove)
**Thursday:** Nature sounds (Recharge)
**Friday:** Video game scores (Fun focus)
**Saturday:** Variety (Mix it up)
**Sunday:** Ambient (Calm review)

**Prevent:** Music fatigue/adaptation

---

**✅ Music Study Checklist:**

□ Playlist queued BEFORE study session
□ Phone on Do Not Disturb
□ Volume at 50-60%
□ Music matches task type
□ No lyrics for language tasks
□ Headphones charged (if using)
□ Backup playlist ready
□ Auto-play enabled (no interruptions)

---

**🚫 Common Music Mistakes:**

**1. Spending 20 min finding "perfect" playlist**
→ Pick one quickly, start studying

**2. Constantly skipping songs**
→ Choose longer mixes, let them play

**3. Using favorite music**
→ Too engaging, use neutral music

**4. Volume too loud**
→ Background level only

**5. Music with ads**
→ Breaks concentration, use premium or ad-free

**6. New music while studying**
→ Familiar music better (less cognitive load)

---

**🎯 Personalized Music Strategy:**

**Week 1: Experiment**
• Try different genres each day
• Note productivity/focus level
• Find what works for YOU

**Week 2: Refine**
• Use top 3 genres from Week 1
• Match genre to task type
• Create custom playlists

**Week 3: Optimize**
• Fine-tune volume
• Set time blocks
• Establish routine

**Week 4: Master**
• Music becomes automatic
• Triggers "study mode"
• Pavlovian conditioning!

---

**💡 Pro Tips:**

• **Study Ritual:** Same music = brain knows "study time"
• **Playlist Length:** 2+ hours (avoid repeats)
• **Start Before Studying:** Music on, then start (not reverse)
• **Silence OK:** Some people work best with no music
• **Test With Silence:** Important exams may be silent
• **Download Playlists:** Avoid buffering/internet issues

---

**🎼 Quick Recommendations by Mood:**

**Feeling Tired:**
→ Upbeat instrumentals, coffee shop sounds

**Feeling Anxious:**
→ Nature sounds, meditation music

**Feeling Unmotivated:**
→ Video game soundtracks, movie scores

**Feeling Overwhelmed:**
→ Classical, lo-fi hip hop

**Feeling Good:**
→ Whatever worked last time!

---

**Remember:** Music is tool, not magic. Best music = music that helps YOU focus! 🎵✨
"""

# Initialize global instance
advanced_features = AdvancedFeatures()
