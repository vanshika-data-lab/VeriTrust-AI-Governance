import React from 'react';
import { ShieldCheck, LayoutDashboard, PlusCircle, BookOpen, Activity } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <header style={{ 
      background: '#0f172a', 
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)', 
      position: 'sticky', 
      top: 0, 
      zIndex: 100 
    }}>
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justify: 'space-between', 
        maxWidth: '1440px', 
        margin: '0 auto', 
        padding: '14px 28px',
        gap: '24px'
      }}>
        
        {/* Brand Logo */}
        <div 
          style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer', flexShrink: 0 }} 
          onClick={() => setActiveTab('dashboard')}
        >
          <div style={{ 
            background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)', 
            padding: '9px', 
            borderRadius: '10px', 
            display: 'flex', 
            alignItems: 'center', 
            justify: 'center',
            boxShadow: '0 4px 14px rgba(37, 99, 235, 0.35)'
          }}>
            <ShieldCheck style={{ width: '24px', height: '24px', color: '#fff' }} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.3rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '6px', lineHeight: 1 }}>
              VeriTrust <span style={{ color: '#60a5fa', fontWeight: 700 }}>AI</span>
            </h1>
            <p style={{ fontSize: '0.68rem', color: '#94a3b8', letterSpacing: '0.05em', textTransform: 'uppercase', marginTop: '3px', fontWeight: 600 }}>
              ENTERPRISE AI GOVERNANCE & RISK PLATFORM
            </p>
          </div>
        </div>

        {/* High-Visibility Navigation Tabs */}
        <nav style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <button 
            className={`nav-tab-btn ${activeTab === 'dashboard' ? 'active-dashboard' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            <LayoutDashboard style={{ width: '16px', height: '16px', color: activeTab === 'dashboard' ? '#fff' : '#60a5fa' }} />
            Risk Dashboard
          </button>

          <button 
            className={`nav-tab-btn ${activeTab === 'assess' ? 'active-assess' : ''}`}
            onClick={() => setActiveTab('assess')}
          >
            <PlusCircle style={{ width: '16px', height: '16px', color: activeTab === 'assess' ? '#fff' : '#34d399' }} />
            Dynamic "Surprise Record" Test
          </button>

          <button 
            className={`nav-tab-btn ${activeTab === 'knowledge' ? 'active-knowledge' : ''}`}
            onClick={() => setActiveTab('knowledge')}
          >
            <BookOpen style={{ width: '16px', height: '16px', color: activeTab === 'knowledge' ? '#fff' : '#c084fc' }} />
            6-Tier Knowledge Base
          </button>
        </nav>

        {/* Engine Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
          <div style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '6px', 
            fontSize: '0.78rem', 
            background: 'rgba(16, 185, 129, 0.15)', 
            padding: '6px 14px', 
            borderRadius: '20px', 
            border: '1px solid rgba(16, 185, 129, 0.4)', 
            color: '#6ee7b7',
            fontWeight: 600
          }}>
            <Activity style={{ width: '13px', height: '13px' }} />
            <span>SQLite Engine Active</span>
          </div>
        </div>

      </div>
    </header>
  );
}
