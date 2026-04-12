<div align="center">

# Tell Me All

**Your personal mission control. One dashboard. Every source. Zero noise.**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io)
[![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)

</div>

---

## The Problem

Most information tools force you to jump between apps, tabs, newsletters, and notifications. You're constantly checking, never monitoring — and still missing what matters.

**Tell Me All changes that.**

---

## What It Does

Tell Me All is an intelligent, real-time floating dashboard where you define exactly what you want to watch — and AI agents handle the rest.

Build your personal cockpit with configurable cards. Each card is a live window into a topic, workflow, or connected tool. Instead of raw feeds, you see **what changed**, **why it matters**, and **what needs your attention now**.

```
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│  🏈 Football Scout   │  │  📈 Finance Focus     │  │  📬 Inbox + Calendar │
│                      │  │                       │  │                      │
│  ⚠ INJURY ALERT     │  │  3 healthcare policy  │  │  2 action items due  │
│  M. Salah – hamstr.  │  │  updates this morning │  │  before 2pm meeting  │
│                      │  │                       │  │                      │
│  12 updates filtered │  │  Filtered: HLTH, CVS, │  │  Linked: Q3 review   │
│  down to 1 flag      │  │  UNH + regulation     │  │  draft + budget call │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

---

## Key Features

**Configurable Cards**
Each card monitors a topic of your choice with keyword and semantic filters, pulls from multiple sources simultaneously, and delivers AI-condensed summaries instead of raw noise.

**Multi-Source Ingestion**
Bring in news and open web updates, external APIs, emails, calendar context, and any connected tool — all in one place.

**Agent-Based Intelligence**
Agents continuously ingest, deduplicate, classify, and summarize updates across sources. They don't just report — they prioritize.

**Proactive Alerts**
Define conditions, get notified when they're met. Stop checking. Start knowing.

**Deeply Personal**
Every user controls their domains of interest, keyword rules, semantic constraints, urgency thresholds, and source trust rankings.

---

## Example Use Cases

| Dashboard | What It Watches | What Gets Flagged |
|---|---|---|
| 🏈 **Football Scout** | All football news | Injury mentions for tracked players |
| 📈 **Finance Focus** | Financial updates | Healthcare-linked companies & policy changes |
| 📬 **Inbox Intelligence** | Email + calendar | Action items before upcoming events |

---

## How It Works

Tell Me All combines event-driven updates with scheduled collection:

- **Webhooks** — push-based updates for sources that support them
- **Agent polling** — scheduled collection every few hours for the rest
- **Queue-driven processing** — reliable, fault-tolerant ingestion at scale
- **Redis caching** — fast reads and short-lived state
- **PostgreSQL** — source of truth for all persistent data

### Agent Pipeline

```
Source Update
     │
     ▼
  Ingestion Layer (webhook / poll)
     │
     ▼
  SQS Queue → Deduplication → Classification → Summarization
                                                     │
                                                     ▼
                                              Flag Evaluation
                                                     │
                                          ┌──────────┴──────────┐
                                          ▼                     ▼
                                     Dashboard Card        SNS Notification
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12+, FastAPI |
| Database | PostgreSQL |
| Cache & Realtime | Redis |
| Messaging | AWS SQS |
| Notifications | AWS SNS |
| Frontend | HTML + JavaScript |
| AI Providers | OpenAI, Claude API, GitHub Models |

---

## Project Roadmap

- [x] Architecture design and documentation
- [ ] Modular card system for personalized dashboards
- [ ] Multi-provider AI summarization pipeline
- [ ] Keyword, semantic, and rule-based filtering
- [ ] Near real-time updates with fault-tolerant ingestion
- [ ] Actionable alert and notification system
- [ ] Email and calendar connector
- [ ] User-defined urgency thresholds and source ranking

---

## Getting Started

> Setup instructions coming soon. Star the repo to follow progress.

---

## Contributing

Contributions, ideas, and feedback are welcome. Open an issue to start a conversation.

---

<div align="center">

Built to reduce the noise. Designed to surface what matters.

</div>