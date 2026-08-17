import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "governance_app.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Use Cases Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS use_cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        industry TEXT NOT NULL,
        purpose TEXT NOT NULL,
        autonomy_level TEXT NOT NULL,
        data_types TEXT NOT NULL, -- JSON array
        affected_population INTEGER DEFAULT 1000,
        impact_tier TEXT NOT NULL,
        is_preseeded BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Assessments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        use_case_id INTEGER NOT NULL,
        overall_risk_score REAL NOT NULL,
        risk_level TEXT NOT NULL,
        eu_ai_act_category TEXT NOT NULL,
        executive_summary TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (use_case_id) REFERENCES use_cases(id) ON DELETE CASCADE
    );
    """)

    # 3. Dimension Assessments Table (10 mandatory governance areas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dimension_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id INTEGER NOT NULL,
        dimension_key TEXT NOT NULL,
        dimension_name TEXT NOT NULL,
        risk_score REAL NOT NULL,
        risk_level TEXT NOT NULL,
        findings TEXT NOT NULL,
        regulatory_impact TEXT NOT NULL,
        mitigating_controls TEXT NOT NULL, -- JSON array
        FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
    );
    """)

    # 4. Evidence Sources Table (6 mandatory source categories)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id INTEGER NOT NULL,
        dimension_key TEXT NOT NULL,
        source_tier TEXT NOT NULL,
        title TEXT NOT NULL,
        author_entity TEXT NOT NULL,
        citation_text TEXT NOT NULL,
        url TEXT DEFAULT '',
        jurisdiction TEXT DEFAULT 'Global',
        pub_date TEXT DEFAULT '',
        reliability_score REAL DEFAULT 0.9,
        FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
    );
    """)

    # 5. Governance Knowledge Base Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_tier TEXT NOT NULL,
        title TEXT NOT NULL,
        author_entity TEXT NOT NULL,
        jurisdiction TEXT NOT NULL,
        pub_date TEXT NOT NULL,
        url TEXT DEFAULT '',
        summary_content TEXT NOT NULL,
        key_rules TEXT NOT NULL, -- JSON array
        tags TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    
    seed_knowledge_base_table()

def seed_knowledge_base_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    count = cursor.fetchone()[0]
    if count == 0:
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seed_knowledge_base.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    cursor.execute("""
                    INSERT INTO knowledge_base (source_tier, title, author_entity, jurisdiction, pub_date, url, summary_content, key_rules, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        item["source_tier"],
                        item["title"],
                        item["author_entity"],
                        item.get("jurisdiction", "Global"),
                        item.get("pub_date", "2024"),
                        item.get("url", ""),
                        item["summary_content"],
                        json.dumps(item.get("key_rules", [])),
                        item.get("tags", "")
                    ))
            conn.commit()
    conn.close()

def save_use_case(name: str, industry: str, purpose: str, autonomy_level: str, data_types: List[str], affected_population: int, impact_tier: str, is_preseeded: bool = False) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO use_cases (name, industry, purpose, autonomy_level, data_types, affected_population, impact_tier, is_preseeded)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, industry, purpose, autonomy_level, json.dumps(data_types), affected_population, impact_tier, is_preseeded))
    use_case_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return use_case_id

def save_full_assessment(use_case_id: int, overall_score: float, risk_level: str, eu_ai_act: str, summary: str, dimensions: List[Dict[str, Any]], sources: List[Dict[str, Any]]) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO assessments (use_case_id, overall_risk_score, risk_level, eu_ai_act_category, executive_summary)
    VALUES (?, ?, ?, ?, ?)
    """, (use_case_id, overall_score, risk_level, eu_ai_act, summary))
    assessment_id = cursor.lastrowid

    for dim in dimensions:
        cursor.execute("""
        INSERT INTO dimension_assessments (assessment_id, dimension_key, dimension_name, risk_score, risk_level, findings, regulatory_impact, mitigating_controls)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            dim["dimension_key"],
            dim["dimension_name"],
            dim["risk_score"],
            dim["risk_level"],
            dim["findings"],
            dim["regulatory_impact"],
            json.dumps(dim.get("mitigating_controls", []))
        ))

    for src in sources:
        cursor.execute("""
        INSERT INTO evidence_sources (assessment_id, dimension_key, source_tier, title, author_entity, citation_text, url, jurisdiction, pub_date, reliability_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            src.get("dimension_key", "general"),
            src["source_tier"],
            src["title"],
            src["author_entity"],
            src["citation_text"],
            src.get("url", ""),
            src.get("jurisdiction", "Global"),
            src.get("pub_date", "2024"),
            src.get("reliability_score", 0.9)
        ))

    conn.commit()
    conn.close()
    return assessment_id

def get_all_use_cases() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.*, a.id as assessment_id, a.overall_risk_score, a.risk_level, a.eu_ai_act_category
    FROM use_cases u
    LEFT JOIN assessments a ON u.id = a.use_case_id
    ORDER BY u.created_at DESC
    """)
    rows = cursor.fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "name": r["name"],
            "industry": r["industry"],
            "purpose": r["purpose"],
            "autonomy_level": r["autonomy_level"],
            "data_types": json.loads(r["data_types"]) if r["data_types"] else [],
            "affected_population": r["affected_population"],
            "impact_tier": r["impact_tier"],
            "is_preseeded": bool(r["is_preseeded"]),
            "created_at": r["created_at"],
            "assessment_id": r["assessment_id"],
            "overall_risk_score": r["overall_risk_score"],
            "risk_level": r["risk_level"],
            "eu_ai_act_category": r["eu_ai_act_category"]
        })
    conn.close()
    return results

def get_assessment_details(assessment_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT a.*, u.name as use_case_name, u.industry, u.purpose, u.autonomy_level, u.data_types, u.affected_population, u.impact_tier
    FROM assessments a
    JOIN use_cases u ON a.use_case_id = u.id
    WHERE a.id = ?
    """, (assessment_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    assessment = {
        "id": row["id"],
        "use_case_id": row["use_case_id"],
        "use_case_name": row["use_case_name"],
        "industry": row["industry"],
        "purpose": row["purpose"],
        "autonomy_level": row["autonomy_level"],
        "data_types": json.loads(row["data_types"]) if row["data_types"] else [],
        "affected_population": row["affected_population"],
        "impact_tier": row["impact_tier"],
        "overall_risk_score": row["overall_risk_score"],
        "risk_level": row["risk_level"],
        "eu_ai_act_category": row["eu_ai_act_category"],
        "executive_summary": row["executive_summary"],
        "created_at": row["created_at"],
        "dimensions": [],
        "sources": []
    }

    cursor.execute("SELECT * FROM dimension_assessments WHERE assessment_id = ?", (assessment_id,))
    dim_rows = cursor.fetchall()
    for d in dim_rows:
        assessment["dimensions"].append({
            "id": d["id"],
            "dimension_key": d["dimension_key"],
            "dimension_name": d["dimension_name"],
            "risk_score": d["risk_score"],
            "risk_level": d["risk_level"],
            "findings": d["findings"],
            "regulatory_impact": d["regulatory_impact"],
            "mitigating_controls": json.loads(d["mitigating_controls"]) if d["mitigating_controls"] else []
        })

    cursor.execute("SELECT * FROM evidence_sources WHERE assessment_id = ?", (assessment_id,))
    src_rows = cursor.fetchall()
    for s in src_rows:
        assessment["sources"].append({
            "id": s["id"],
            "dimension_key": s["dimension_key"],
            "source_tier": s["source_tier"],
            "title": s["title"],
            "author_entity": s["author_entity"],
            "citation_text": s["citation_text"],
            "url": s["url"],
            "jurisdiction": s["jurisdiction"],
            "pub_date": s["pub_date"],
            "reliability_score": s["reliability_score"]
        })

    conn.close()
    return assessment

def query_knowledge_base(query: str = "", source_tier: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    q = f"%{query.strip().lower()}%"
    
    if source_tier:
        cursor.execute("""
        SELECT * FROM knowledge_base
        WHERE source_tier = ? AND (
            LOWER(title) LIKE ? OR 
            LOWER(summary_content) LIKE ? OR 
            LOWER(tags) LIKE ? OR 
            LOWER(author_entity) LIKE ? OR
            LOWER(key_rules) LIKE ?
        )
        """, (source_tier, q, q, q, q, q))
    else:
        cursor.execute("""
        SELECT * FROM knowledge_base
        WHERE LOWER(title) LIKE ? OR 
              LOWER(summary_content) LIKE ? OR 
              LOWER(tags) LIKE ? OR 
              LOWER(source_tier) LIKE ? OR
              LOWER(author_entity) LIKE ? OR
              LOWER(key_rules) LIKE ?
        """, (q, q, q, q, q, q))
        
    rows = cursor.fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "source_tier": r["source_tier"],
            "title": r["title"],
            "author_entity": r["author_entity"],
            "jurisdiction": r["jurisdiction"],
            "pub_date": r["pub_date"],
            "url": r["url"],
            "summary_content": r["summary_content"],
            "key_rules": json.loads(r["key_rules"]) if r["key_rules"] else [],
            "tags": r["tags"]
        })
    conn.close()
    return results

def delete_use_case(use_case_id: int) -> bool:
    """
    Deletes a specific use case and cascades deletion to assessments,
    dimension_assessments, and evidence_sources.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Fetch associated assessment IDs
    cursor.execute("SELECT id FROM assessments WHERE use_case_id = ?", (use_case_id,))
    assessment_rows = cursor.fetchall()
    
    for row in assessment_rows:
        aid = row["id"]
        # Delete evidence sources
        cursor.execute("DELETE FROM evidence_sources WHERE assessment_id = ?", (aid,))
        # Delete dimension assessments
        cursor.execute("DELETE FROM dimension_assessments WHERE assessment_id = ?", (aid,))
    
    # 2. Delete assessments
    cursor.execute("DELETE FROM assessments WHERE use_case_id = ?", (use_case_id,))
    
    # 3. Delete use case
    cursor.execute("DELETE FROM use_cases WHERE id = ?", (use_case_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    return deleted

