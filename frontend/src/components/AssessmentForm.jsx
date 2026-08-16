import React, { useState } from 'react';
import { Sparkles, ArrowLeft, ShieldAlert, Cpu, Database, FileText, CheckCircle } from 'lucide-react';

export default function AssessmentForm({ onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    industry: 'BFSI / Financial Services',
    purpose: '',
    autonomy_level: 'Human-on-the-Loop',
    data_types: ['PII', 'Financial'],
    affected_population: 50000,
    impact_tier: 'High'
  });

  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  const availableDataTypes = [
    'PII', 'Biometric', 'Medical', 'Financial', 'Credit History', 
    'Protected Attributes', 'Video Audio', 'Public Data', 'Telemetry Data'
  ];

  const surprisePresets = [
    {
      name: "Generative AI Claims Settlement Agent",
      industry: "Insurance & Claims",
      purpose: "LLM agent that ingests damage photos and medical bills to automatically calculate and approve payout amounts under $10,000.",
      autonomy_level: "Fully Autonomous",
      data_types: ["PII", "Financial", "Medical"],
      affected_population: 120000,
      impact_tier: "High"
    },
    {
      name: "Biometric AI Attendance & Mood Monitor",
      industry: "Corporate & Workplace",
      purpose: "Facial recognition camera system deployed in office hallways to track employee physical presence and analyze emotional stress levels.",
      autonomy_level: "Fully Autonomous",
      data_types: ["PII", "Biometric", "Video Audio"],
      affected_population: 5000,
      impact_tier: "Critical"
    },
    {
      name: "AI Autonomous Flight Path Collision Avoidance",
      industry: "Aviation & Aerospace",
      purpose: "Edge AI system mounted on commercial aircraft that autonomously modifies flight trajectory during sudden turbulence or drone proximity.",
      autonomy_level: "Human-on-the-Loop",
      data_types: ["Telemetry Data", "Public Data"],
      affected_population: 1000000,
      impact_tier: "Critical"
    }
  ];

  const handleToggleDataType = (type) => {
    if (formData.data_types.includes(type)) {
      setFormData({ ...formData, data_types: formData.data_types.filter(t => t !== type) });
    } else {
      setFormData({ ...formData, data_types: [...formData.data_types, type] });
    }
  };

  const handleLoadPreset = (preset) => {
    setFormData(preset);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name || !formData.purpose) return;

    setLoading(true);
    setCurrentStep(1);

    const timer1 = setTimeout(() => setCurrentStep(2), 700);
    const timer2 = setTimeout(() => setCurrentStep(3), 1500);
    const timer3 = setTimeout(() => setCurrentStep(4), 2200);

    setTimeout(async () => {
      try {
        await onSubmit(formData);
      } catch (err) {
        alert("Error generating assessment: " + err.message);
      } finally {
        setLoading(false);
      }
    }, 2800);
  };

  return (
    <div style={{ maxWidth: '920px', margin: '28px auto', padding: '0 28px' }}>
      
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '24px' }}>
        <button className="btn-v btn-v-outline" onClick={onCancel} style={{ padding: '8px 14px' }}>
          <ArrowLeft style={{ width: '16px', height: '16px' }} />
          Back to Dashboard
        </button>
        <div>
          <h2 style={{ fontSize: '1.6rem', color: '#fff' }}>Dynamic "Surprise Record" Live Assessment</h2>
          <p style={{ color: '#cbd5e1', fontSize: '0.9rem' }}>Enter any novel AI use case to execute dynamic retrieval and 10-dimension assessment.</p>
        </div>
      </div>

      {/* Preset Pickers with High Contrast & Readability */}
      <div className="veritrust-card" style={{ padding: '18px 22px', marginBottom: '24px', background: 'rgba(30, 41, 59, 0.9)', borderLeft: '4px solid #38bdf8' }}>
        <span style={{ fontSize: '0.82rem', color: '#38bdf8', fontWeight: 700, display: 'block', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
          ⚡ QUICK LOAD SAMPLE DEMO USE CASES:
        </span>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          {surprisePresets.map((preset, idx) => (
            <button 
              key={idx} 
              type="button" 
              onClick={() => handleLoadPreset(preset)}
              style={{ 
                fontSize: '0.82rem', 
                padding: '8px 14px', 
                background: '#1e293b', 
                color: '#38bdf8', 
                border: '1px solid #0284c7', 
                borderRadius: '6px', 
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              + {preset.name}
            </button>
          ))}
        </div>
      </div>

      {/* Form Container */}
      <div className="veritrust-card" style={{ padding: '32px' }}>
        
        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px 20px' }}>
            <Sparkles style={{ width: '48px', height: '48px', color: '#60a5fa', animation: 'spin 2s linear infinite', marginBottom: '20px' }} />
            <h3 style={{ fontSize: '1.4rem', color: '#fff', marginBottom: '16px' }}>Evaluating AI System Governance...</h3>
            
            <div style={{ maxWidth: '520px', margin: '0 auto', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: currentStep >= 1 ? '#6ee7b7' : '#94a3b8', fontSize: '0.92rem' }}>
                {currentStep >= 1 ? <CheckCircle style={{ width: '18px', height: '18px', color: '#10b981' }} /> : <Cpu style={{ width: '18px', height: '18px' }} />}
                <span>Step 1: Parsing System Architecture & Data Flow</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: currentStep >= 2 ? '#6ee7b7' : '#94a3b8', fontSize: '0.92rem' }}>
                {currentStep >= 2 ? <CheckCircle style={{ width: '18px', height: '18px', color: '#10b981' }} /> : <ShieldAlert style={{ width: '18px', height: '18px' }} />}
                <span>Step 2: Computing Deterministic 10-Dimension Risk Matrix</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: currentStep >= 3 ? '#6ee7b7' : '#94a3b8', fontSize: '0.92rem' }}>
                {currentStep >= 3 ? <CheckCircle style={{ width: '18px', height: '18px', color: '#10b981' }} /> : <Database style={{ width: '18px', height: '18px' }} />}
                <span>Step 3: Searching 6-Tier Regulatory & Research Knowledge Base</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: currentStep >= 4 ? '#6ee7b7' : '#94a3b8', fontSize: '0.92rem' }}>
                {currentStep >= 4 ? <CheckCircle style={{ width: '18px', height: '18px', color: '#10b981' }} /> : <FileText style={{ width: '18px', height: '18px' }} />}
                <span>Step 4: Synthesizing Statutory Obligations & Mitigating Controls</span>
              </div>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '22px' }}>
            
            {/* System Name */}
            <div>
              <label style={{ display: 'block', fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px', fontWeight: 600 }}>
                AI Use Case / System Name *
              </label>
              <input 
                type="text" 
                required
                placeholder="e.g. Algorithmic Credit Line Underwriting Engine"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                style={{ width: '100%', padding: '12px 16px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.95rem' }}
              />
            </div>

            {/* Industry & Autonomy Level */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px', fontWeight: 600 }}>
                  Industry Sector *
                </label>
                <select 
                  value={formData.industry}
                  onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                  style={{ width: '100%', padding: '12px 16px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.95rem' }}
                >
                  <option value="BFSI / Financial Services">BFSI / Financial Services</option>
                  <option value="Healthcare & Life Sciences">Healthcare & Life Sciences</option>
                  <option value="HR & Employment">HR & Employment</option>
                  <option value="Aviation & Aerospace">Aviation & Aerospace</option>
                  <option value="Insurance & Claims">Insurance & Claims</option>
                  <option value="Corporate & Workplace">Corporate & Workplace</option>
                  <option value="Retail & E-Commerce">Retail & E-Commerce</option>
                  <option value="Legal & Law Enforcement">Legal & Law Enforcement</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px', fontWeight: 600 }}>
                  Decision Autonomy Level *
                </label>
                <select 
                  value={formData.autonomy_level}
                  onChange={(e) => setFormData({ ...formData, autonomy_level: e.target.value })}
                  style={{ width: '100%', padding: '12px 16px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.95rem' }}
                >
                  <option value="Fully Autonomous">Fully Autonomous (No human in loop)</option>
                  <option value="Human-on-the-Loop">Human-on-the-Loop (Supervisory oversight)</option>
                  <option value="Human-in-the-Loop">Human-in-the-Loop (Human sign-off required)</option>
                  <option value="Advisory / Decision Support">Advisory / Decision Support (Informational)</option>
                </select>
              </div>
            </div>

            {/* Purpose */}
            <div>
              <label style={{ display: 'block', fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px', fontWeight: 600 }}>
                Intended Purpose & Operational Description *
              </label>
              <textarea 
                required
                rows={3}
                placeholder="Describe what the AI model does, how decisions are rendered, and affected stakeholders..."
                value={formData.purpose}
                onChange={(e) => setFormData({ ...formData, purpose: e.target.value })}
                style={{ width: '100%', padding: '12px 16px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.95rem', fontFamily: 'inherit' }}
              />
            </div>

            {/* Data Types Selection */}
            <div>
              <label style={{ display: 'block', fontSize: '0.9rem', color: '#f8fafc', marginBottom: '10px', fontWeight: 600 }}>
                Data Types Processed by Model
              </label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {availableDataTypes.map((type) => {
                  const selected = formData.data_types.includes(type);
                  return (
                    <button 
                      key={type}
                      type="button"
                      onClick={() => handleToggleDataType(type)}
                      style={{
                        padding: '7px 14px',
                        borderRadius: '6px',
                        fontSize: '0.84rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                        border: selected ? '1px solid #3b82f6' : '1px solid #334155',
                        background: selected ? '#1e3a8a' : '#1e293b',
                        color: selected ? '#93c5fd' : '#cbd5e1'
                      }}
                    >
                      {selected ? '✓ ' : '+ '}{type}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Population & Impact Tier */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px', fontWeight: 600 }}>
                  Estimated Affected Population
                </label>
                <input 
                  type="number" 
                  value={formData.affected_population}
                  onChange={(e) => setFormData({ ...formData, affected_population: parseInt(e.target.value) || 1000 })}
                  style={{ width: '100%', padding: '12px 16px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.95rem' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.9rem', color: '#f8fafc', marginBottom: '8px', fontWeight: 600 }}>
                  Potential Decision Impact Severity
                </label>
                <select 
                  value={formData.impact_tier}
                  onChange={(e) => setFormData({ ...formData, impact_tier: e.target.value })}
                  style={{ width: '100%', padding: '12px 16px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.95rem' }}
                >
                  <option value="Critical">Critical (Irreversible financial, physical, or rights harm)</option>
                  <option value="High">High (Significant impact on credit, hiring, health)</option>
                  <option value="Medium">Medium (Operational impact with user recourse)</option>
                  <option value="Low">Low (Informational / low stakes)</option>
                </select>
              </div>
            </div>

            {/* High-Visibility Gradient Submit CTA */}
            <button 
              className="btn-v btn-v-primary" 
              type="submit" 
              style={{ 
                padding: '14px', 
                fontSize: '1.02rem', 
                marginTop: '10px',
                background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
                color: '#ffffff',
                fontWeight: 700,
                border: '1px solid #3b82f6',
                boxShadow: '0 4px 18px rgba(37, 99, 235, 0.4)'
              }}
            >
              <Sparkles style={{ width: '18px', height: '18px' }} />
              Execute Dynamic 10-Dimension Risk & Evidence Assessment
            </button>

          </form>
        )}

      </div>

    </div>
  );
}
