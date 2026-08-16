import React from 'react';
import { ShieldCheck, AlertTriangle, FileCheck, ArrowRight, Building2, Layers, Sparkles, Scale, BookOpen, Award, CheckCircle2, Lock, Eye, Cpu, Activity, Zap, AlertCircle } from 'lucide-react';

export default function DashboardView({ useCases, onSelectCase, onStartNewTest, analytics }) {

  const avgScore = useCases.length > 0 
    ? Math.round(useCases.reduce((acc, c) => acc + (c.overall_risk_score || 70), 0) / useCases.length) 
    : 78;

  const tierDistribution = analytics?.source_tier_distribution || {
    "Law / Regulation": 8,
    "Regulatory Guidance": 7,
    "Industry Standard": 5,
    "Research": 4,
    "Vendor Information": 3,
    "General Web Content": 2
  };

  // Eye-catchy 10 Governance Areas with icons & descriptions
  const governanceAreas = [
    { name: "Data Lineage & Quality", score: 82, level: "High Risk", icon: Layers, color: "#f59e0b" },
    { name: "Privacy & Protection", score: 88, level: "Critical Risk", icon: Lock, color: "#f43f5e" },
    { name: "Bias, Fairness & Equity", score: 91, level: "Critical Risk", icon: Scale, color: "#f43f5e" },
    { name: "Human Oversight Controls", score: 84, level: "High Risk", icon: Eye, color: "#f59e0b" },
    { name: "Explainability & Recourse", score: 79, level: "High Risk", icon: BookOpen, color: "#f59e0b" },
    { name: "Cybersecurity Robustness", score: 76, level: "High Risk", icon: ShieldCheck, color: "#f59e0b" },
    { name: "Decision Impact Severity", score: 92, level: "Critical Risk", icon: Zap, color: "#f43f5e" },
    { name: "Regulatory Exposure", score: 89, level: "Critical Risk", icon: AlertCircle, color: "#f43f5e" },
    { name: "Model Reliability & Drift", score: 75, level: "High Risk", icon: Cpu, color: "#f59e0b" },
    { name: "Continuous Monitoring", score: 80, level: "High Risk", icon: Activity, color: "#f59e0b" }
  ];

  return (
    <div style={{ maxWidth: '1440px', margin: '24px auto', padding: '0 28px' }}>
      
      {/* Clean Uncluttered Hero Banner */}
      <div className="veritrust-card" style={{ 
        padding: '24px 30px', 
        marginBottom: '24px', 
        background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
        borderLeft: '5px solid #4f46e5',
        display: 'flex',
        justify: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '20px'
      }}>
        <div style={{ flex: 1, minWidth: '320px' }}>
          <h2 style={{ fontSize: '1.65rem', color: '#fff', marginBottom: '6px' }}>
            Enterprise AI Risk & Governance Assessment Engine
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '0.92rem', maxWidth: '820px', lineHeight: '1.5' }}>
            Automated research and multi-tier evaluation framework assessing enterprise AI systems across <strong>10 mandatory governance dimensions</strong>. 
            Combines a deterministic risk scoring matrix with <strong>6-tier regulatory RAG evidence</strong> across laws, guidance frameworks, industry standards, research, vendor specifications, and web sources.
          </p>
        </div>

        <div>
          <button 
            className="btn-v btn-v-success" 
            onClick={onStartNewTest}
            style={{ padding: '12px 22px', fontSize: '0.92rem' }}
          >
            <Sparkles style={{ width: '16px', height: '16px' }} />
            Test New "Surprise Record" Live
          </button>
        </div>
      </div>

      {/* Structured Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '18px', marginBottom: '28px' }}>
        
        <div className="veritrust-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Evaluated AI Use Cases
            </span>
            <Layers style={{ width: '18px', height: '18px', color: '#818cf8' }} />
          </div>
          <div style={{ fontSize: '2.1rem', fontWeight: 700, color: '#fff' }}>{useCases.length}</div>
          <div style={{ fontSize: '0.75rem', color: '#6ee7b7', marginTop: '2px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <CheckCircle2 style={{ width: '12px', height: '12px' }} />
            <span>Persisted SQLite Database</span>
          </div>
        </div>

        <div className="veritrust-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Average Risk Score
            </span>
            <AlertTriangle style={{ width: '18px', height: '18px', color: '#f59e0b' }} />
          </div>
          <div style={{ fontSize: '2.1rem', fontWeight: 700, color: '#fcd34d' }}>
            {avgScore}<span style={{ fontSize: '1rem', color: '#64748b' }}> / 100</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>
            EU AI Act High Risk Tiering
          </div>
        </div>

        <div className="veritrust-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Source Classification
            </span>
            <FileCheck style={{ width: '18px', height: '18px', color: '#10b981' }} />
          </div>
          <div style={{ fontSize: '2.1rem', fontWeight: 700, color: '#6ee7b7' }}>6 Tiers</div>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>
            Law, Guidance, Std, Research, Vendor, Web
          </div>
        </div>

        <div className="veritrust-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Assessment Engine
            </span>
            <ShieldCheck style={{ width: '18px', height: '18px', color: '#38bdf8' }} />
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#7dd3fc', marginTop: '2px' }}>10 Dimensions</div>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>
            Deterministic Scoring Matrix + RAG
          </div>
        </div>

      </div>

      {/* Eye-Catchy Governance Areas Visualizer + 6-Tier Evidence Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(480px, 1fr))', gap: '22px', marginBottom: '32px' }}>
        
        {/* STUNNING EYE-CATCHY 10 GOVERNANCE AREAS CARD */}
        <div className="veritrust-card" style={{ padding: '24px', borderTop: '4px solid #6366f1' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Layers style={{ width: '18px', height: '18px', color: '#818cf8' }} />
                10 Mandatory Governance Assessment Areas
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '2px' }}>
                Systematic evaluation matrix across core risk dimensions
              </p>
            </div>
            <span style={{ fontSize: '0.75rem', background: 'rgba(99, 102, 241, 0.15)', color: '#c7d2fe', padding: '4px 10px', borderRadius: '20px', fontWeight: 600, border: '1px solid rgba(99, 102, 241, 0.3)' }}>
              100% Evaluated
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px 14px' }}>
            {governanceAreas.map((area, idx) => {
              const IconComp = area.icon;
              return (
                <div key={idx} className="gov-meter-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <span style={{ fontSize: '0.78rem', color: '#f1f5f9', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <IconComp style={{ width: '14px', height: '14px', color: area.color }} />
                      {area.name}
                    </span>
                    <span style={{ fontSize: '0.78rem', color: area.color, fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                      {area.score}/100
                    </span>
                  </div>
                  
                  {/* Glowing Progress Bar */}
                  <div style={{ background: 'rgba(255, 255, 255, 0.08)', height: '6px', borderRadius: '3px', overflow: 'hidden' }}>
                    <div 
                      style={{ 
                        width: `${area.score}%`, 
                        height: '100%', 
                        background: area.score >= 88 ? 'linear-gradient(90deg, #f43f5e, #fb7185)' : 'linear-gradient(90deg, #f59e0b, #fbbf24)',
                        boxShadow: `0 0 8px ${area.color}66`
                      }} 
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* 6-Tier Evidence Classification Matrix */}
        <div className="veritrust-card" style={{ padding: '24px', borderTop: '4px solid #10b981' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileCheck style={{ width: '18px', height: '18px', color: '#34d399' }} />
                6-Tier Source Classification Matrix
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '2px' }}>
                Evidence sources supporting risk findings categorized by authority tier
              </p>
            </div>
            <span style={{ fontSize: '0.75rem', background: 'rgba(16, 185, 129, 0.15)', color: '#a7f3d0', padding: '4px 10px', borderRadius: '20px', fontWeight: 600, border: '1px solid rgba(16, 185, 129, 0.3)' }}>
              6 Tiers Active
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(99, 102, 241, 0.12)', borderRadius: '8px', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
              <span style={{ fontSize: '0.86rem', color: '#c7d2fe', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Scale style={{ width: '16px', height: '16px' }} /> ⚖️ Law / Regulation
              </span>
              <span style={{ fontSize: '0.86rem', color: '#fff', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>{tierDistribution["Law / Regulation"]} Cited Statutes</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(16, 185, 129, 0.12)', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
              <span style={{ fontSize: '0.86rem', color: '#a7f3d0', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileCheck style={{ width: '16px', height: '16px' }} /> 🏛️ Regulatory Guidance
              </span>
              <span style={{ fontSize: '0.86rem', color: '#fff', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>{tierDistribution["Regulatory Guidance"]} Guidance Documents</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(245, 158, 11, 0.12)', borderRadius: '8px', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
              <span style={{ fontSize: '0.86rem', color: '#fde68a', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Award style={{ width: '16px', height: '16px' }} /> 📐 Industry Standard
              </span>
              <span style={{ fontSize: '0.86rem', color: '#fff', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>{tierDistribution["Industry Standard"]} Standards</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(168, 85, 247, 0.12)', borderRadius: '8px', border: '1px solid rgba(168, 85, 247, 0.3)' }}>
              <span style={{ fontSize: '0.86rem', color: '#f5d0fe', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
                <BookOpen style={{ width: '16px', height: '16px' }} /> 🔬 Academic Research
              </span>
              <span style={{ fontSize: '0.86rem', color: '#fff', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>{tierDistribution["Research"]} Benchmarks</span>
            </div>
          </div>
        </div>

      </div>

      {/* Main Grid Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.25rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Building2 style={{ width: '20px', height: '20px', color: '#818cf8' }} />
          Enterprise AI Use Case Library ({useCases.length})
        </h3>
        <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Click any card to inspect full 10-dimension audit report</span>
      </div>

      {/* Grid of Use Case Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: '22px' }}>
        {useCases.map((uc) => {
          const isCritical = uc.risk_level === 'Critical Risk' || (uc.overall_risk_score >= 88);
          return (
            <div key={uc.id} className="veritrust-card" style={{ padding: '22px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                  <span className="badge-tag" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#c7d2fe', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                    {uc.industry}
                  </span>
                  <span className={`badge-tag ${isCritical ? 'badge-critical' : 'badge-high'}`}>
                    {uc.risk_level || 'Evaluated'} ({uc.overall_risk_score}/100)
                  </span>
                </div>

                <h4 style={{ fontSize: '1.12rem', color: '#fff', marginBottom: '6px', lineHeight: '1.3' }}>{uc.name}</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.86rem', marginBottom: '14px', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {uc.purpose}
                </p>

                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '14px' }}>
                  <span style={{ fontSize: '0.74rem', background: 'rgba(255, 255, 255, 0.05)', color: '#cbd5e1', padding: '3px 8px', borderRadius: '4px', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
                    Autonomy: {uc.autonomy_level}
                  </span>
                  <span style={{ fontSize: '0.74rem', background: 'rgba(255, 255, 255, 0.05)', color: '#cbd5e1', padding: '3px 8px', borderRadius: '4px', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
                    Impact Severity: {uc.impact_tier}
                  </span>
                </div>

                <div style={{ background: 'rgba(13, 21, 39, 0.8)', padding: '10px 12px', borderRadius: '6px', border: '1px dashed rgba(255, 255, 255, 0.12)', marginBottom: '18px' }}>
                  <span style={{ fontSize: '0.7rem', color: '#64748b', display: 'block', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>EU AI ACT STATUTORY CLASSIFICATION</span>
                  <span style={{ fontSize: '0.82rem', color: '#f8fafc', fontWeight: 600 }}>{uc.eu_ai_act_category}</span>
                </div>
              </div>

              <button 
                className="btn-v btn-v-outline" 
                style={{ width: '100%', justifyContent: 'center' }}
                onClick={() => onSelectCase(uc.assessment_id)}
              >
                Inspect 10-Dimension Risk Report
                <ArrowRight style={{ width: '14px', height: '14px' }} />
              </button>
            </div>
          );
        })}
      </div>

    </div>
  );
}
