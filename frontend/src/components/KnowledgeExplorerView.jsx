import React, { useState, useEffect } from 'react';
import { BookOpen, Search, ExternalLink } from 'lucide-react';

export default function KnowledgeExplorerView() {
  const [sources, setSources] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTier, setSelectedTier] = useState('');

  useEffect(() => {
    fetchSources();
  }, [searchQuery, selectedTier]);

  const fetchSources = async () => {
    try {
      let url = `/api/sources?query=${encodeURIComponent(searchQuery)}`;
      if (selectedTier) url += `&source_tier=${encodeURIComponent(selectedTier)}`;
      const res = await fetch(url);
      const data = await res.json();
      setSources(data);
    } catch (err) {
      console.error("Error fetching knowledge base:", err);
    }
  };

  return (
    <div style={{ maxWidth: '1440px', margin: '28px auto', padding: '0 28px' }}>
      
      <div className="veritrust-card" style={{ padding: '28px', marginBottom: '28px', background: '#0f172a' }}>
        <h2 style={{ fontSize: '1.75rem', color: '#fff', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <BookOpen style={{ width: '24px', height: '24px', color: '#818cf8' }} />
          6-Tier Governance & Regulatory Knowledge Base
        </h2>
        <p style={{ color: '#cbd5e1', fontSize: '0.94rem', marginBottom: '20px' }}>
          Explore curated legal statutes, regulatory guidance, industry standards, research benchmarks, vendor specs, and web analysis.
        </p>

        {/* Search Bar & Tier Filter */}
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '280px', position: 'relative' }}>
            <Search style={{ width: '18px', height: '18px', color: '#64748b', position: 'absolute', left: '14px', top: '14px' }} />
            <input 
              type="text" 
              placeholder="Search statutes (e.g. EU AI Act, GDPR, HIPAA, NIST AI RMF, NYC LL144)..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ width: '100%', padding: '12px 14px 12px 42px', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.95rem' }}
            />
          </div>

          <select 
            value={selectedTier}
            onChange={(e) => setSelectedTier(e.target.value)}
            style={{ padding: '12px 16px', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.95rem' }}
          >
            <option value="">All 6 Source Tiers</option>
            <option value="Law / Regulation">Law / Regulation</option>
            <option value="Regulatory Guidance">Regulatory Guidance</option>
            <option value="Industry Standard">Industry Standard</option>
            <option value="Research">Research</option>
            <option value="Vendor Information">Vendor Information</option>
            <option value="General Web Content">General Web Content</option>
          </select>
        </div>
      </div>

      {/* Grid of KB cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(420px, 1fr))', gap: '22px' }}>
        {sources.map((item) => (
          <div key={item.id} className="veritrust-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span className="badge-tag tier-law" style={{ background: 'rgba(99, 102, 241, 0.25)', color: '#c7d2fe', border: '1px solid rgba(99, 102, 241, 0.4)' }}>
                  {item.source_tier}
                </span>
                <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontWeight: 600 }}>{item.jurisdiction}</span>
              </div>

              <h3 style={{ fontSize: '1.18rem', color: '#fff', marginBottom: '6px', lineHeight: '1.3' }}>{item.title}</h3>
              <div style={{ fontSize: '0.82rem', color: '#94a3b8', marginBottom: '12px' }}>
                {item.author_entity} • {item.pub_date}
              </div>

              <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: '1.5', marginBottom: '16px' }}>
                {item.summary_content}
              </p>

              {/* Key Rules List */}
              {item.key_rules && item.key_rules.length > 0 && (
                <div style={{ background: 'rgba(15, 23, 42, 0.7)', padding: '14px', borderRadius: '8px', marginBottom: '16px', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
                  <span style={{ fontSize: '0.78rem', color: '#60a5fa', fontWeight: 700, display: 'block', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                    KEY STATUTORY ARTICLES & MANDATES:
                  </span>
                  <ul style={{ paddingLeft: '18px', fontSize: '0.82rem', color: '#e2e8f0', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    {item.key_rules.map((rule, idx) => (
                      <li key={idx}>{rule}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {item.url && (
              <a 
                href={item.url} 
                target="_blank" 
                rel="noopener noreferrer" 
                style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.84rem', color: '#60a5fa', textDecoration: 'none', fontWeight: 600, marginTop: '8px' }}
              >
                Access Official Statutory Reference Document <ExternalLink style={{ width: '14px', height: '14px' }} />
              </a>
            )}
          </div>
        ))}
      </div>

    </div>
  );
}
