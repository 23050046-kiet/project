# FlashMaster - Ứng Dụng Học Tập Bằng Flashcard

## 📋 Mục Đích
FlashMaster là một ứng dụng web giúp người dùng học tiếng Anh thông qua:
1. **Learning Vocabulary** - Học từ vựng bằng flashcard
2. **Quiz** - Kiểm tra kiến thức bằng bài trắc nghiệm

---

## 🏗️ Kiến Trúc Dự Án

### Cấu Trúc Thư Mục
```
vibecode-python/
├── app.py                 # Flask app factory
├── config.py             # Cấu hình (database, secret key)
├── models.py             # Database models
├── run.py                # Entry point
├── init_db.py            # Script khởi tạo database
├── seed_quizzes.py       # Script tạo dữ liệu quiz
│
├── routes/               # Các route của ứng dụng
│   ├── __init__.py
│   ├── main.py          # Trang chính, dashboard
│   ├── auth.py          # Đăng nhập, đăng ký
│   ├── cards.py         # Flashcard learning
│   ├── admin.py         # Admin dashboard
│   └── quiz.py          # Quiz routes (NEW)
│
├── templates/           # HTML templates
│   ├── base.html        # Base layout
│   ├── welcome.html     # Trang chào mừng
│   ├── dashboard.html   # Dashboard người dùng
│   ├── cards/
│   │   ├── index.html   # Danh sách flashcard
│   │   └── play.html    # Học flashcard
│   ├── auth/
│   │   ├── login.html   # Đăng nhập
│   │   └── register.html # Đăng ký
│   ├── admin/           # Admin pages
│   └── quiz/            # Quiz pages (NEW)
│       ├── index.html   # Danh sách quiz
│       ├── play.html    # Làm quiz
│       └── result.html  # Kết quả chi tiết
│
├── static/              # CSS, JS
│   ├── css/app.css
│   └── js/app.js
│
└── requirements.txt     # Python dependencies
```

---

## 🗄️ Database Schema

### Core Models

#### **User**
- `id` (PK)
- `name` - Tên người dùng
- `email` - Email (unique)
- `password_hash` - Mật khẩu hash
- `is_admin` - Là admin hay không
- `created_at, updated_at`
- **Relations**: card_reviews, quiz_attempts

#### **Desk** (Bộ flashcard)
- `id` (PK)
- `name_en` - Tên bộ flashcard
- `image_path` - Đường dẫn ảnh
- `created_at, updated_at`
- **Relations**: cards

#### **Card** (Thẻ học)
- `id` (PK)
- `desk_id` (FK) - Thuộc bộ nào
- `question` - Câu hỏi
- `answer` - Câu trả lời
- `example` - Ví dụ
- `order` - Thứ tự
- `created_at, updated_at`
- **Relations**: card_reviews

#### **CardReview** (Lịch sử học)
- `id` (PK)
- `user_id` (FK)
- `card_id` (FK)
- `is_correct` - Trả lời đúng hay sai
- `review_stage` - Giai đoạn học
- `next_review_at` - Khi nào học tiếp
- `created_at, updated_at`

#### **Quiz** (Bài quiz)
- `id` (PK)
- `title` - Tên quiz
- `description` - Mô tả
- `category` - Danh mục
- `created_at, updated_at`
- **Relations**: questions, attempts

#### **QuizQuestion** (Câu hỏi trong quiz)
- `id` (PK)
- `quiz_id` (FK)
- `question_text` - Nội dung câu hỏi
- `question_type` - Loại (multiple_choice, fill_blank)
- `order` - Thứ tự (1-10)
- `created_at`
- **Relations**: answers, user_answers

#### **QuizAnswer** (Đáp án)
- `id` (PK)
- `question_id` (FK)
- `answer_text` - Nội dung đáp án
- `is_correct` - Là đáp án đúng không
- `order` - Thứ tự (A, B, C, D)

#### **UserQuizAnswer** (Câu trả lời của user)
- `id` (PK)
- `user_id` (FK)
- `question_id` (FK)
- `selected_answer_id` (FK)
- `is_correct` - Trả lời có đúng không
- `created_at`

#### **QuizAttempt** (Lần làm quiz)
- `id` (PK)
- `user_id` (FK)
- `quiz_id` (FK)
- `score` - Điểm số
- `total_questions` - Tổng câu hỏi
- `percentage` - Tỉ lệ (%)
- `started_at, completed_at`

---

## 🔄 Workflow Hệ Thống

### 1. Learning Vocabulary Flow
```
User Login
    ↓
Dashboard (Xem các desks)
    ↓
Select Desk (Chọn bộ flashcard)
    ↓
CardReview (Học từng card)
    → Xem câu hỏi/đáp án
    → Đánh dấu hoàn thành
    → Lưu CardReview record
    ↓
Repeat (Câu tiếp theo hoặc hoàn thành)
```

### 2. Quiz Flow
```
User Login
    ↓
Click "📝 Quiz" (Navigation)
    ↓
Quiz List (/quiz/)
    → Hiển thị 3 quizzes
    → Hiển thị best score, attempts
    ↓
Start Quiz (/quiz/<id>/play)
    ↓
Display Question (One per page)
    → Question text + 4 answers
    → Navigation buttons (Prev/Next)
    → Progress tracker (Q1-Q10)
    ↓
User Selects Answer
    → Lưu vào userAnswers object
    → Auto-save (không submit to server)
    ↓
Click "Next" → Display next question
    OR
Click "Finish" (on last question) → Submit
    ↓
Submit Quiz (/quiz/<id>/submit) [POST]
    → Backend tính điểm
    → Tạo UserQuizAnswer records
    → Tạo QuizAttempt record
    → Return: score, total, percentage, attempt_id
    ↓
Show Result Modal
    → Điểm số + Phần trăm
    → Feedback message
    → "View Detailed Results" button
    ↓
View Result Page (/quiz/<id>/result/<attempt_id>)
    → Hiển thị tất cả câu hỏi
    → Highlight correct/wrong answers
    → Color coding:
        - GREEN = Correct answer
        - RED = Your wrong answer
        - GRAY = Not selected
    ↓
Options:
    → Retake Quiz
    → Back to All Quizzes
```

---

## 💻 Logic Code Chi Tiết

### Quiz Play Logic (quiz/play.html)

#### Frontend - JavaScript
```javascript
// 1. Data Structure
const quizData = [
  { question: {...}, answers: [...] },
  { question: {...}, answers: [...] },
  ...
]

// 2. User Answers Storage
let userAnswers = {};  // { question_id: answer_id }

// 3. Display Question
function displayQuestion(index) {
  - Cập nhật question number
  - Cập nhật progress bar
  - Render radio buttons cho answers
  - Hiển thị button trạng thái (Previous/Next/Finish)
  - Cập nhật question tracker
}

// 4. Navigation
- Previous: displayQuestion(index - 1)
- Next/Finish: 
  - Nếu index < total - 1: displayQuestion(index + 1)
  - Nếu index == total - 1: submitQuiz()

// 5. Submit Quiz
async function submitQuiz() {
  - Gửi POST /quiz/<id>/submit
  - Payload: { answers: { q1: a1, q2: a2, ... } }
  - Nhận response: { score, total, percentage, attempt_id }
  - Hiển thị modal kết quả
  - Set button link → /quiz/<id>/result/<attempt_id>
}
```

#### Backend - routes/quiz.py
```python
# 1. GET /quiz/<id>/play
@quiz_bp.route('/<int:quiz_id>/play')
def play(quiz_id):
  - Lấy quiz + questions + answers
  - Chuẩn bị quiz_data (dict structure)
  - Render template với quiz_data

# 2. POST /quiz/<id>/submit
@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
def submit(quiz_id):
  - Nhận JSON: { answers: {...} }
  - Loop qua mỗi question:
    - Kiểm tra answer có đúng không
    - Tăng score nếu đúng
    - Tạo UserQuizAnswer record
  - Tính percentage: (score / total) * 100
  - Tạo QuizAttempt record
  - Return JSON: { score, total, percentage, attempt_id }

# 3. GET /quiz/<id>/result/<attempt_id>
@quiz_bp.route('/<int:quiz_id>/result/<int:attempt_id>')
def result(quiz_id, attempt_id):
  - Lấy attempt + questions
  - Collect user answers (UserQuizAnswer)
  - Hiển thị kết quả chi tiết
```

---

## 🎯 Dữ Liệu Mẫu

### Quizzes (3 quizzes)
1. **English Vocabulary Basics** (10 câu)
   - Từ vựng cơ bản
   - Opposites, synonyms, meanings

2. **English Grammar Essentials** (10 câu)
   - Ngữ pháp
   - Present perfect, conditional, passive voice

3. **Daily English Conversations** (10 câu)
   - Hội thoại hàng ngày
   - Greetings, thanks, polite expressions

### Learning Vocabulary (1 desk)
- **English Vocabulary** - 5 cards mẫu

---

## 🚀 Cách Chạy

### 1. Cài Đặt
```bash
pip install -r requirements.txt
```

### 2. Khởi Tạo Database
```bash
python init_db.py --reset
```

### 3. Chạy Server
```bash
python run.py
```

### 4. Truy Cập
- URL: http://localhost:5000
- Đăng nhập: admin@flashmaster.local / admin123

---

## 🎨 Giao Diện

### Navigation Bar
```
FlashMaster
├── Dashboard (nếu logged in)
├── 📚 Learn (Flashcard)
├── 📝 Quiz (NEW)
└── Logout
```

### Quiz Page Structure
```
┌─────────────────────────────────────┐
│ Quiz Title                    ← Back │
├─────────────────────────────────────┤
│ Progress: Question 1 / 10      50%  │
│ ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
├─────────────────────────────────────┤
│ Question 1                          │
│ What is the opposite of "big"?      │
│                                     │
│ ○ small      ← Selected             │
│ ○ large                             │
│ ○ huge                              │
│ ○ tall                              │
│                                     │
│ [← Previous] [Next →]               │
├─────────────────────────────────────┤
│ [1] [2] [3] [4] [5]...             │
│  ✓   ✓   •   ○   ○                  │
│                                     │
│ ✓ = Answered  • = Current  ○ = Not │
└─────────────────────────────────────┘
```

### Result Page
```
┌─────────────────────────────────────┐
│ Quiz Results                        │
├─────────────────────────────────────┤
│ Score: 8/10                         │
│ Percentage: 80%                     │
│ 🎉 Excellent work!                  │
├─────────────────────────────────────┤
│ Question 1 ✓ CORRECT                │
│ ✓ Correct Answer (GREEN)            │
│ ○ Other options (GRAY)              │
│                                     │
│ Question 2 ✗ WRONG                  │
│ ✓ Correct Answer (GREEN)            │
│ ✗ Your Answer (RED)                 │
│ ○ Other options (GRAY)              │
├─────────────────────────────────────┤
│ [Retake Quiz] [All Quizzes]         │
└─────────────────────────────────────┘
```

---

## 📊 Thống Kê & Features

### Quiz Statistics
- Số lần làm quiz
- Điểm cao nhất
- Lịch sử attempts
- Tỉ lệ thành công

### Color Coding System
- **Green (#198754)** - Câu trả lời đúng
- **Red (#dc3545)** - Câu trả lời sai
- **Gray (#6c757d)** - Không chọn
- **Blue (#007bff)** - Câu hiện tại
- **Light Green** - Background câu đúng

---

## 🔐 Authentication

### User Roles
- **Admin** - Có thể quản lý desks, cards
- **User** - Có thể học và làm quiz

### Protected Routes
- `/dashboard` - Yêu cầu login
- `/cards/play` - Yêu cầu login
- `/quiz/*` - Yêu cầu login

---

## 📝 Notes

- Quiz data lưu tạm thời trong `userAnswers` object, không submit đến server cho đến khi user finish
- Các answer được serialize thành dictionary trước khi lưu vào template
- Progress bar và question tracker update real-time khi user chọn answer
- Result page hiển thị chi tiết từng câu hỏi với color coding

---

**Version**: 1.0
**Last Updated**: December 2, 2025
