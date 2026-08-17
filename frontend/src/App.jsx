import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DashboardView from './components/DashboardView';
import AssessmentForm from './components/AssessmentForm';
import AssessmentDetailView from './components/AssessmentDetailView';
import KnowledgeExplorerView from './components/KnowledgeExplorerView';
import { AlertTriangle, RefreshCw, Server, CheckCircle2 } from 'lucide-react';

const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');

async function fetchJson(url, options = {}) {
  let res;
  try {
    res = await fetch(url, options);
  } catch (netErr) {
    throw new Error(`Cannot connect to backend (${netErr.message || 'Network request failed'}). If deployed on Render free tier, it may be waking up from sleep.`);
  }

  const contentType = res.headers.get("content-type") || "";
  
  if (!res.ok) {
    let errorMsg = `Server error (HTTP ${res.status})`;
    if (contentType.includes("application/json")) {
      try {
        const errJson = await res.json();
        errorMsg = errJson.detail || errJson.message || errorMsg;
      } catch (e) {}
    } else {
      const text = await res.text();
      if (text.includes("<!DOCTYPE") || text.includes("<html") || text.includes("vite")) {
        errorMsg = `API request reached Vercel frontend instead of Render backend. Please set 'VITE_API_BASE_URL' in Vercel project environment variables to your Render service URL.`;
      }
    }
    throw new Error(errorMsg);
  }

  if (!contentType.includes("application/json")) {
    const text = await res.text();
    if (text.includes("<!DOCTYPE") || text.includes("<html") || text.includes("vite")) {
      throw new Error(`API returned HTML instead of JSON. Ensure 'VITE_API_BASE_URL' in Vercel is set to your Render backend URL (e.g. https://veritrust-backend.onrender.com).`);
    }
    throw new Error(`Expected JSON response but received content-type: ${contentType}`);
  }

  return await res.json();
}

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [useCases, setUseCases] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [selectedAssessment, setSelectedAssessment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [connectionError, setConnectionError] = useState(null);
  const [isBackendConnected, setIsBackendConnected] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setConnectionError(null);
      const [casesData, analyticsData] = await Promise.all([
        fetchJson(`${API_BASE}/api/use-cases`),
        fetchJson(`${API_BASE}/api/analytics`)
      ]);
      setUseCases(casesData);
      setAnalytics(analyticsData);
      setIsBackendConnected(true);
    } catch (err) {
      console.error("Error fetching data:", err);
      setConnectionError(err.message);
      setIsBackendConnected(false);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCase = async (assessmentId) => {
    try {
      setLoading(true);
      const data = await fetchJson(`${API_BASE}/api/assessments/${assessmentId}`);
      setSelectedAssessment(data);
      setActiveTab('detail');
    } catch (err) {
      console.error("Error loading assessment details:", err);
      alert("Error loading assessment: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAssessment = async (inputData) => {
    try {
      const newAssessment = await fetchJson(`${API_BASE}/api/assess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputData)
      });
      setSelectedAssessment(newAssessment);
      await fetchData();
      setActiveTab('detail');
    } catch (err) {
      throw err;
    }
  };

  const handleDeleteUseCase = async (useCaseId, useCaseName) => {
    const confirmed = window.confirm(`Are you sure you want to delete the AI use case "${useCaseName}"? All associated assessments and evidence citations will be removed.`);
    if (!confirmed) return;

    try {
      setLoading(true);
      await fetchJson(`${API_BASE}/api/use-cases/${useCaseId}`, {
        method: 'DELETE'
      });
      if (selectedAssessment?.use_case_id === useCaseId) {
        setSelectedAssessment(null);
        setActiveTab('dashboard');
      }
      await fetchData();
    } catch (err) {
      alert("Error deleting use case: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExportReport = async (assessmentId) => {
    try {
      const data = await fetchJson(`${API_BASE}/api/export-report/${assessmentId}`);
      const jsonString = `data:text/json;charset=utf-8,${encodeURIComponent(
        JSON.stringify(data, null, 2)
      )}`;
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", jsonString);
      downloadAnchor.setAttribute("download", `VeriTrust_AI_Audit_${assessmentId}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    } catch (err) {
      alert("Error exporting report: " + err.message);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={(tab) => {
          if (tab !== 'detail') setSelectedAssessment(null);
          setActiveTab(tab);
        }} 
        isBackendConnected={isBackendConnected}
      />

      {/* Backend Connection Warning Banner if Disconnected */}
      {connectionError && (
        <div style={{
          background: 'linear-gradient(90deg, rgba(239, 68, 68, 0.15) 0%, rgba(245, 158, 11, 0.15) 100%)',
          borderBottom: '1px solid rgba(239, 68, 68, 0.3)',
          padding: '12px 28px',
          color: '#fca5a5',
          fontSize: '0.88rem'
        }}>
          <div style={{ maxWidth: '1440px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <AlertTriangle style={{ width: '18px', height: '18px', color: '#f87171', flexShrink: 0 }} />
              <span>
                <strong>Backend Connection Notice:</strong> {connectionError}
              </span>
            </div>
            <button 
              onClick={fetchData} 
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 14px',
                background: '#ef4444',
                color: '#fff',
                border: 'none',
                borderRadius: '6px',
                fontSize: '0.8rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              <RefreshCw style={{ width: '13px', height: '13px' }} />
              Retry Connection
            </button>
          </div>
        </div>
      )}

      <main style={{ flex: 1 }}>
        {loading && !selectedAssessment && activeTab === 'dashboard' && useCases.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '100px 20px', color: '#94a3b8' }}>
            <RefreshCw style={{ width: '32px', height: '32px', color: '#60a5fa', animation: 'spin 1.5s linear infinite', marginBottom: '14px' }} />
            <div style={{ fontSize: '1.1rem', color: '#f1f5f9', fontWeight: 600 }}>Connecting to VeriTrust AI Governance Engine...</div>
            <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '6px' }}>
              Connecting to {API_BASE ? API_BASE : 'Local Host / Proxy'} (Render free tier may take ~30s if waking from sleep)
            </p>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <DashboardView 
                useCases={useCases}
                analytics={analytics}
                onSelectCase={handleSelectCase}
                onStartNewTest={() => setActiveTab('assess')}
                onDeleteCase={handleDeleteUseCase}
              />
            )}

            {activeTab === 'assess' && (
              <AssessmentForm 
                onSubmit={handleCreateAssessment}
                onCancel={() => setActiveTab('dashboard')}
              />
            )}

            {activeTab === 'detail' && (
              <AssessmentDetailView 
                assessment={selectedAssessment}
                onBack={() => setActiveTab('dashboard')}
                onExportReport={handleExportReport}
              />
            )}

            {activeTab === 'knowledge' && (
              <KnowledgeExplorerView />
            )}
          </>
        )}
      </main>

      {/* Clean Uncluttered Footer */}
      <footer style={{ borderTop: '1px solid rgba(255, 255, 255, 0.08)', padding: '18px 28px', marginTop: '50px', textAlign: 'center', color: '#64748b', fontSize: '0.8rem' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
          <div>VeriTrust AI — Enterprise AI Governance & Risk Assessment Platform v1.0</div>
          <div>10 Governance Areas & 6-Tier Regulatory Evidence Retrieval Engine</div>
        </div>
      </footer>
    </div>
  );
}
