// src/App.tsx
import { useEffect, useState, FormEvent } from "react";
import { api } from "./api/client";

interface Course {
  id: number;
  name: string;
  termStart: string;
  termEnd: string;
  mainExamDate: string | null;
}

function App() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [name, setName] = useState("");
  const [termStart, setTermStart] = useState("");
  const [termEnd, setTermEnd] = useState("");
  const [mainExamDate, setMainExamDate] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Course[]>("/courses")
      .then((res) => setCourses(res.data))
      .finally(() => setLoading(false));
  }, []);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    if (!name || !termStart || !termEnd) return;

    await api.post("/courses", {
      name,
      termStart,
      termEnd,
      mainExamDate: mainExamDate || null,
    });

    const res = await api.get<Course[]>("/courses");
    setCourses(res.data);

    setName("");
    setTermStart("");
    setTermEnd("");
    setMainExamDate("");
  };

  return (
    <div className="app-root">
      <div className="app-shell">
        <header className="app-header">
          <div>
            <h1 className="app-title">Study Coach</h1>
            <p className="app-subtitle">
              Track courses and generate smart study plans later. For now, set up your classes.
            </p>
          </div>
          <div className="app-pill">Beta</div>
        </header>

        <main className="app-main">
          <section className="panel panel-form">
            <h2 className="panel-title">Add a course</h2>
            <p className="panel-desc">
              Enter the term dates and exam date so the planner can schedule work across the semester.
            </p>

            <form className="course-form" onSubmit={handleCreate}>
              <div className="field full">
                <label>Course name</label>
                <input
                  placeholder="CSE 316 – Software Development"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>

              <div className="field">
                <label>Term start</label>
                <input
                  type="date"
                  value={termStart}
                  onChange={(e) => setTermStart(e.target.value)}
                  required
                />
              </div>

              <div className="field">
                <label>Term end</label>
                <input
                  type="date"
                  value={termEnd}
                  onChange={(e) => setTermEnd(e.target.value)}
                  required
                />
              </div>

              <div className="field full">
                <label>Main exam date (optional)</label>
                <input
                  type="date"
                  value={mainExamDate}
                  onChange={(e) => setMainExamDate(e.target.value)}
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">
                  Save course
                </button>
              </div>
            </form>
          </section>

          <section className="panel panel-list">
            <div className="panel-header-row">
              <h2 className="panel-title">Your courses</h2>
              {courses.length > 0 && (
                <span className="chip">{courses.length} total</span>
              )}
            </div>

            {loading ? (
              <p className="muted">Loading courses…</p>
            ) : courses.length === 0 ? (
              <p className="muted">
                No courses yet. Add one on the left to get started.
              </p>
            ) : (
              <div className="course-grid">
                {courses.map((c) => (
                  <article key={c.id} className="course-card">
                    <h3 className="course-name">{c.name}</h3>
                    <p className="course-dates">
                      <span>
                        {c.termStart} → {c.termEnd}
                      </span>
                      {c.mainExamDate && (
                        <span className="exam-pill">
                          Exam: <strong>{c.mainExamDate}</strong>
                        </span>
                      )}
                    </p>
                    <p className="course-meta">
                      Study plan generation will go here.
                    </p>
                  </article>
                ))}
              </div>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;