import json
import random
from pathlib import Path
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

TEAMS = [
    {"id": "TEAM-CORE", "name": "Core Platform"},
    {"id": "TEAM-DATA", "name": "Data Infrastructure"},
    {"id": "TEAM-FIN", "name": "FinOps & Billing"},
    {"id": "TEAM-SEC", "name": "Security & Identity"},
]

PEOPLE = [
    {"id": "PER-ALEX", "name": "Alex Rivera", "role": "Lead Architect", "email": "alex@company.internal", "team_id": "TEAM-CORE"},
    {"id": "PER-SARAH", "name": "Sarah Chen", "role": "Head of Payments", "email": "sarah@company.internal", "team_id": "TEAM-FIN"},
    {"id": "PER-DEVON", "name": "Devon Vance", "role": "Principal SRE", "email": "devon@company.internal", "team_id": "TEAM-CORE"},
    {"id": "PER-PRIYA", "name": "Priya Nair", "role": "Staff Data Engineer", "email": "priya@company.internal", "team_id": "TEAM-DATA"},
    {"id": "PER-MARCUS", "name": "Marcus Brody", "role": "Security Director", "email": "marcus@company.internal", "team_id": "TEAM-SEC"},
    {"id": "PER-ELENA", "name": "Elena Rostova", "role": "Backend Lead", "email": "elena@company.internal", "team_id": "TEAM-CORE"},
    {"id": "PER-LIAM", "name": "Liam O'Connor", "role": "DevOps Engineer", "email": "liam@company.internal", "team_id": "TEAM-CORE"},
    {"id": "PER-MAYA", "name": "Maya Lin", "role": "Product Manager", "email": "maya@company.internal", "team_id": "TEAM-FIN"},
    {"id": "PER-KAI", "name": "Kai Tanaka", "role": "Frontend Architect", "email": "kai@company.internal", "team_id": "TEAM-CORE"},
    {"id": "PER-CHLOE", "name": "Chloe Bennett", "role": "Compliance Officer", "email": "chloe@company.internal", "team_id": "TEAM-SEC"},
    {"id": "PER-OMAR", "name": "Omar Farooq", "role": "ML Platform Engineer", "email": "omar@company.internal", "team_id": "TEAM-DATA"},
    {"id": "PER-ZOE", "name": "Zoe Kim", "role": "Senior Backend Dev", "email": "zoe@company.internal", "team_id": "TEAM-CORE"},
    {"id": "PER-DAVID", "name": "David Ross", "role": "Infrastructure Eng", "email": "david@company.internal", "team_id": "TEAM-DATA"},
    {"id": "PER-NINA", "name": "Nina Patel", "role": "Billing Engineer", "email": "nina@company.internal", "team_id": "TEAM-FIN"},
    {"id": "PER-TARIQ", "name": "Tariq Mansoor", "role": "IAM Specialist", "email": "tariq@company.internal", "team_id": "TEAM-SEC"},
    {"id": "PER-SOPHIA", "name": "Sophia Becker", "role": "Database Admin", "email": "sophia@company.internal", "team_id": "TEAM-DATA"},
    {"id": "PER-JUCAS", "name": "Lucas Silva", "role": "Staff Platform Eng", "email": "lucas@company.internal", "team_id": "TEAM-CORE"},
    {"id": "PER-HANNAH", "name": "Hannah Ward", "role": "FinOps Analyst", "email": "hannah@company.internal", "team_id": "TEAM-FIN"},
]

DOMAINS = ["Database", "Architecture", "Billing", "Security", "Infrastructure", "API", "Frontend", "Analytics"]

def generate_seed_dataset():
    decisions = []
    assumptions = []
    sources = []
    tickets = []
    events = []
    
    # 1. Planted Cluster 1: Postgres Caching Blast Radius
    sources.append({
        "id": "SRC-BENCHMARK-2024",
        "title": "Q1 2024 Cache Latency & JSONB Benchmark RFC",
        "type": "RFC Document",
        "url": "https://wiki.internal/rfc/2024-q1-postgres-cache",
        "created_at": "2024-01-15T10:00:00Z"
    })
    
    assumptions.append({
        "id": "ASM-LATENCY-Q1",
        "text": "Postgres JSONB latency remains sub-10ms for 95% of reads under 5k QPS with unlogged tables",
        "valid": True,
        "category": "Performance",
        "validated_at": "2024-01-15T10:00:00Z"
    })
    
    assumptions.append({
        "id": "ASM-REDIS-COST",
        "text": "Eliminating dedicated Redis cluster saves $8,400 monthly in cloud infrastructure overhead",
        "valid": True,
        "category": "Cost",
        "validated_at": "2024-01-15T10:00:00Z"
    })
    
    decisions.append({
        "id": "DEC-POSTGRES-CACHE",
        "title": "Consolidate App Caching into PostgreSQL Unlogged Tables",
        "rationale": "Avoid operational overhead of running multi-region Redis cluster given Postgres meets latency SLAs",
        "status": "active",
        "decided_at": "2024-01-20T14:30:00Z",
        "domain": "Database",
        "confidence": 0.92,
        "person_id": "PER-ALEX",
        "source_id": "SRC-BENCHMARK-2024",
        "relies_on": ["ASM-LATENCY-Q1", "ASM-REDIS-COST"],
        "depends_on": []
    })

    decisions.append({
        "id": "DEC-FEED-SERVICE",
        "title": "Feed Service reads user timeline cache from PostgreSQL",
        "rationale": "High-throughput timeline cache leverages unified PostgreSQL connection pool",
        "status": "active",
        "decided_at": "2024-02-01T09:15:00Z",
        "domain": "Architecture",
        "confidence": 0.88,
        "person_id": "PER-ELENA",
        "source_id": "SRC-BENCHMARK-2024",
        "relies_on": ["ASM-LATENCY-Q1"],
        "depends_on": ["DEC-POSTGRES-CACHE"]
    })

    decisions.append({
        "id": "DEC-NOTIF-CACHE",
        "title": "Notification Service token invalidation lookup via Postgres unlogged cache",
        "rationale": "Ensures instant auth token revocation check within main DB network boundary",
        "status": "active",
        "decided_at": "2024-02-10T11:00:00Z",
        "domain": "Security",
        "confidence": 0.85,
        "person_id": "PER-MARCUS",
        "source_id": "SRC-BENCHMARK-2024",
        "relies_on": ["ASM-LATENCY-Q1"],
        "depends_on": ["DEC-POSTGRES-CACHE"]
    })

    decisions.append({
        "id": "DEC-SEARCH-HINTS",
        "title": "Search Autocomplete Service stores query hints in Postgres cache",
        "rationale": "Shared cached query suggestions without extra Redis memory footprint",
        "status": "active",
        "decided_at": "2024-02-25T16:20:00Z",
        "domain": "API",
        "confidence": 0.81,
        "person_id": "PER-ZOE",
        "source_id": "SRC-BENCHMARK-2024",
        "relies_on": ["ASM-LATENCY-Q1"],
        "depends_on": ["DEC-POSTGRES-CACHE"]
    })

    # 2. Planted Cluster 2: Stripe Interchange Fee Blast Radius
    sources.append({
        "id": "SRC-STRIPE-CONTRACT",
        "title": "Stripe Custom Enterprise Agreement 2024",
        "type": "Contract",
        "url": "https://vault.internal/contracts/stripe-2024-v3.pdf",
        "created_at": "2024-01-10T08:00:00Z"
    })

    assumptions.append({
        "id": "ASM-STRIPE-FEE",
        "text": "European Interchange++ fee fixed under 1.4% with cross-border waiver through 2026",
        "valid": True,
        "category": "Billing",
        "validated_at": "2024-01-10T08:00:00Z"
    })

    decisions.append({
        "id": "DEC-STRIPE-PRIMARY",
        "title": "Migrate Global Subscription Billing to Stripe Elements & Custom Payouts",
        "rationale": "Single gateway simplifies accounting and offers favorable negotiated EU processing rates",
        "status": "active",
        "decided_at": "2024-01-18T10:00:00Z",
        "domain": "Billing",
        "confidence": 0.95,
        "person_id": "PER-SARAH",
        "source_id": "SRC-STRIPE-CONTRACT",
        "relies_on": ["ASM-STRIPE-FEE"],
        "depends_on": []
    })

    decisions.append({
        "id": "DEC-EU-BILLING",
        "title": "Zero-Surcharge Euro Pricing for European B2B Customers",
        "rationale": "Interchange waiver allows passing direct 0% conversion margin to European customers",
        "status": "active",
        "decided_at": "2024-02-12T13:40:00Z",
        "domain": "Billing",
        "confidence": 0.90,
        "person_id": "PER-MAYA",
        "source_id": "SRC-STRIPE-CONTRACT",
        "relies_on": ["ASM-STRIPE-FEE"],
        "depends_on": ["DEC-STRIPE-PRIMARY"]
    })

    decisions.append({
        "id": "DEC-MICRO-SUBSCRIPTION",
        "title": "Launch €3.99/mo Developer Starter Tier without minimum transaction fees",
        "rationale": "Unit economics hold only if processing fee stays strictly under 1.5%",
        "status": "active",
        "decided_at": "2024-03-05T15:10:00Z",
        "domain": "Billing",
        "confidence": 0.86,
        "person_id": "PER-NINA",
        "source_id": "SRC-STRIPE-CONTRACT",
        "relies_on": ["ASM-STRIPE-FEE"],
        "depends_on": ["DEC-STRIPE-PRIMARY"]
    })

    # 3. Generate 55+ realistic engineering decisions to reach 60+ nodes
    sample_topics = [
        ("Kafka for Event Bus", "High throughput event stream for async services", "Infrastructure"),
        ("Kubernetes EKS Migration", "Container orchestration to standardize deployments", "Infrastructure"),
        ("Adopt gRPC for Internal Services", "Binary serialization reduces microservice RPC latency", "API"),
        ("OpenTelemetry Tracing", "Distributed trace collection across all HTTP & gRPC gateways", "Architecture"),
        ("Single Sign-On with Okta OIDC", "Centralize corporate identity and MFA policies", "Security"),
        ("Tailscale Mesh VPN for Staging", "Zero-trust network access replacing OpenVPN", "Security"),
        ("ClickHouse for Product Analytics", "Columnar store for real-time telemetry aggregation", "Analytics"),
        ("S3 Intelligent Tiering for Logs", "Auto-transition raw logs older than 30 days to Glacier", "Cost"),
        ("React with Vite & Tailwind", "Standardize developer frontend tooling and fast HMR", "Frontend"),
        ("GraphQL Gateway for Mobile Clients", "Minimize over-fetching on high latency mobile networks", "Frontend"),
        ("Adopt Rust for Image Processing Worker", "Eliminate garbage collection pauses during media transcode", "Architecture"),
        ("Flyway for Database Migrations", "Deterministic schema migration applied at pod startup", "Database"),
        ("Vector Search with pgvector", "Embeddings stored directly alongside relational entity rows", "Database"),
        ("Prometheus Alertmanager PagerDuty", "Route critical tier-1 outages directly to on-call phone", "Infrastructure"),
        ("Branch Previews with Vercel", "Ephemeral PR preview environments for designer review", "Frontend"),
        ("Snowflake Data Warehouse", "Central analytical warehouse for executive reporting", "Analytics"),
        ("mTLS Between Microservices", "Mutual TLS enforced by Linkerd service mesh", "Security"),
        ("GitHub Actions CI Standardization", "Migrate all legacy Jenkins pipelines to GHA reusable workflows", "Infrastructure"),
        ("ArgoCD GitOps Deployment", "Declarative Kubernetes state synced from git repo", "Infrastructure"),
        ("Datadog APM Deprecation", "Shift to self-hosted Grafana Tempo to curb APM cost overrun", "Cost"),
    ]

    for i in range(1, 55):
        topic_title, topic_rat, topic_domain = random.choice(sample_topics)
        d_id = f"DEC-GEN-{i:03d}"
        s_id = f"SRC-GEN-{i:03d}"
        a_id = f"ASM-GEN-{i:03d}"
        person = random.choice(PEOPLE)
        
        sources.append({
            "id": s_id,
            "title": f"RFC {100 + i}: {topic_title} Architecture Spec",
            "type": "Architecture RFC",
            "url": f"https://wiki.internal/rfc/{100 + i}",
            "created_at": fake.iso8601()
        })
        
        assumptions.append({
            "id": a_id,
            "text": f"Assumption: {topic_title} satisfies team SLA with less than 5% maintenance overhead",
            "valid": random.random() > 0.1,
            "category": "Engineering SLA",
            "validated_at": fake.iso8601()
        })
        
        # Link to a previous decision occasionally to create graph depth
        dep_ids = []
        if decisions and random.random() > 0.6:
            dep_ids.append(random.choice(decisions)["id"])
            
        decisions.append({
            "id": d_id,
            "title": f"{topic_title} (Phase {random.randint(1,3)})",
            "rationale": topic_rat,
            "status": "active" if random.random() > 0.15 else "superseded",
            "decided_at": fake.iso8601(),
            "domain": topic_domain,
            "confidence": round(random.uniform(0.75, 0.98), 2),
            "person_id": person["id"],
            "source_id": s_id,
            "relies_on": [a_id],
            "depends_on": dep_ids
        })

    data = {
        "teams": TEAMS,
        "people": PEOPLE,
        "sources": sources,
        "assumptions": assumptions,
        "decisions": decisions,
        "tickets": tickets,
        "events": events
    }
    
    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / "seed_data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    return out_path, len(decisions), len(assumptions), len(people := PEOPLE)

if __name__ == "__main__":
    out_path, d_count, a_count, p_count = generate_seed_dataset()
    print(f"Generated seed dataset at {out_path}: {d_count} decisions, {a_count} assumptions, {p_count} people.")
