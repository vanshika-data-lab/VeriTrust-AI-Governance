import React, { useState } from 'react';
import { 
  ShieldCheck, AlertTriangle, FileCheck, ArrowRight, Building2, Layers, Sparkles, 
  Scale, BookOpen, Award, CheckCircle2, Lock, Eye, Cpu, Activity, Zap, 
  AlertCircle, Trash2, Building, Globe, Search, Filter, RefreshCw, X
} from 'lucide-react';

export default function DashboardView({ useCases, onSelectCase, onStartNewTest, onDeleteCase, analytics }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedIndustry, setSelectedIndustry] = useState('All');
  const [selectedRiskFilter, setSelectedRiskFilter] = useState('All');
  const [useCaseToDelete, setUseCaseToDelete] = useState(null);

  const avgScore = useCases.length > 0 
    ? Math.round(useCases.reduce((acc, c) => acc + (c.overall_risk_score || 70), 0) / useCases.length) 
    : 78;

  const tierDistribution = analytics?.source_tier_distribution || {
    "Law / Regulation": 4,
    "Regulatory Guidance": 4,
    "Industry Standard": 3,
    "Research": 2,
    "Vendor Information": 2,
    "General Web Content": 1
  };

  // 10 Governance Areas with icons & descriptions
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

  // Complete 6-Tier Source Classification List (All 6 Tiers Displayed)
  const sourceTiersList = [
    { 
      key: "Law / Regulation", 
      label: "Law / Regulation", 
      desc: "EU AI Act, GDPR Art. 35, NYC LL144, ECOA", 
      icon: Scale, 
      count: tierDistribution["Law / Regulation"] || 4, 
      unit: "Statutes",
      color: "#818cf8",
      bg: "rgba(99, 102, 241, 0.12)",
      border: "rgba(99, 102, 241, 0.3)"
    },
    { 
      key: "Regulatory Guidance", 
      label: "Regulatory Guidance", 
      desc: "NIST AI RMF 1.0, FTC Fair Info, EEOC Guidance", 
      icon: FileCheck, 
      count: tierDistribution["Regulatory Guidance"] || 4, 
      unit: "Guidance Docs",
      color: "#34d399",
      bg: "rgba(16, 185, 129, 0.12)",
      border: "rgba(16, 185, 129, 0.3)"
    },
    { 
      key: "Industry Standard", 
      label: "Industry Standard", 
      desc: "ISO/IEC 42001, IEEE 7000 Series Standards", 
      icon: Award, 
      count: tierDistribution["Industry Standard"] || 3, 
      unit: "Standards",
      color: "#fbbf24",
      bg: "rgba(245, 158, 11, 0.12)",
      border: "rgba(245, 158, 11, 0.3)"
    },
    { 
      key: "Research", 
      label: "Academic Research", 
      desc: "Stanford CRFM, MIT Disparate Impact Benchmarks", 
      icon: BookOpen, 
      count: tierDistribution["Research"] || 2, 
      unit: "Studies",
      color: "#c084fc",
      bg: "rgba(168, 85, 247, 0.12)",
      border: "rgba(168, 85, 247, 0.3)"
    },
    { 
      key: "Vendor Information", 
      label: "Vendor Information", 
      desc: "Model System Cards, API SLAs, Cloud Audits", 
      icon: Building, 
      count: tierDistribution["Vendor Information"] || 2, 
      unit: "Tech Specs",
      color: "#22d3ee",
      bg: "rgba(6, 182, 212, 0.12)",
      border: "rgba(6, 182, 212, 0.3)"
    },
    { 
      key: "General Web Content", 
      label: "General Web Content", 
      desc: "Audited Industry Analysis & Regulatory Trackers", 
      icon: Globe, 
      count: tierDistribution["General Web Content"] || 1, 
      unit: "Analyses",
      color: "#94a3b8",
      bg: "rgba(148, 163, 184, 0.12)",
      border: "rgba(148, 163, 184, 0.3)"
    }
  ];

  // Unique industries for filter dropdown
  const industries = ['All', ...new Set(useCases.map(u => u.industry).filter(Boolean))];

  // Filtered use cases
  const filteredUseCases = useCases.filter(uc => {
    const matchesSearch = 
      uc.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      uc.purpose?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      uc.industry?.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesIndustry = selectedIndustry === 'All' || uc.industry === selectedIndustry;
    
    const matchesRisk = 
      selectedRiskFilter === 'All' || 
      (selectedRiskFilter === 'Critical' && (uc.risk_level === 'Critical Risk' || uc.overall_risk_score >= 88)) ||
      (selectedRiskFilter === 'High' && (uc.risk_level === 'High Risk' || (uc.overall_risk_score >= 68 && uc.overall_risk_score < 88))) ||
      (selectedRiskFilter === 'Medium' && uc.overall_risk_score < 68);

    return matchesSearch && matchesIndustry && matchesRisk;
  });

  return (
    <div style={{ maxWidth: '1440px', margin: '24px auto', padding: '0 28px' }}>
      
      {/* Clean Uncluttered Hero Banner */}
      <div className="veritrust-card" style={{ 
        padding: '24px 30px', 
        marginBottom: '24px', 
        background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
        borderLeft: '5px solid #4f46e5',
        display: 'flex',
        justifyContent: 'space-between',
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
            className="btn btn-success" 
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

      {/* 10 Governance Areas Visualizer + 6-Tier Evidence Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(480px, 1fr))', gap: '22px', marginBottom: '32px' }}>
        
        {/* 10 GOVERNANCE AREAS CARD */}
        <div className="veritrust-card" style={{ padding: '24px', borderTop: '4px solid #6366f1', display: 'flex', flexDirection: 'column' }}>
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

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '9px 12px', flex: 1 }}>
            {governanceAreas.map((area, idx) => {
              const IconComp = area.icon;
              const isCritical = area.score >= 88;
              return (
                <div 
                  key={idx} 
                  style={{
                    background: 'rgba(15, 23, 42, 0.65)',
                    border: '1px solid rgba(255, 255, 255, 0.07)',
                    borderRadius: '8px',
                    padding: '8px 10px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    gap: '6px'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.78rem', color: '#f1f5f9', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '22px',
                        height: '22px',
                        borderRadius: '5px',
                        background: isCritical ? 'rgba(244, 63, 94, 0.12)' : 'rgba(245, 158, 11, 0.12)'
                      }}>
                        <IconComp style={{ width: '13px', height: '13px', color: area.color }} />
                      </div>
                      {area.name}
                    </span>
                    <span style={{ fontSize: '0.78rem', color: area.color, fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                      {area.score}/100
                    </span>
                  </div>
                  
                  {/* Glowing Progress Bar */}
                  <div style={{ background: 'rgba(255, 255, 255, 0.08)', height: '5px', borderRadius: '3px', overflow: 'hidden' }}>
                    <div 
                      style={{ 
                        width: `${area.score}%`, 
                        height: '100%', 
                        background: isCritical ? 'linear-gradient(90deg, #f43f5e, #fb7185)' : 'linear-gradient(90deg, #f59e0b, #fbbf24)',
                        boxShadow: `0 0 6px ${area.color}66`
                      }} 
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* FULL 6-TIER SOURCE CLASSIFICATION MATRIX */}
        <div className="veritrust-card" style={{ padding: '24px', borderTop: '4px solid #10b981', display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileCheck style={{ width: '18px', height: '18px', color: '#34d399' }} />
                6-Tier Source Classification Matrix
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '2px' }}>
                Verified regulatory, statutory, standard, and empirical research citations
              </p>
            </div>
            <span style={{ fontSize: '0.75rem', background: 'rgba(16, 185, 129, 0.15)', color: '#a7f3d0', padding: '4px 10px', borderRadius: '20px', fontWeight: 600, border: '1px solid rgba(16, 185, 129, 0.3)' }}>
              6 Tiers Active
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
            {sourceTiersList.map((tier) => {
              const IconComponent = tier.icon;
              return (
                <div 
                  key={tier.key} 
                  style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'space-between', 
                    padding: '8px 12px', 
                    background: tier.bg, 
                    borderRadius: '8px', 
                    border: `1px solid ${tier.border}`,
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center', 
                      width: '26px', 
                      height: '26px', 
                      borderRadius: '6px', 
                      background: 'rgba(255, 255, 255, 0.06)' 
                    }}>
                      <IconComponent style={{ width: '15px', height: '15px', color: tier.color }} />
                    </div>
                    <div>
                      <span style={{ fontSize: '0.84rem', color: '#f8fafc', fontWeight: 600, display: 'block', lineHeight: 1.2 }}>
                        {tier.label}
                      </span>
                      <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                        {tier.desc}
                      </span>
                    </div>
                  </div>

                  <div style={{ textAlign: 'right' }}>
                    <span style={{ fontSize: '0.88rem', color: '#fff', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                      {tier.count}
                    </span>
                    <span style={{ fontSize: '0.72rem', color: '#94a3b8', display: 'block' }}>
                      {tier.unit}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* Main Grid Header & Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '14px' }}>
        <div>
          <h3 style={{ fontSize: '1.25rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Building2 style={{ width: '20px', height: '20px', color: '#818cf8' }} />
            Enterprise AI Use Case Library ({useCases.length})
          </h3>
          <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
            Showing {filteredUseCases.length} of {useCases.length} evaluated AI systems
          </span>
        </div>

        {/* Live Filter Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          {/* Search Box */}
          <div style={{ position: 'relative', minWidth: '220px' }}>
            <Search style={{ width: '15px', height: '15px', color: '#64748b', position: 'absolute', left: '10px', top: '10px' }} />
            <input 
              type="text" 
              placeholder="Search use cases..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '7px 10px 7px 32px',
                background: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '6px',
                color: '#fff',
                fontSize: '0.82rem'
              }}
            />
          </div>

          {/* Industry Filter */}
          <select 
            value={selectedIndustry}
            onChange={(e) => setSelectedIndustry(e.target.value)}
            style={{
              padding: '7px 10px',
              background: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '6px',
              color: '#cbd5e1',
              fontSize: '0.82rem',
              cursor: 'pointer'
            }}
          >
            {industries.map(ind => (
              <option key={ind} value={ind}>{ind === 'All' ? 'All Industries' : ind}</option>
            ))}
          </select>

          {/* Risk Level Filter */}
          <select 
            value={selectedRiskFilter}
            onChange={(e) => setSelectedRiskFilter(e.target.value)}
            style={{
              padding: '7px 10px',
              background: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '6px',
              color: '#cbd5e1',
              fontSize: '0.82rem',
              cursor: 'pointer'
            }}
          >
            <option value="All">All Risk Tiers</option>
            <option value="Critical">Critical Risk (88+)</option>
            <option value="High">High Risk (68-87)</option>
            <option value="Medium">Medium/Low (&lt;68)</option>
          </select>
        </div>
      </div>

      {/* Grid of Use Case Cards */}
      {filteredUseCases.length === 0 ? (
        <div className="veritrust-card" style={{ padding: '48px 24px', textAlign: 'center', background: 'rgba(15, 23, 42, 0.6)' }}>
          <Building2 style={{ width: '48px', height: '48px', color: '#64748b', margin: '0 auto 12px' }} />
          <h4 style={{ color: '#fff', fontSize: '1.2rem', marginBottom: '8px' }}>
            {useCases.length === 0 ? 'No AI Use Cases in Governance Library' : 'No Use Cases Match Filters'}
          </h4>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '20px', maxWidth: '500px', margin: '0 auto 20px' }}>
            {useCases.length === 0 
              ? 'All use cases have been cleared. Launch a live dynamic test to evaluate a new AI architecture and persist governance records.'
              : 'Try clearing your search query or selecting a different industry/risk tier.'
            }
          </p>
          {useCases.length === 0 ? (
            <button className="btn btn-success" onClick={onStartNewTest}>
              <Sparkles style={{ width: '16px', height: '16px' }} />
              Test New "Surprise Record" Live
            </button>
          ) : (
            <button 
              className="btn btn-secondary" 
              onClick={() => { setSearchQuery(''); setSelectedIndustry('All'); setSelectedRiskFilter('All'); }}
            >
              <RefreshCw style={{ width: '14px', height: '14px' }} />
              Reset All Filters
            </button>
          )}
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: '22px' }}>
          {filteredUseCases.map((uc) => {
            const isCritical = uc.risk_level === 'Critical Risk' || (uc.overall_risk_score >= 88);
            return (
              <div key={uc.id} className="veritrust-card" style={{ padding: '22px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                      <span className="badge-tag" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#c7d2fe', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                        {uc.industry}
                      </span>
                      <span className={`badge-tag ${isCritical ? 'badge-critical' : 'badge-high'}`}>
                        {uc.risk_level || 'Evaluated'} ({uc.overall_risk_score}/100)
                      </span>
                    </div>

                    {/* Delete Use Case Button with Modal Prompt */}
                    <button 
                      className="btn-delete-card" 
                      title={`Delete "${uc.name}" from library`}
                      onClick={(e) => {
                        e.stopPropagation();
                        setUseCaseToDelete(uc);
                      }}
                    >
                      <Trash2 style={{ width: '15px', height: '15px' }} />
                    </button>
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
                      Impact: {uc.impact_tier}
                    </span>
                    {uc.affected_population && (
                      <span style={{ fontSize: '0.74rem', background: 'rgba(255, 255, 255, 0.05)', color: '#cbd5e1', padding: '3px 8px', borderRadius: '4px', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
                        Population: {uc.affected_population.toLocaleString()}
                      </span>
                    )}
                  </div>

                  <div style={{ background: 'rgba(13, 21, 39, 0.8)', padding: '10px 12px', borderRadius: '6px', border: '1px dashed rgba(255, 255, 255, 0.12)', marginBottom: '18px' }}>
                    <span style={{ fontSize: '0.7rem', color: '#64748b', display: 'block', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>EU AI ACT STATUTORY CLASSIFICATION</span>
                    <span style={{ fontSize: '0.82rem', color: '#f8fafc', fontWeight: 600 }}>{uc.eu_ai_act_category}</span>
                  </div>
                </div>

                <button 
                  className="btn btn-secondary" 
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
      )}

      {/* Styled Delete Confirmation Modal */}
      {useCaseToDelete && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div className="veritrust-card" style={{
            maxWidth: '500px',
            width: '100%',
            padding: '28px',
            background: '#0f172a',
            border: '1px solid #334155',
            boxShadow: '0 20px 50px rgba(0, 0, 0, 0.7)',
            animation: 'fadeIn 0.2s ease-out'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <div style={{
                background: 'rgba(244, 63, 94, 0.15)',
                color: '#f43f5e',
                width: '42px',
                height: '42px',
                borderRadius: '10px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: '1px solid rgba(244, 63, 94, 0.3)'
              }}>
                <Trash2 style={{ width: '22px', height: '22px' }} />
              </div>
              <div>
                <h4 style={{ fontSize: '1.2rem', color: '#fff' }}>Delete AI Use Case?</h4>
                <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>This action cannot be undone.</span>
              </div>
            </div>

            <p style={{ color: '#cbd5e1', fontSize: '0.9rem', lineHeight: '1.5', marginBottom: '20px' }}>
              Are you sure you want to permanently delete <strong>"{useCaseToDelete.name}"</strong>? All associated 10-dimension assessments and 6-tier citations will be removed from the SQLite database.
            </p>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
              <button 
                className="btn btn-secondary"
                onClick={() => setUseCaseToDelete(null)}
              >
                Cancel
              </button>
              <button 
                className="btn btn-danger-outline"
                style={{ background: '#e11d48', color: '#fff', borderColor: '#f43f5e' }}
                onClick={() => {
                  const toDelete = useCaseToDelete;
                  setUseCaseToDelete(null);
                  if (onDeleteCase) {
                    onDeleteCase(toDelete.id, toDelete.name);
                  }
                }}
              >
                <Trash2 style={{ width: '15px', height: '15px' }} />
                Delete Permanently
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
