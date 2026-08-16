import React, { useState } from 'react';
import { X, ExternalLink, ShieldCheck, Scale, FileText, Award, BookOpen, Building, Globe } from 'lucide-react';

export default function EvidenceDrawer({ sources, onClose }) {
  const [selectedTier, setSelectedTier] = useState('All');

  const tiers = [
    { key: 'All', label: 'All Sources', icon: ShieldCheck },
    { key: 'Law / Regulation', label: 'Law / Regulation', icon: Scale, badgeClass: 'tier-law' },
    { key: 'Regulatory Guidance', label: 'Regulatory Guidance', icon: FileText, badgeClass: 'tier-guidance' },
    { key: 'Industry Standard', label: 'Industry Standard', icon: Award, badgeClass: 'tier-standard' },
    { key: 'Research', label: 'Research', icon: BookOpen, badgeClass: 'tier-research' },
    { key: 'Vendor Information', label: 'Vendor Information', icon: Building, badgeClass: 'tier-vendor' },
    { key: 'General Web Content', label: 'General Web Content', icon: Globe, badgeClass: 'tier-web' }
  ];

  const filteredSources = selectedTier === 'All' 
    ? sources 
    : sources.filter(s => s.source_tier === selectedTier);

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      right: 0,
      bottom: 0,
      width: '650px',
      maxWidth: '90vw',
      background: 'rgba(13, 21, 39, 0.96)',
      backdropFilter: 'blur(24px)',
      borderLeft: '1px solid rgba(255, 255, 255, 0.15)',
      boxShadow: '-10px 0 30px rgba(0, 0, 0, 0.6)',
      zIndex: 200,
      display: 'flex',
      flexDirection: 'column'
    }}>
      
      {/* Drawer Header */}
      <div style={{ padding: '20px 24px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: '1.2rem', color: '#fff' }}>6-Tier Governance Evidence & Citations</h3>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Categorized source metadata and statutory citations backing risk findings</p>
        </div>
        <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '6px' }}>
          <X style={{ width: '22px', height: '22px' }} />
        </button>
      </div>

      {/* 6 Tier Tabs */}
      <div style={{ padding: '12px 24px', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', gap: '6px', overflowX: 'auto' }}>
        {tiers.map(t => (
          <button 
            key={t.key}
            onClick={() => setSelectedTier(t.key)}
            style={{
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '0.78rem',
              fontWeight: 600,
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              border: selectedTier === t.key ? '1px solid #6366f1' : '1px solid rgba(255, 255, 255, 0.08)',
              background: selectedTier === t.key ? 'rgba(99, 102, 241, 0.25)' : 'rgba(255, 255, 255, 0.03)',
              color: selectedTier === t.key ? '#a5b4fc' : '#94a3b8'
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Sources List */}
      <div style={{ padding: '20px 24px', flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {filteredSources.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#64748b', padding: '40px' }}>
            No sources retrieved for category '{selectedTier}'
          </div>
        ) : (
          filteredSources.map((src, idx) => (
            <div key={idx} className="glass-card" style={{ padding: '16px', background: 'rgba(17, 24, 39, 0.7)' }}>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span className="tier-badge" style={{ background: 'rgba(99, 102, 241, 0.2)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                  {src.source_tier}
                </span>
                <span style={{ fontSize: '0.72rem', color: '#6ee7b7', fontFamily: 'var(--font-mono)' }}>
                  Reliability: {Math.round((src.reliability_score || 0.9) * 100)}%
                </span>
              </div>

              <h4 style={{ fontSize: '1rem', color: '#fff', marginBottom: '4px' }}>{src.title}</h4>
              <div style={{ fontSize: '0.78rem', color: '#64748b', marginBottom: '10px' }}>
                Entity: {src.author_entity} • Jurisdiction: {src.jurisdiction} • Date: {src.pub_date}
              </div>

              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: '1.5', marginBottom: '12px', background: 'rgba(13, 21, 39, 0.5)', padding: '10px', borderRadius: '6px' }}>
                "{src.citation_text}"
              </p>

              {src.url && (
                <a 
                  href={src.url} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '0.78rem', color: '#6366f1', textDecoration: 'none', fontWeight: 600 }}
                >
                  Verify Source Citation <ExternalLink style={{ width: '12px', height: '12px' }} />
                </a>
              )}

            </div>
          ))
        )}
      </div>

    </div>
  );
}
