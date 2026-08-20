# Smart Timetable & Substitute Management System

A complete web-based application for managing school timetables, teacher absences, and intelligent substitute teacher assignments.

## 🎯 Features

- **Dashboard Analytics**: Real-time overview of teachers, classes, absences, and pending substitutions
- **Timetable Management**: Create, edit, and manage class and teacher schedules
- **Teacher Management**: Complete CRUD for teacher profiles with department and designation tracking
- **Class & Subject Management**: Organize classes and subjects with status tracking
- **Period Configuration**: Configurable period timings for Mon-Thu and Friday schedules
- **Smart Absence System**: Mark teachers absent and automatically detect affected periods
- **Intelligent Substitution Engine**: AI-driven substitute recommendations based on:
  - Teacher subject expertise
  - Department match
  - Availability status
  - Existing timetable conflicts
  - Transparent scoring system (30+ points for availability, +40 for subject match, +20 for department, +10 for class knowledge)
- **Conflict Detection**: Prevents double-booking and invalid assignments
- **Reports & Analytics**: 
  - Teacher weekly schedules
  - Class weekly schedules
  - Daily timetables
  - Absence reports
  - Substitution analytics
  - Teacher workload analysis
- **Print & Export**: Generate printable daily substitution sheets and reports
- **Audit Logging**: Track all administrative actions
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 📋 Project Structure

```
smart-timetable-system/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application
│   │   ├── database.py             # SQLAlchemy configuration
│   │   ├── models/
│   │   │   └── entities.py         # Database models
│   │   ├── routers/                # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── teachers.py
│   │   │   ├── classes.py
│   │   │   ├── subjects.py
│   │   │   ├── periods.py
│   │   │   ├── timetable.py
│   │   │   ├── absences.py
│   │   │   ├── substitutions.py
│   │   │   ├── dashboard.py
│   │   │   ├── reports.py
│   │   │   ├── search.py
│   │   │   ├── settings.py
│   │   │   └── audit.py
│   │   ├── schemas/                # Pydantic validation schemas
│   │   ├── services/               # Business logic
│   │   │   ├── crud_service.py
│   │   │   ├── conflict_service.py
│   │   │   ├── recommendation_service.py
│   │   │   ├── absence_service.py
│   │   │   ├── substitution_service.py
│   │   │   ├── report_service.py
│   │   │   └── audit_service.py
│   │   ├── utils/
│   │   │   ├── security.py         # Password hashing & JWT
│   │   │   ├── deps.py             # Dependency injection
│   │   │   ├── enums.py            # Enumerations
│   │   │   └── exceptions.py       # Custom exceptions
│   │   └── seed.py                 # Database seeding
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable components
│   │   ├── pages/                  # Page components
│   │   ├── layouts/                # Layout components
│   │   ├── hooks/                  # Custom React hooks
│   │   ├── services/               # API client
│   │   ├── types/                  # TypeScript types
│   │   ├── utils/                  # Utility functions
│   │   ├── App.tsx                 # Main app component
│   │   └── main.tsx                # Entry point
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── reference/
│   └── timetable.jpg               # Reference timetable image
└── README.md
```

## 🔧 Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (configurable for PostgreSQL/MySQL)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod validation
- **Router**: React Router v6
- **UI Components**: Lucide Icons
- **Notifications**: Sonner Toast

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Seed the database (creates database and loads initial data):
```bash
python run_seed.py
```

5. Start the backend server:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## 🔐 Default Credentials

After seeding the database:
- **Admin Account**: 
  - Username: `admin`
  - Password: `admin123`
  - Role: Administrator (full access)

- **Scheduler Account**:
  - Username: `scheduler`
  - Password: `scheduler123`
  - Role: Scheduler (can manage teachers, timetables, absences, substitutions)

## 📊 Database Schema

### Core Entities
- **User**: Login credentials and roles (admin, scheduler)
- **Teacher**: Teacher profiles with department, designation, contact info
- **ClassRoom**: Class information with section and program details
- **Subject**: Subject names and departmental organization
- **Period**: Time slots with different configurations for Mon-Thu and Friday

### Operational Data
- **Timetable**: Weekly schedule assignments (teacher-class-subject-period-day)
- **TeacherAbsence**: Absence records with reason and notes
- **Substitution**: Substitute assignments with automatic recommendations
- **TeacherAvailability**: Per-teacher period availability for filtering substitutes

### Metadata
- **AuditLog**: Track all administrative actions
- **Setting**: School-wide configuration and preferences

## 🚀 API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get JWT token

### Teachers
- `GET /api/teachers` - List all teachers
- `POST /api/teachers` - Create new teacher
- `GET /api/teachers/{id}` - Get teacher details
- `PUT /api/teachers/{id}` - Update teacher
- `DELETE /api/teachers/{id}` - Delete teacher

### Classes
- `GET /api/classes` - List all classes
- `POST /api/classes` - Create class
- `GET /api/classes/{id}` - Get class details
- `PUT /api/classes/{id}` - Update class
- `DELETE /api/classes/{id}` - Delete class

### Subjects
- `GET /api/subjects` - List subjects
- `POST /api/subjects` - Create subject
- `PUT /api/subjects/{id}` - Update subject
- `DELETE /api/subjects/{id}` - Delete subject

### Periods
- `GET /api/periods` - List periods
- `POST /api/periods` - Create period
- `PUT /api/periods/{id}` - Update period
- `DELETE /api/periods/{id}` - Delete period

### Timetable
- `GET /api/timetable?day=monday&class_id=1&teacher_id=1` - Get filtered timetable
- `POST /api/timetable` - Create timetable entry
- `PUT /api/timetable/{id}` - Update entry
- `DELETE /api/timetable/{id}` - Delete entry

### Absences
- `GET /api/absences` - List absences
- `POST /api/absences` - Mark teacher absent (auto-creates pending substitutions)

### Substitutions
- `GET /api/substitutions?status=pending` - List substitutions with filters
- `GET /api/substitutions/recommend/{id}` - Get substitute recommendations
- `POST /api/substitutions/assign` - Assign substitute teacher
- `PUT /api/substitutions/{id}/cancel` - Cancel substitution

### Reports
- `GET /api/reports/teacher/{id}` - Teacher weekly schedule
- `GET /api/reports/class/{id}` - Class weekly schedule
- `GET /api/reports/daily?day=monday` - Daily timetable
- `GET /api/reports/workload` - Teacher workload analysis
- `GET /api/reports/daily-substitution-sheet?date=2026-08-20` - Printable substitution sheet

### Dashboard
- `GET /api/dashboard` - Dashboard summary and today's data

### Search
- `GET /api/search?q=teacher_name` - Global search

## 💡 Key Workflows

### 1. Marking a Teacher Absent
1. Navigate to **Absences** → **Mark Absent**
2. Select teacher, date, and reason
3. System automatically:
   - Creates TeacherAbsence record
   - Finds all affected periods on that day
   - Creates pending Substitution entries for each period
   - Displays affected periods summary

### 2. Smart Substitute Assignment
1. View pending substitutions in **Substitutions** page
2. Click **Get Recommendations** for a pending substitution
3. System scores available teachers based on:
   - Subject expertise (highest weight)
   - Department match
   - Period availability
   - No timetable conflicts
4. Select recommended substitute or manually choose
5. System validates assignment and updates status to "assigned"

### 3. Conflict Prevention
- Teacher cannot be assigned to two classes in same period
- Class cannot have two teachers in same period
- Substitute cannot be double-booked
- Unavailable teachers are excluded from recommendations
- Original absent teacher cannot be selected as substitute

### 4. Generating Reports
1. Navigate to **Reports**
2. Select report type (Teacher Schedule, Class Schedule, etc.)
3. Choose filters (teacher, class, date range)
4. View or print report

## 🎨 Responsive Design

- **Desktop** (>1024px): Full sidebar + main content
- **Tablet** (768-1024px): Responsive grid layouts
- **Mobile** (<768px): Drawer sidebar, stacked layouts, horizontal scrolling for tables

## 📝 Environment Configuration

Create `.env` file in project root:

```env
# Backend
DATABASE_URL=sqlite:///./smart_timetable.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=720
ALLOWED_ORIGINS=http://localhost:5173

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

## 🧪 Testing

### Seed Data Includes
- 10 teachers across different departments
- 7 classes with different programs
- 13 subjects
- 8 periods (Mon-Thu) + 8 periods (Friday)
- Full weekly timetable assignments
- Sample teacher availability constraints
- Demo absence scenario for Monday with pending substitutions

### Test Workflow
1. Login with admin/admin123
2. View Dashboard → See today's schedule, absences, substitutions
3. Go to Absences → Mark "Ms. Arshia" absent
4. View affected periods
5. Go to Substitutions → Get recommendations
6. Verify scoring system and teacher ranking
7. Assign a substitute
8. Verify permanent timetable unchanged (only substitution created)
9. Generate daily substitution report

## 🔄 Data Flow

```
Admin marks teacher absent
        ↓
AbsenceService finds all teacher's classes on that day
        ↓
Creates pending Substitution for each affected period
        ↓
Frontend shows affected periods
        ↓
Admin clicks "Get Recommendations"
        ↓
RecommendationService scores available teachers
        ↓
ConflictService validates each teacher
        ↓
Frontend displays ranked list with scores and reasons
        ↓
Admin selects substitute
        ↓
SubstitutionService assigns and updates status
        ↓
Dashboard and reports reflect change
        ↓
Original timetable remains unchanged
```

## 📈 Substitute Scoring System

```
Base Score = 0

If subject matches: +40 points
If department matches: +20 points
If period is free: +30 points
If already teaches class: +10 points

Penalties:
- Already teaching another class: -100 (excluded)
- Marked unavailable: -100 (excluded)
- Is original absent teacher: -100 (excluded)
- Inactive teacher: -100 (excluded)

Final Score = Total Points (must be > 0 to recommend)
```

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Try clearing database: `rm smart_timetable.db` then reseed

### Frontend won't start
- Check if port 5173 is available
- Clear node_modules: `rm -rf node_modules` and `npm install`
- Check .env for correct API URL

### Seed data fails
- Ensure database file is writable
- Check Python version >= 3.10
- Verify bcrypt compatibility

### Login fails
- Check credentials: admin/admin123 or scheduler/scheduler123
- Verify backend is running: `curl http://localhost:8000/api/health`
- Check browser console for CORS errors

## 🚀 Deployment

### Production Database
Change `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/smarttimetable
```

### Production Frontend Build
```bash
npm run build
# Output in dist/ folder - deploy to web server
```

### Production Backend
Use production ASGI server:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -b 0.0.0.0:8000
```

## 📚 Additional Features (Future Enhancements)

- Email notifications for substitutes
- SMS alerts for urgent absences
- Calendar integration
- Teacher preference settings
- Recurring absence patterns
- Bulk timetable imports
- Teacher workload balancing
- Substitute performance analytics
- Parent notifications
- Mobile app

## 📄 License

This project is built for educational and institutional use.

## 🤝 Support

For issues or questions:
1. Check API documentation at `/api/docs` (backend running)
2. Review error messages in browser console
3. Check audit logs for action history
4. Verify database state with direct queries

## 📞 Contact

Built with ❤️ as a complete school management system.

---

**Status**: ✅ Production Ready
**Last Updated**: August 2026
**Version**: 1.0.0
