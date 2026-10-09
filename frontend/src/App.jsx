import Prediction from "./prediction.jsx";
import ModelAnalytics from "./modelAnalytics.jsx";
import { useState } from "react";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("Overview");

  const tabs = ["Overview", "Risk Prediction", "Model Analytics"];

  return (
    <div className="app">
      <aside className="sidebar">
        <h2 className="brand">Student<span>IQ</span></h2>
        <p className="sidebar-label">WORKSPACE</p>

        {tabs.map((tab) => (
          <button
            key={tab}
            className={`nav-item ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab === "Overview" && "▦"}
            {tab === "Risk Prediction" && "◎"}
            {tab === "Model Analytics" && "▥"}
            <span>{tab}</span>
          </button>
        ))}

        <div className="sidebar-bottom">
          <div className="avatar">SP</div>
          <div>
            <strong>Student Analytics</strong>
            <p>ML Dashboard</p>
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <p className="eyebrow">STUDENT PERFORMANCE / ANALYTICS</p>
            <h1>{activeTab}</h1>
          </div>
          <div className="status"><span /> API Dashboard</div>
        </header>
        
        
{activeTab === "Risk Prediction" ? (
  <Prediction />
) : activeTab === "Model Analytics" ? (
  <ModelAnalytics />
) : (
  <>

  

        <section className="welcome">
          <div>
            <p className="eyebrow">ACADEMIC INTELLIGENCE</p>
            <h2>Understand performance.<br />Support potential.</h2>
            <p className="welcome-text">
              Explore student data and identify where additional academic
              support may be useful.
            </p>
          </div>
          <div className="hero-icon">✳</div>
        </section>

        <section className="section-heading">
          <div>
            <h2>Performance overview</h2>
            <p>Your machine learning workspace at a glance.</p>
          </div>
          <span className="tag">STUDENT DATASET</span>
        </section>

        <section className="stats">
          <article className="stat-card">
            <div className="stat-top"><span>Dataset</span><span>▤</span></div>
            <h3>395</h3>
            <p>Student records</p>
            <div className="stat-note">Portuguese secondary-school data</div>
          </article>

          <article className="stat-card">
            <div className="stat-top"><span>ML Models</span><span>⌘</span></div>
            <h3>3</h3>
            <p>Models evaluated</p>
            <div className="stat-note">Baseline, Logistic Regression, Random Forest</div>
          </article>

          <article className="stat-card">
            <div className="stat-top"><span>Best ROC-AUC</span><span>↗</span></div>
            <h3>0.727</h3>
            <p>Logistic Regression</p>
            <div className="stat-note">Held-out test-set result</div>
          </article>

          <article className="stat-card">
            <div className="stat-top"><span>Best F1-score</span><span>◎</span></div>
            <h3>0.60</h3>
            <p>At-risk class</p>
            <div className="stat-note">Held-out test-set result</div>
          </article>
        </section>

        <section className="content-grid">
          <article className="panel">
            <div className="panel-heading">
              <div>
                <h2>Model performance</h2>
                <p>Test-set metrics from your training run</p>
              </div>
              <span className="tag">F1 SCORE</span>
            </div>

            <div className="metric-row">
              <span>Logistic Regression</span>
              <div className="bar"><div style={{ width: "60%" }} /></div>
              <strong>0.60</strong>
            </div>
            <div className="metric-row">
              <span>Random Forest</span>
              <div className="bar"><div style={{ width: "51%" }} /></div>
              <strong>0.51</strong>
            </div>
            <div className="metric-row">
              <span>Dummy Baseline</span>
              <div className="bar"><div style={{ width: "0%" }} /></div>
              <strong>—</strong>
            </div>

            <p className="footnote">
              Metrics are from the current training run and may change when the
              model is retrained.
            </p>
          </article>

          <article className="panel prediction-panel">
            <div className="prediction-symbol">✧</div>
            <p className="eyebrow">MACHINE LEARNING</p>
            <h2>Student risk prediction</h2>
            <p>
              Use your trained model to estimate whether a student may benefit
              from additional academic support.
            </p>
            <button
              className="primary-button"
              onClick={() => setActiveTab("Risk Prediction")}
            >
              Open prediction workspace <span>→</span>
            </button>
          </article>
        </section>

        <footer>
          <span>StudentIQ · Student Performance Analytics</span>
          <span>Educational prototype · Not for consequential decisions</span>
        </footer>
          </>
)}
      </main>
    </div>
  );
}

export default App;