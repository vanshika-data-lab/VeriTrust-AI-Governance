"""
6-Tier Source Classifier for AI Governance
Categorizes retrieved evidence into:
- Law / Regulation
- Regulatory Guidance
- Industry Standard
- Research
- Vendor Information
- General Web Content
"""

from typing import Dict, Any

LAW_KEYWORDS = ["act", "regulation", "statute", "directive", "law", "code of federal regulations", "cfr", "gdpr", "hipaa", "ecoa", "article"]
GUIDANCE_KEYWORDS = ["guidance", "framework", "circular", "enforcement", "bulletin", "advisory", "nist ai rmf", "ftc guidance", "eeoc select issues"]
STANDARD_KEYWORDS = ["iso", "iec", "ieee", "soc 2", "aicpa", "ansi", "standard", "bsi", "nist sp 800"]
RESEARCH_KEYWORDS = ["paper", "journal", "proceedings", "acm", "arxiv", "stanford hai", "empirical study", "technical report", "doi"]
VENDOR_KEYWORDS = ["aws", "amazon", "microsoft", "google", "openai", "anthropic", "ibm", "nvidia", "vendor", "cloud", "documentation"]

def classify_source_tier(title: str, author_entity: str, url: str = "", text_content: str = "") -> str:
    combined = f"{title} {author_entity} {url} {text_content}".lower()

    if any(k in combined for k in LAW_KEYWORDS) and ("eu ai act" in combined or "regulation" in combined or "law" in combined or "act" in combined):
        return "Law / Regulation"
    
    if any(k in combined for k in STANDARD_KEYWORDS):
        return "Industry Standard"

    if any(k in combined for k in GUIDANCE_KEYWORDS):
        return "Regulatory Guidance"

    if any(k in combined for k in RESEARCH_KEYWORDS):
        return "Research"

    if any(k in combined for k in VENDOR_KEYWORDS):
        return "Vendor Information"

    return "General Web Content"

def enrich_source_metadata(source: Dict[str, Any]) -> Dict[str, Any]:
    tier = classify_source_tier(
        title=source.get("title", ""),
        author_entity=source.get("author_entity", ""),
        url=source.get("url", ""),
        text_content=source.get("citation_text", "")
    )
    
    # Tier reliability score weighting
    reliability_map = {
        "Law / Regulation": 0.98,
        "Regulatory Guidance": 0.93,
        "Industry Standard": 0.90,
        "Research": 0.85,
        "Vendor Information": 0.78,
        "General Web Content": 0.65
    }

    source["source_tier"] = source.get("source_tier") or tier
    source["reliability_score"] = reliability_map.get(source["source_tier"], 0.75)
    return source
