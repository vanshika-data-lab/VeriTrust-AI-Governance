import React, { useState } from 'react';
import { ArrowLeft, Shield, AlertTriangle, FileCheck, ExternalLink, Download, Layers, CheckCircle2, ChevronDown, ChevronUp } from 'lucide-react';
import EvidenceDrawer from './EvidenceDrawer';

export default function AssessmentDetailView({ assessment, onBack, onExportReport }) {
  const [expandedDimension, setExpandedDimension] = useState(null);
  const [showEvidenceDrawer, setShowEvidenceDrawer] = useState(false);

  if (!assessment) return null;

  const isHighRisk = assessment.overall_risk_score >= 68.0;

  const toggleDimension = (key) => {
    setExpandedDimension(expandedDimension === key ? null : key);
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '30px auto', padding: '0 28px' }}>
      
      {/* Top Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <button className="btn btn-secondary" onClick={onBack} style={{ padding: '8px 14px' }}>
          <ArrowLeft style={{ width: '16px', height: '16px' }} />
          Back to Dashboard
        </button>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button 
            className="btn btn-secondary"
            onClick={() => setShowEvidenceDrawer(true)}
            style={{ background: 'rgba(99, 102, 241, 0.15)', borderColor: 'rgba(99, 102, 241, 0.4)', color: '#a5b4fc' }}
          >
            <FileCheck style={{ width: '16px', height: '16px' }} />
            View 6-Tier Cited Evidence Sources ({assessment.sources?.length || 0})
          </button>

          <button className="btn btn-primary" onClick={() => onExportReport(assessment.id)}>
            <Download style={{ width: '16px', height: '16px' }} />
            Export Audit Report (JSON)
          </button>
        </div>
      </div>

      {/* Header Banner */}
      <div className="glass-panel" style={{ padding: '30px', marginBottom: '30px', borderLeft: `6px solid ${isHighRisk ? '#f43f5e' : '#10b981'}` }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '20px' }}>
          
          <div style={{ flex: 1, minWidth: '320px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
              <span className="badge" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                {assessment.industry}
              </span>
              <span className={`badge ${isHighRisk ? 'badge-high' : 'badge-low'}`}>
                {assessment.risk_level}
              </span>
            </div>

            <h2 style={{ fontSize: '1.9rem', color: '#fff', marginBottom: '8px' }}>{assessment.use_case_name}</h2>
            <p style={{ color: '#94a3b8', fontSize: '0.92rem', marginBottom: '16px' }}>{assessment.purpose}</p>

            {/* EU AI Act Banner */}
            <div style={{ background: 'rgba(13, 21, 39, 0.85)', padding: '12px 16px', borderRadius: '10px', border: '1px solid rgba(255, 255, 255, 0.12)', display: 'inline-flex', alignItems: 'center', gap: '10px' }}>
              <Shield style={{ width: '20px', height: '20px', color: '#6366f1' }} />
              <div>
                <span style={{ fontSize: '0.72rem', color: '#64748b', display: 'block', textTransform: 'uppercase', letterSpacing: '0.05em' }}>EU AI ACT CLASSIFICATION</span>
                <span style={{ fontSize: '0.9rem', color: '#f8fafc', fontWeight: 600 }}>{assessment.eu_ai_act_category}</span>
              </div>
            </div>
          </div>

          {/* Big Score Gauge */}
          <div className="glass-card" style={{ padding: '24px', textAlign: 'center', minWidth: '220px', background: 'rgba(17, 24, 39, 0.9)' }}>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em', display: 'block', marginBottom: '8px' }}>GOVERNANCE RISK INDEX</span>
            <div style={{ fontSize: '3rem', fontWeight: 800, color: isHighRisk ? '#f43f5e' : '#10b981', lineHeight: 1 }}>
              {assessment.overall_risk_score}
              <span style={{ fontSize: '1.2rem', color: '#64748b' }}>/100</span>
            </div>
            <span style={{ fontSize: '0.78rem', color: '#94a3b8', marginTop: '8px', display: 'block' }}>
              10 Dimensions Evaluated
            </span>
          </div>

        </div>

        {/* Executive Summary */}
        <div style={{ marginTop: '24px', paddingTop: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
          <h4 style={{ fontSize: '0.95rem', color: '#a5b4fc', marginBottom: '6px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>EXECUTIVE ASSESSMENT SUMMARY</h4>
          <p style={{ color: '#cbd5e1', fontSize: '0.92rem', lineHeight: '1.6' }}>{assessment.executive_summary}</p>
        </div>
      </div>

      {/* 10 Governance Dimensions Section */}
      <div style={{ marginBottom: '36px' }}>
        <h3 style={{ fontSize: '1.3rem', color: '#fff', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Layers style={{ width: '20px', height: '20px', color: '#6366f1' }} />
          Detailed 10-Dimension Risk Breakdown & Mitigating Controls
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(620px, 1fr))', gap: '20px' }}>
          {assessment.dimensions?.map((dim) => {
            const isDimHigh = dim.risk_score >= 68.0;
            const isExpanded = expandedDimension === dim.dimension_key;

            return (
              <div key={dim.dimension_key} className="glass-card" style={{ padding: '20px', borderLeft: `4px solid ${isDimHigh ? '#f43f5e' : '#10b981'}` }}>
                
                {/* Header */}
                <div 
                  style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}
                  onClick={() => toggleDimension(dim.dimension_key)}
                >
                  <div>
                    <span style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em' }}>GOVERNANCE AREA</span>
                    <h4 style={{ fontSize: '1.1rem', color: '#fff' }}>{dim.dimension_name}</h4>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span className={`badge ${isDimHigh ? 'badge-high' : 'badge-low'}`}>
                      Score: {dim.risk_score}/100
                    </span>
                    {isExpanded ? <ChevronUp style={{ width: '18px', height: '18px', color: '#94a3b8' }} /> : <ChevronDown style={{ width: '18px', height: '18px', color: '#94a3b8' }} />}
                  </div>
                </div>

                {/* Score Progress Bar */}
                <div style={{ background: 'rgba(255, 255, 255, 0.08)', height: '6px', borderRadius: '3px', margin: '14px 0', overflow: 'hidden' }}>
                  <div 
                    style={{ 
                      width: `${dim.risk_score}%`, 
                      height: '100%', 
                      background: isDimHigh ? 'linear-gradient(90deg, #f43f5e, #fb7185)' : 'linear-gradient(90deg, #10b981, #34d399)' 
                    }} 
                  />
                </div>

                {/* Empirical Findings */}
                <p style={{ color: '#cbd5e1', fontSize: '0.88rem', marginBottom: '12px' }}>
                  <strong>Findings:</strong> {dim.findings}
                </p>

                {/* Statutory Impact */}
                <div style={{ background: 'rgba(13, 21, 39, 0.6)', padding: '10px 12px', borderRadius: '6px', marginBottom: '12px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                  <span style={{ fontSize: '0.78rem', color: '#a5b4fc', fontWeight: 600 }}>Statutory Impact: </span>
                  <span style={{ fontSize: '0.82rem', color: '#94a3b8' }}>{dim.regulatory_impact}</span>
                </div>

                {/* Mitigating Controls Checklist */}
                {isExpanded && (
                  <div style={{ marginTop: '14px', paddingTop: '14px', borderTop: '1px dashed rgba(255, 255, 255, 0.1)' }}>
                    <span style={{ fontSize: '0.8rem', color: '#6ee7b7', fontWeight: 600, display: 'block', marginBottom: '8px' }}>
                      ✓ MANDATORY ACTIONABLE MITIGATING CONTROLS:
                    </span>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                      {dim.mitigating_controls?.map((ctrl, idx) => (
                        <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.82rem', color: '#cbd5e1' }}>
                          <CheckCircle2 style={{ width: '14px', height: '14px', color: '#10b981', marginTop: '2px', flexShrink: 0 }} />
                          <span>{ctrl}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

              </div>
            );
          })}
        </div>
      </div>

      {/* Slide-over Evidence Drawer */}
      {showEvidenceDrawer && (
        <EvidenceDrawer 
          sources={assessment.sources || []} 
          onClose={() => setShowEvidenceDrawer(false)} 
        />
      )}

    </div>
  );
}
