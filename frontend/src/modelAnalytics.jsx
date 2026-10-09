
import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
} from "recharts";

export default function ModelAnalytics() {
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("https://studentiq-api.onrender.com/metrics")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load model metrics");
        }
        return response.json();
      })
      .then(setMetrics)
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <section className="panel">
        <h2>Model Analytics</h2>
        <p>{error}. Please ensure the backend is running.</p>
      </section>
    );
  }

  if (!metrics) {
    return <section className="panel">Loading model analytics...</section>;
  }

  const modelData = Object.entries(metrics.models).map(([name, model]) => ({
    name,
    Accuracy: +(model.accuracy * 100).toFixed(1),
    Precision: +(model.precision * 100).toFixed(1),
    Recall: +(model.recall * 100).toFixed(1),
    "F1 Score": +(model.f1 * 100).toFixed(1),
  }));

  const cvData = Object.entries(metrics.models).map(([name, model]) => ({
    name,
    "Mean CV F1": +(model.cv_f1_mean * 100).toFixed(1),
    "CV F1 Std": +(model.cv_f1_std * 100).toFixed(1),
  }));

  const score = (value) => `${value}%`;

  return (
    <div className="analytics-page">
      <section className="section-heading">
        <div>
          <p className="eyebrow">MACHINE LEARNING</p>
          <h2>Model Analytics</h2>
          <p>Compare model performance using your latest training results.</p>
        </div>
        <span className="tag">LIVE METRICS</span>
      </section>

      <section className="stats">
        <article className="stat-card">
          <div className="stat-top">
            <span>Best Model</span>
            <span>✦</span>
          </div>
          <h3>{metrics.best_model_by_cv_f1}</h3>
          <p>Selected using cross-validation F1</p>
        </article>

        <article className="stat-card">
          <div className="stat-top">
            <span>Best CV F1</span>
            <span>◎</span>
          </div>
          <h3>{(metrics.best_cv_f1 * 100).toFixed(1)}%</h3>
          <p>Mean cross-validation F1 score</p>
        </article>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h2>Model Performance Comparison</h2>
            <p>Held-out test set metrics</p>
          </div>
        </div>

        <div style={{ width: "100%", height: 360 }}>
          <ResponsiveContainer>
            <BarChart
  data={modelData}
  margin={{ top: 20, right: 20, left: 10, bottom: 60 }}
>
              <XAxis
  dataKey="name"
  stroke="#a8a8bd"
  interval={0}
  tick={{ fontSize: 12 }}
  tickMargin={12}
  height={70}
  angle={-15}
  textAnchor="end"
/>
              <YAxis stroke="#a8a8bd" domain={[0, 100]} tickFormatter={score} />
              <Tooltip formatter={(value) => `${value}%`} />
              <Legend />
              <Bar dataKey="Accuracy" fill="#8b5cf6" radius={[5, 5, 0, 0]} />
              <Bar dataKey="Precision" fill="#38bdf8" radius={[5, 5, 0, 0]} />
              <Bar dataKey="Recall" fill="#34d399" radius={[5, 5, 0, 0]} />
              <Bar dataKey="F1 Score" fill="#fbbf24" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h2>Cross-validation F1 Comparison</h2>
            <p>Mean F1 score across training folds</p>
          </div>
        </div>

        <div style={{ width: "100%", height: 320 }}>
          <ResponsiveContainer>
            <LineChart data={cvData} margin={{ top: 20, right: 25, left: 5, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#343442" />
              <XAxis dataKey="name" stroke="#a8a8bd" />
              <YAxis stroke="#a8a8bd" domain={[0, 100]} tickFormatter={score} />
              <Tooltip formatter={(value) => `${value}%`} />
              <Legend
  verticalAlign="bottom"
  align="center"
  wrapperStyle={{
    paddingTop: "25px",
    fontSize: "13px"
  }}
/>
              <Line
                type="monotone"
                dataKey="CV F1 Std"
                stroke="#fb7185"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <p className="footnote">
          CV F1 Std shows variation across folds; lower variation generally
          indicates more consistent cross-validation scores.
        </p>
      </section>

      <section className="panel">
        <h2>Model Scores</h2>
        {modelData.map((model) => (
          <article key={model.name} className="metric-row">
            <span>{model.name}</span>
            <strong>F1: {model["F1 Score"]}%</strong>
          </article>
        ))}
        <p className="footnote">
          Educational prototype only. Predictions should not be used as the
          sole basis for consequential decisions about students.
        </p>
      </section>
    </div>
  );
}
