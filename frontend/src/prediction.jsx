import { useState } from "react";

const initialForm = {
  school: "GP",
  sex: "F",
  age: 17,
  address: "U",
  famsize: "GT3",
  Pstatus: "T",
  Medu: 3,
  Fedu: 2,
  Mjob: "other",
  Fjob: "other",
  reason: "course",
  guardian: "mother",
  traveltime: 1,
  studytime: 2,
  failures: 0,
  schoolsup: "no",
  famsup: "yes",
  paid: "no",
  activities: "yes",
  nursery: "yes",
  higher: "yes",
  internet: "yes",
  romantic: "no",
  famrel: 4,
  freetime: 3,
  goout: 3,
  Dalc: 1,
  Walc: 2,
  health: 4,
  absences: 2,
};

const fields = [
  ["school", "School", ["GP", "MS"]],
  ["sex", "Sex", ["F", "M"]],
  ["age", "Age", null, 15, 22],
  ["address", "Home address type", ["U", "R"]],
  ["famsize", "Family size", ["GT3", "LE3"]],
  ["Pstatus", "Parents' cohabitation", ["T", "A"]],
  ["Medu", "Mother's education (0–4)", null, 0, 4],
  ["Fedu", "Father's education (0–4)", null, 0, 4],
  ["Mjob", "Mother's job", ["teacher", "health", "services", "at_home", "other"]],
  ["Fjob", "Father's job", ["teacher", "health", "services", "at_home", "other"]],
  ["reason", "School choice reason", ["course", "home", "reputation", "other"]],
  ["guardian", "Guardian", ["mother", "father", "other"]],
  ["traveltime", "Travel time (1–4)", null, 1, 4],
  ["studytime", "Weekly study time (1–4)", null, 1, 4],
  ["failures", "Past class failures (0–4)", null, 0, 4],
  ["schoolsup", "School support", ["yes", "no"]],
  ["famsup", "Family support", ["yes", "no"]],
  ["paid", "Extra paid classes", ["yes", "no"]],
  ["activities", "Extracurricular activities", ["yes", "no"]],
  ["nursery", "Attended nursery", ["yes", "no"]],
  ["higher", "Wants higher education", ["yes", "no"]],
  ["internet", "Internet access at home", ["yes", "no"]],
  ["romantic", "In a romantic relationship", ["yes", "no"]],
  ["famrel", "Family relationship (1–5)", null, 1, 5],
  ["freetime", "Free time (1–5)", null, 1, 5],
  ["goout", "Going out (1–5)", null, 1, 5],
  ["Dalc", "Workday alcohol consumption (1–5)", null, 1, 5],
  ["Walc", "Weekend alcohol consumption (1–5)", null, 1, 5],
  ["health", "Self-reported health (1–5)", null, 1, 5],
  ["absences", "School absences", null, 0, 100],
];

export default function Prediction() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateField(key, value, numeric = false) {
    setForm((old) => ({
      ...old,
      [key]: numeric ? Number(value) : value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("https://studentiq-api.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail
            ? JSON.stringify(data.detail)
            : "Prediction request failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot connect to the API. Check that your FastAPI server is running at http://127.0.0.1:8000."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="prediction-page">
      <div className="prediction-intro">
        <p className="eyebrow">MACHINE LEARNING WORKSPACE</p>
        <h2>Student risk prediction</h2>
        <p>Enter student details to request a prediction from your trained model.</p>
      </div>

      <form className="prediction-form" onSubmit={handleSubmit}>
        <div className="form-heading">
          <h3>Student information</h3>
          <span>30 INPUT FIELDS</span>
        </div>

        <div className="form-grid">
          {fields.map(([key, label, options, min, max]) => (
            <label className="field" key={key}>
              <span>{label}</span>
              {options ? (
                <select
                  value={form[key]}
                  onChange={(e) => updateField(key, e.target.value)}
                >
                  {options.map((option) => (
                    <option value={option} key={option}>
                      {option}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type="number"
                  min={min}
                  max={max}
                  value={form[key]}
                  required
                  onChange={(e) => updateField(key, e.target.value, true)}
                />
              )}
            </label>
          ))}
        </div>

        <button className="primary-button submit-button" disabled={loading}>
          {loading ? "Analysing student..." : "Generate prediction →"}
        </button>
      </form>

      {error && (
        <div className="prediction-result error-result">
          <h3>Prediction unavailable</h3>
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="prediction-result">
          <p className="eyebrow">MODEL OUTPUT</p>
          <h3>{result.at_risk ? "Potential support may be useful" : "Lower predicted risk"}</h3>
          <p>
            Estimated risk probability:{" "}
            <strong>{(result.risk_probability * 100).toFixed(1)}%</strong>
          </p>
          <div className="result-track">
            <div style={{ width: `${Math.min(100, Math.max(0, result.risk_probability * 100))}%` }} />
          </div>
          <p>{result.interpretation}</p>
          <small>{result.notice}</small>
        </div>
      )}
    </section>
  );
} 