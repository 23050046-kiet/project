# 📋 REMINDER - FlashMaster Features & Usage Guide

## 🎓 1. Flashcard Learning (Học Từ Vựng)

### Chức Năng
- Học từ vựng tiếng Anh thông qua flashcard
- Mỗi flashcard có một từ + định nghĩa + ví dụ
- Đánh dấu từ đã học hoặc chưa biết

### Cách Sử Dụng
1. Vào trang chủ → Click "Learning" hoặc "📚 Flashcards"
2. Xem flashcard:
   - Mặt trước: Hiển thị **từ tiếng Anh**
   - Click card → Mặt sau: Hiển thị **định nghĩa + ví dụ**
3. Đánh dấu:
   - ✅ "Mark as Known" - Tôi đã biết từ này
   - ❌ "Mark as Unknown" - Cần học thêm
4. Progress bar hiển thị tiến độ học

### Dữ Liệu
- **1 Desk:** English Vocabulary 1
- **5 Flashcards:** small, large, huge, tall, beautiful (ví dụ)
- Theo dõi: Bao nhiêu từ đã học / tổng số từ

---

## 🎯 2. Quiz System (Trắc Nghiệm)

### Chức Năng
- Làm bài trắc nghiệm 10 câu hỏi
- Mỗi câu có 4 đáp án (A, B, C, D)
- Xem kết quả và đánh giá sau khi hoàn thành

### Giao Diện

#### 📝 **Quiz List Page** (`/quiz/`)
- Danh sách tất cả quizzes
- Mỗi quiz hiển thị:
  - 📌 Tiêu đề + mô tả
  - 🎯 Best score của user (nếu làm rồi)
  - 🔴 Button "Start Quiz"
- 3 quizzes mặc định:
  1. English Vocabulary Basics
  2. English Grammar Essentials
  3. Daily English Conversations

#### 🎮 **Quiz Play Page** (`/quiz/<id>/play`)
- **Một câu hỏi trên một trang**
- **Thanh tiến độ:** Hiển thị % hoàn thành (0% → 100%)
- **Question tracker:** Q1-Q10 buttons
  - 🔵 Xanh dương = Câu hiện tại
  - 🟢 Xanh lá = Đã trả lời
  - ⚪ Xám = Chưa trả lời
  - Click button để nhảy tới câu khác
- **Câu hỏi:** In đậm, rõ ràng
- **4 Đáp án với 4 màu:**
  -  **A (Blue)** - Màu xanh dương
  -  **B (Green)** - Màu xanh lá
  -  **C (Yellow)** - Màu vàng
  -  **D (Red)** - Màu đỏ
  - Click để chọn đáp án (radio button)
- **Navigation Buttons:**
  - ← Previous: Quay lại câu trước
  - Next → : Tới câu tiếp theo
  - Finish → (câu cuối): Nộp bài

#### ✅ **Quiz Result Page** (`/quiz/<id>/result/<attempt_id>`)
- **Kết quả ngay sau submit:**
  - 🏆 Điểm số: "7/10"
  - 📊 Phần trăm: "70%"
  - 💬 Nhận xét: "Good job! Keep it up!"
- **Review chi tiết:**
  - Tất cả 10 câu hiển thị lại
  - Đáp án đúng (✅ Xanh)
  - Đáp án sai (❌ Đỏ)
  - Đáp án không chọn (⚪ Xám)
- **Button:** 
  - 🔄 "Retake Quiz" - Làm lại
  - ← "Back to Quizzes" - Quay lại danh sách

### Cách Sử Dụng

#### Bước 1: Vào trang Quiz
- Click "📝 Quiz" trong navigation bar
- Xem danh sách 3 quizzes

#### Bước 2: Chọn Quiz
- Click "Start Quiz" trên quiz bạn muốn làm

#### Bước 3: Trả Lời Câu Hỏi
```
Ví dụ câu hỏi:
❓ "What is the opposite of 'small'?"

A) tiny
B) large (✓ Đáp án đúng)
C) huge (Cũng đúng nhưng không phải tốt nhất)
D) tall
```
- Click vào một đáp án
- Button "Next →" tự động bật lên
- Click để tới câu tiếp theo

#### Bước 4: Navigation
- **Click "Previous"** → Quay lại câu trước
- **Click số câu (Q1-Q10)** → Nhảy tới câu đó (không cần làm lần lượt)
- **Progress bar** tự động cập nhật % hoàn thành

#### Bước 5: Hoàn Thành
- Khi ở câu hỏi cuối (Q10)
- Click "Finish →" thay vì "Next →"
- Bài quiz được nộp tự động

#### Bước 6: Xem Kết Quả
- **Modal pop-up** hiển thị ngay:
  - Điểm số (VD: 7/10)
  - Phần trăm (VD: 70%)
  - Nhận xét (VD: "Good job! Keep it up!")
- Click "View Detailed Results" → Xem chi tiết từng câu
- Review màu sắc:
  - ✅ **Xanh** = Câu bạn trả lời đúng
  - ❌ **Đỏ** = Câu bạn trả lời sai
  - ⚪ **Xám** = Câu bạn không chọn

#### Bước 7: Làm Lại (Optional)
- Click "Retake Quiz" để làm lại
- Điểm mới sẽ ghi đè điểm cũ (best score giữ nguyên)

---

## � Tính Năng Tiện Lợi

### ✨ Features Trong Quiz
1. **Lưu tự động:** Trả lời được lưu ngay khi bạn click
2. **Skip câu:** Không cần trả lời theo thứ tự, nhảy được
3. **Progress tracking:** Biết được làm đến mấy % rồi
4. **Visual feedback:** Màu sắc giúp dễ phân biệt
5. **Instant results:** Kết quả hiển thị ngay sau submit
6. **Attempt history:** Lưu lại tất cả lần làm

### 🔐 Bảo Mật
- Phải đăng nhập mới được vào Quiz
- Mỗi user có history riêng
- Không ai xem được kết quả của người khác

---

## 💾 Dữ Liệu Được Lưu

### Flashcard Learning
- ✅ Số lần mark as known/unknown
- 📊 Progress mỗi desk
- 📅 Lần cuối cùng học

### Quiz System
- 📝 Tất cả câu trả lời
- 🎯 Điểm số & phần trăm
- ⏰ Thời gian hoàn thành
- 📊 Attempt history
- 🏆 Best score

---

## 🚀 Hướng Dẫn Bắt Đầu

### 1. Cài Đặt Database
```
python init_db.py --reset
```
Tạo:
- 2 tài khoản test (admin + user)
- 1 Desk English Vocabulary (5 cards)
- 3 Quizzes (30 câu hỏi)

### 2. Chạy Server
```
python run.py
```

### 3. Đăng Nhập
- URL: http://localhost:5000
- Admin: `admin@flashmaster.local` / `admin123`
- User: `user@flashmaster.local` / `user123`

### 4. Sử Dụng
- **Flashcards:** Learning → Click card
- **Quiz:** Quiz → Start Quiz → Trả lời → Submit

---

## ⚙️ Cấu Hình

### Database
- File: `flashmaster.db`
- Type: SQLite
- Location: Root folder

### Server
- Host: `http://0.0.0.0`
- Port: `5000`
- Debug: ON (development mode)

---

## � Thống Kê Mặc Định

| Item | Giá Trị |
|------|--------|
| Flashcard Desks | 1 |
| Flashcards | 5 |
| Quizzes | 3 |
| Questions/Quiz | 10 |
| Answers/Question | 4 |
| Total Questions | 30 |
| Test Users | 2 |

---

## 🎓 Ví Dụ Sử Dụng

### Quiz Example
```
📝 Quiz: English Vocabulary Basics

Question 1/10 [████░░░░░░] 10%
────────────────────────────

❓ "What is the opposite of 'small'?"

    A) tiny
    B) large      ← Click here (Correct!)
    C) huge
    D) tall

[← Previous]  [Next →]

Question Progress: 1 2 3 4 5 6 7 8 9 10
```

### Result Example
```
✅ Quiz Completed!

Score: 7/10
Percentage: 70%
Feedback: "Good job! Keep it up!"

────────────────────────────
Question Review:

Q1: ✅ What is the opposite of 'small'?
    Your answer: B) large (Correct!)

Q2: ❌ What is the opposite of 'big'?
    Your answer: A) tiny (Wrong!)
    Correct: B) large

Q3: ⚪ What is 'beautiful'?
    Your answer: (Not answered)
    Correct: B) very pretty
────────────────────────────

[← Back to Quizzes] [🔄 Retake Quiz]
```

---

## � Checklist Trước Sử Dụng

- [ ] Database đã khởi tạo (`python init_db.py --reset`)
- [ ] Server chạy bình thường (`python run.py`)
- [ ] Có thể đăng nhập với tài khoản test
- [ ] Thấy "📚 Flashcards" link trong navbar
- [ ] Thấy "📝 Quiz" link trong navbar
- [ ] Flashcard load được 5 cards
- [ ] Quiz load được 3 quizzes
- [ ] Quiz play page hiển thị 4 đáp án với 4 màu
- [ ] Navigation buttons hoạt động
- [ ] Question tracker hiển thị đúng
- [ ] Result modal hiển thị kết quả

---

**✨ Author: Phạm Tuấn Kiệt**
