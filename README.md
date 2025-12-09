# 📘 Study Coach  
### AI-Powered Personalized Study Planner

Study Coach is a full-stack web application that helps students organize courses, parse syllabi, and automatically generate personalized study plans using AI.

Built with:

- React + Vite (frontend)  
- Flask + SQLAlchemy (backend)  
- PDF parsing + LLM integration (coming soon)

---

## 🔧 Tech Stack

| Layer | Technologies |
|-------|--------------|
| Frontend | React, Vite, TypeScript, Axios |
| Backend | Python, Flask, SQLAlchemy, Flask-CORS |
| Database | SQLite (dev), PostgreSQL (later) |
| AI | LLM-powered study plan generation (upcoming) |

---

## ✨ Features

### ✅ Current
- Modern dashboard UI  
- Dark theme with responsive layout  
- Add and view courses  
- REST API for storing / retrieving course data  
- Clean backend architecture (routes, models, services)

### 🔮 In Development
- PDF upload and syllabus parsing  
- Topic extraction from documents  
- AI-generated study plan  
- Daily task breakdown  
- “Today’s Plan” suggestions  

### 🚀 Future Enhancements
- User authentication  
- Google Calendar sync  
- Progress analytics  
- AI practice question generator  

---

## 🗂 Project Structure
study-coach/
│
├── backend/
│ ├── app.py
│ ├── models.py
│ ├── routes/
│ ├── services/
│ └── requirements.txt
│
└── frontend/
├── src/
│ ├── App.tsx
│ ├── api/
│ └── components/
├── package.json
└── vite.config.ts


---

## 🛠️ Local Development

### Backend (Flask)



cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py

---

### Frontend (React + Vite)



cd frontend
npm install
npm run dev

---

## 🎯 Purpose

Study Coach aims to become an intelligent academic assistant that understands syllabi, deadlines, and pacing to generate optimized study schedules tailored to each student.

---

## 🤝 Contributing

This project is in early development. Suggestions and feature ideas are welcome.

---

## 📄 License

License will be added once project direction is finalized.