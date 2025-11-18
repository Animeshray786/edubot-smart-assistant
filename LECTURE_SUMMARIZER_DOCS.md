# 📚 Lecture Note Summarizer - Feature Documentation

## Overview
The **Lecture Note Summarizer** is an AI-powered feature that automatically summarizes lecture notes and transcripts, extracts key concepts, and generates study questions.

---

## ✨ Features

### 1. **AI-Powered Summarization**
- Upload lecture notes or transcripts (minimum 50 words)
- Get concise bullet-point summaries
- Compression ratio analysis (shows how much content was condensed)
- Estimated read time vs review time

### 2. **Key Concept Extraction**
- Automatically identifies important terms
- Provides definitions for each concept
- Importance rating (high/medium/low)
- Track mastery level for each concept (0-100%)
- Review tracking with timestamps

### 3. **Study Questions Generation**
- Auto-generates 10+ study questions from content
- Multiple question types:
  - Short answer
  - Essay questions
  - List-based questions
- Difficulty levels: easy, medium, hard
- Related to specific concepts from lecture

### 4. **Beautiful HTML Formatting**
- Professional gradient design
- Color-coded elements
- Statistics dashboard
- Progress tracking
- Responsive layout

---

## 🚀 User Features

### Upload & Summarize
**Endpoint:** `POST /api/lecture/upload`

**Request Body:**
```json
{
  "title": "Introduction to Machine Learning",
  "content": "Your lecture transcript or notes (minimum 50 words)...",
  "subject": "Computer Science",
  "tags": "ML, AI, algorithms"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "note_id": 1,
    "title": "Introduction to Machine Learning",
    "summary": {
      "bullet_points": ["...", "..."],
      "word_count": 500,
      "compressed_words": 120,
      "compression_ratio": "76%"
    },
    "key_concepts": [
      {
        "term": "Machine Learning",
        "definition": "...",
        "importance": "high"
      }
    ],
    "study_questions": [
      {
        "id": 1,
        "question": "What is Machine Learning?",
        "type": "short_answer",
        "difficulty": "easy"
      }
    ],
    "html_summary": "<div>...</div>"
  }
}
```

### Get All Notes
**Endpoint:** `GET /api/lecture/notes?page=1&per_page=10&subject=Math`

**Response:**
```json
{
  "success": true,
  "data": {
    "notes": [...],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 50,
      "pages": 5
    }
  }
}
```

### Get Note Details
**Endpoint:** `GET /api/lecture/notes/{note_id}`

**Response:**
- Full note content
- Complete summary data
- All study questions
- All key concepts
- HTML formatted summary

### Answer Study Questions
**Endpoint:** `POST /api/lecture/questions/{question_id}/answer`

**Request Body:**
```json
{
  "answer": "Machine learning is a subset of AI..."
}
```

### Review Concepts
**Endpoint:** `POST /api/lecture/concepts/{concept_id}/review`

**Request Body:**
```json
{
  "mastery_level": 85
}
```

### Get Statistics
**Endpoint:** `GET /api/lecture/stats`

**Response:**
```json
{
  "success": true,
  "data": {
    "total_notes": 25,
    "total_questions": 250,
    "answered_questions": 180,
    "unanswered_questions": 70,
    "total_concepts": 200,
    "mastered_concepts": 120,
    "mastery_percentage": 60.0,
    "subjects": [
      {"subject": "Math", "count": 10},
      {"subject": "Physics", "count": 8}
    ]
  }
}
```

---

## 👨‍💼 Admin Features

### Access Admin Dashboard
**URL:** `http://localhost:5000/admin/lecture/`

**Features:**
- Real-time statistics overview
- Notes timeline chart (30 days)
- Popular subjects chart
- Top users chart
- Notes management table
- Filter and search functionality
- Bulk operations

### Admin Overview
**Endpoint:** `GET /admin/lecture/overview`

**Response:**
```json
{
  "success": true,
  "data": {
    "total_stats": {
      "total_notes": 100,
      "total_users": 25,
      "total_questions": 1000,
      "total_concepts": 800,
      "recent_notes_7d": 15
    },
    "averages": {
      "avg_word_count": 450,
      "avg_questions_per_note": 10,
      "avg_concepts_per_note": 8
    },
    "engagement": {
      "answer_rate": 72.5,
      "answered_questions": 725,
      "unanswered_questions": 275,
      "mastery_rate": 65.0,
      "mastered_concepts": 520
    },
    "status_breakdown": [...],
    "subject_breakdown": [...]
  }
}
```

### Get All Notes (Admin)
**Endpoint:** `GET /admin/lecture/notes?page=1&status=processed&subject=Math&search=query`

**Query Parameters:**
- `page`: Page number
- `per_page`: Items per page (default: 20)
- `status`: Filter by status (processed/pending/failed)
- `subject`: Filter by subject
- `user_id`: Filter by user
- `search`: Search in title and tags

### Update Note Status
**Endpoint:** `PUT /admin/lecture/notes/{note_id}/status`

**Request Body:**
```json
{
  "status": "processed"
}
```

### Get User's Notes
**Endpoint:** `GET /admin/lecture/users/{user_id}/notes`

### Analytics Endpoints

#### Notes Timeline
**Endpoint:** `GET /admin/lecture/analytics/timeline?days=30`

#### Popular Subjects
**Endpoint:** `GET /admin/lecture/analytics/popular-subjects?limit=10`

#### Top Users
**Endpoint:** `GET /admin/lecture/analytics/top-users?limit=10`

### Bulk Delete
**Endpoint:** `POST /admin/lecture/bulk-delete`

**Request Body:**
```json
{
  "note_ids": [1, 2, 3]
}
```
OR
```json
{
  "status": "failed",
  "older_than_days": 90
}
```

### Export Data
**Endpoint:** `GET /admin/lecture/export?format=json`

**Formats:** `json` or `csv`

---

## 🎨 Frontend Integration

### Chat Interface
Users can trigger the feature by typing:
- "summarize"
- "lecture notes"
- "note summary"

The bot will respond with instructions and a link to the feature.

### Dashboard Integration
Add a new section to user dashboard:

```html
<div class="dashboard-section">
  <h3>📚 Lecture Notes</h3>
  <button onclick="uploadLecture()">Upload New Note</button>
  <div id="recentNotes"></div>
</div>
```

### Sample JavaScript
```javascript
async function uploadLecture() {
  const response = await fetch('/api/lecture/upload', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: document.getElementById('title').value,
      content: document.getElementById('content').value,
      subject: document.getElementById('subject').value,
      tags: document.getElementById('tags').value
    })
  });
  
  const data = await response.json();
  if (data.success) {
    // Display the formatted HTML summary
    document.getElementById('summary').innerHTML = data.data.html_summary;
  }
}
```

---

## 📊 Database Schema

### `lecture_notes` Table
```sql
CREATE TABLE lecture_notes (
    note_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    original_content TEXT NOT NULL,
    summary_data JSON,
    subject VARCHAR(100),
    tags VARCHAR(500),
    word_count INTEGER,
    status VARCHAR(20) DEFAULT 'processed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### `study_questions` Table
```sql
CREATE TABLE study_questions (
    question_id INTEGER PRIMARY KEY,
    note_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50),
    difficulty VARCHAR(20),
    related_concept VARCHAR(200),
    user_answer TEXT,
    is_answered BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    answered_at DATETIME,
    FOREIGN KEY (note_id) REFERENCES lecture_notes(note_id)
);
```

### `key_concepts` Table
```sql
CREATE TABLE key_concepts (
    concept_id INTEGER PRIMARY KEY,
    note_id INTEGER NOT NULL,
    term VARCHAR(200) NOT NULL,
    definition TEXT NOT NULL,
    importance VARCHAR(20),
    mastery_level INTEGER DEFAULT 0,
    times_reviewed INTEGER DEFAULT 0,
    last_reviewed DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (note_id) REFERENCES lecture_notes(note_id)
);
```

---

## 🔒 Security

### Authentication Required
All endpoints except admin endpoints require user login:
- `@login_required` decorator

### Admin Endpoints
Admin-only endpoints require admin role:
- `@admin_required` decorator

### Data Validation
- Minimum content length: 50 characters
- Maximum file size: 16MB
- Input sanitization for XSS prevention
- SQL injection protection via SQLAlchemy ORM

---

## 🚀 Testing

### Test Upload
```bash
curl -X POST http://localhost:5000/api/lecture/upload \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Lecture",
    "content": "This is a test lecture about machine learning. Machine learning is defined as a subset of artificial intelligence. It involves training algorithms on data. The key concepts include supervised learning, unsupervised learning, and reinforcement learning. Neural networks are important for deep learning.",
    "subject": "Computer Science",
    "tags": "ML, AI, test"
  }'
```

### Test Summarization
The summarizer will:
1. Extract 10 key sentences
2. Generate 5-8 key concepts
3. Create 10 study questions
4. Calculate statistics
5. Return formatted HTML

---

## 📈 Performance

### Processing Time
- Average: 1-3 seconds for 500-word content
- Large documents (2000+ words): 3-5 seconds

### Database Queries
- Optimized with SQLAlchemy relationships
- Pagination for large datasets
- Indexed on `user_id`, `created_at`, `status`

### Scalability
- Can handle 1000+ notes per user
- Efficient JSON storage for summary data
- Background processing possible for very large documents

---

## 🎯 Future Enhancements

1. **PDF Upload Support**
   - Extract text from PDF files
   - Maintain formatting

2. **Audio Transcription**
   - Upload lecture recordings
   - Automatic speech-to-text
   - Timestamp markers

3. **Collaborative Notes**
   - Share notes with classmates
   - Collaborative editing
   - Comments and annotations

4. **Smart Search**
   - Search across all notes
   - Semantic search
   - Concept-based retrieval

5. **Export Options**
   - Export as PDF with formatting
   - Export as Markdown
   - Export to note-taking apps

6. **Advanced Analytics**
   - Learning progress tracking
   - Time spent on concepts
   - Predicted exam performance

7. **Integration with Calendar**
   - Link notes to class schedule
   - Automatic reminders for review
   - Spaced repetition algorithm

---

## 📝 Implementation Status

✅ **Completed:**
- AI summarization engine
- Key concept extraction
- Study question generation
- User API endpoints
- Admin dashboard
- Database models
- HTML formatting
- Statistics tracking

🔄 **In Progress:**
- Frontend UI integration
- Mobile responsiveness
- PDF upload support

📋 **Planned:**
- Audio transcription
- Collaborative features
- Advanced analytics

---

## 🆘 Support

### Common Issues

**Issue:** "Content too short" error
**Solution:** Ensure content is at least 50 characters

**Issue:** Summary not generating
**Solution:** Check content has proper sentences with punctuation

**Issue:** No concepts extracted
**Solution:** Add more descriptive content with definitions

### Contact
For bugs or feature requests, contact the development team.

---

**Built with ❤️ by EduBot Team**
