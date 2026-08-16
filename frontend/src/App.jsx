import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DashboardView from './components/DashboardView';
import AssessmentForm from './components/AssessmentForm';
import AssessmentDetailView from './components/AssessmentDetailView';
import KnowledgeExplorerView from './components/KnowledgeExplorerView';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [useCases, setUseCases] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [selectedAssessment, setSelectedAssessment] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [casesRes, analyticsRes] = await Promise.all([
        fetch('/api/use-cases'),
        fetch('/api/analytics')
      ]);
      const casesData = await casesRes.json();
      const analyticsData = await analyticsRes.json();
      setUseCases(casesData);
      setAnalytics(analyticsData);
    } catch (err) {
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCase = async (assessmentId) => {
    try {
      setLoading(true);
      const res = await fetch(`/api/assessments/${assessmentId}`);
      const data = await res.json();
      setSelectedAssessment(data);
      setActiveTab('detail');
    } catch (err) {
      console.error("Error loading assessment details:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAssessment = async (inputData) => {
    try {
      const res = await fetch('/api/assess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputData)
      });
      const newAssessment = await res.json();
      setSelectedAssessment(newAssessment);
      await fetchData();
      setActiveTab('detail');
    } catch (err) {
      throw err;
    }
  };

  const handleExportReport = async (assessmentId) => {
    try {
      const res = await fetch(`/api/export-report/${assessmentId}`);
      const data = await res.json();
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
      />

      <main style={{ flex: 1 }}>
        {loading && !selectedAssessment && activeTab === 'dashboard' ? (
          <div style={{ textAlign: 'center', padding: '100px 20px', color: '#94a3b8' }}>
            Loading VeriTrust AI Governance Intelligence...
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <DashboardView 
                useCases={useCases}
                analytics={analytics}
                onSelectCase={handleSelectCase}
                onStartNewTest={() => setActiveTab('assess')}
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
