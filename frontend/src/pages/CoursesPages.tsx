import { useEffect, useState } from "react";
import { api } from "../api/client";

interface Course {
  id: number;
  name: string;
  termStart: string;
  termEnd: string;
  mainExamDate: string | null;
}

export function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [name, setName] = useState("");
  const [termStart, setTermStart] = useState("");
  const [termEnd, setTermEnd] = useState("");
  const [mainExamDate, setMainExamDate] = useState("");

  useEffect(() => {
    api.get<Course[]>("/courses").then((res) => setCourses(res.data));
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
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
    <div style={{ padding: "2rem" }}>
      <h1>My Courses</h1>

      <form onSubmit={handleCreate} style={{ marginBottom: "1.5rem" }}>
        <input
          placeholder="Course name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="date"
          value={termStart}
          onChange={(e) => setTermStart(e.target.value)}
          required
        />
        <input
          type="date"
          value={termEnd}
          onChange={(e) => setTermEnd(e.target.value)}
          required
        />
        <input
          type="date"
          value={mainExamDate}
          onChange={(e) => setMainExamDate(e.target.value)}
        />
        <button type="submit">Add course</button>
      </form>

      <ul>
        {courses.map((c) => (
          <li key={c.id}>
            {c.name} ({c.termStart} → {c.termEnd})
          </li>
        ))}
      </ul>
    </div>
  );
}