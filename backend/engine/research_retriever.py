"""
Hybrid Governance Research Retriever
Combines local multi-tier knowledge base retrieval with real-time web search for surprise AI use cases.
"""

import json
import os
import httpx
from typing import List, Dict, Any
from database.db_manager import query_knowledge_base
from engine.evidence_classifier import enrich_source_metadata, classify_source_tier

SEED_KB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seed_knowledge_base.json")

def load_seed_kb() -> List[Dict[str, Any]]:
    if os.path.exists(SEED_KB_PATH):
        try:
            with open(SEED_KB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def search_local_governance_kb(use_case_name: str, industry: str, purpose: str) -> List[Dict[str, Any]]:
    kb_data = load_seed_kb()
    if not kb_data:
        kb_data = query_knowledge_base("")

    matched_sources = []
    query_terms = set(f"{use_case_name} {industry} {purpose}".lower().split())

    for item in kb_data:
        item_text = f"{item['title']} {item['summary_content']} {item.get('tags', '')} {item['source_tier']}".lower()
        score = 0
        
        # Keyword relevance
        for term in query_terms:
            if len(term) > 3 and term in item_text:
                score += 1

        # Industry affinity
        ind_lower = industry.lower()
        if "credit" in ind_lower or "financial" in ind_lower or "bank" in ind_lower:
            if "ecoa" in item_text or "financial" in item_text or "credit" in item_text:
                score += 3
        elif "health" in ind_lower or "medical" in ind_lower:
            if "hipaa" in item_text or "health" in item_text or "medical" in item_text:
                score += 3
        elif "hr" in ind_lower or "hiring" in ind_lower or "employment" in ind_lower:
            if "nyc ll144" in item_text or "eeoc" in item_text or "employment" in item_text:
                score += 3

        # Always include baseline EU AI Act and NIST AI RMF
        if "eu ai act" in item_text or "nist ai rmf" in item_text or "iso/iec 42001" in item_text:
            score += 2

        if score > 0:
            matched_sources.append({
                "source_tier": item["source_tier"],
                "title": item["title"],
                "author_entity": item["author_entity"],
                "citation_text": item["summary_content"],
                "url": item.get("url", ""),
                "jurisdiction": item.get("jurisdiction", "Global"),
                "pub_date": item.get("pub_date", "2024"),
                "relevance_score": score
            })

    # Sort by relevance score
    matched_sources.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Enrich with 6-tier classification
    return [enrich_source_metadata(s) for s in matched_sources[:8]]

async def fetch_live_web_governance(query: str) -> List[Dict[str, Any]]:
    """Fetches real-time public governance information for surprise use cases."""
    results = []
    try:
        url = f"https://api.duckduckgo.com/?q={query}+AI+governance+regulation+risk&format=json"
        async with httpx.AsyncClient(timeout=4.0) as client:
            res = await client.get(url)
            if res.status_code == 200:
                data = res.json()
                abstract = data.get("AbstractText", "")
                heading = data.get("Heading", "")
                if abstract and heading:
                    results.append(enrich_source_metadata({
                        "source_tier": "General Web Content",
                        "title": f"DuckDuckGo Public Search: {heading}",
                        "author_entity": "Web Public Knowledge",
                        "citation_text": abstract,
                        "url": data.get("AbstractURL", ""),
                        "jurisdiction": "Global Web",
                        "pub_date": "2024"
                    }))
                
                for topic in data.get("RelatedTopics", [])[:3]:
                    if "Text" in topic:
                        results.append(enrich_source_metadata({
                            "source_tier": "General Web Content",
                            "title": f"Web Source: {topic.get('FirstURL', '').split('/')[-1]}",
                            "author_entity": "Public Web Repository",
                            "citation_text": topic["Text"],
                            "url": topic.get("FirstURL", ""),
                            "jurisdiction": "Global",
                            "pub_date": "2024"
                        }))
    except Exception:
        pass
    return results

async def retrieve_governance_evidence(use_case_name: str, industry: str, purpose: str) -> List[Dict[str, Any]]:
    sources = search_local_governance_kb(use_case_name, industry, purpose)
    
    # Try fetching live web research for dynamic surprise use cases
    web_sources = await fetch_live_web_governance(f"{industry} {use_case_name}")
    if web_sources:
        sources.extend(web_sources)

    # Ensure diversity across 6 source tiers
    seen_tiers = set()
    deduped = []
    for s in sources:
        key = f"{s['title']}_{s['source_tier']}"
        if key not in seen_tiers:
            seen_tiers.add(key)
            deduped.append(s)

    return deduped[:10]
