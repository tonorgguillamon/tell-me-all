# Tell Me All

An intelligent, real-time floating dashboard where users build their own view of the world.

Think of it as a personal mission-control panel: cards for topics you care about, live updates from multiple sources, and AI agents that summarize noise into action.

## Why This Project Exists

Most information tools force users to jump between apps, tabs, newsletters, and notifications.

Tell Me All brings everything into one place:

- news and open web updates
- APIs and external tools
- emails and calendar context
- AI summaries and key points
- proactive alerts when something important happens

The result is one dashboard, tailored to each person, always up to date.

## Core Product Vision

Users can create a floating dashboard made of configurable cards.

Each card can:

- monitor a topic (for example football, finance, healthcare)
- apply keyword or semantic filters
- pull from multiple sources (newspapers, APIs, tools)
- show condensed AI summaries instead of raw feeds
- raise flags and send notifications when important conditions are met

### Example Use Cases

1. Football scout view
	Track all football news but only highlight updates related to injuries.

2. Finance focus view
	Follow financial updates, restricted to healthcare-related companies and policy changes.

3. Inbox + calendar intelligence
	Collect important emails, link relevant context to calendar events, and surface action items.

## What Makes It Different

- User-defined dashboard, not a fixed feed
- Multi-source ingestion in one product
- Agent-based summarization and prioritization
- Real-time style updates via events or scheduled polling
- Active monitoring with alerts, so users do not need to watch constantly

## Architecture Overview

Tell Me All combines event-driven updates with scheduled collection:

- Webhooks for fast, push-based updates when available
- Agent polling every few hours when sources do not support webhooks
- Queue-driven processing for reliability and scale
- Redis-backed caching and short-lived state
- PostgreSQL as the source of truth

### High-Level Flow

```text
Sources (news/APIs/tools/email/calendar)
  -> Ingestion (webhooks + polling agents)
  -> Queue (AWS SQS)
  -> Processing + Summarization Agents (LLM providers)
  -> Rules/Flags Engine
  -> Storage (PostgreSQL + Redis)
  -> Dashboard Cards (HTML/JS UI)
  -> Notifications (AWS SNS)
```

## Tech Stack

- Backend: Python 3.12+, FastAPI
- Database: PostgreSQL
- Cache/Realtime support: Redis
- Messaging: AWS SQS
- Notifications: AWS SNS
- Frontend: HTML + JavaScript
- LLM Providers: OpenAI, Claude API, GitHub Models

## Project Goals

- Build a modular card system for personalized dashboards
- Add multi-provider AI summarization pipelines
- Support keyword, semantic, and rule-based filtering
- Deliver near real-time updates with fault-tolerant ingestion
- Trigger actionable notifications through flags and thresholds

## Application Experience

Tell Me All is designed as a living workspace, not a static report.

Users shape their own cockpit with cards that can be moved, resized, grouped, and pinned by priority. A card can represent a topic, a workflow, or a connected tool. Instead of showing raw streams, cards focus on:

- what changed
- why it matters
- what needs attention now

### Personalization Model

Each user can define:

- domains of interest (sports, finance, healthcare, policy, etc.)
- strict keywords (for example "football players INJURED")
- semantic constraints (for example finance only when linked to healthcare)
- urgency thresholds and notification preferences
- data source trust level and ranking preferences

This makes the dashboard highly personal while keeping the signal quality high.

### Agent Behavior

Agents are not only summarizers; they are continuous monitors.

They can:

- ingest updates from different connectors
- deduplicate repeated information across sources
- extract key points with references
- classify items by urgency and relevance
- trigger flags when predefined patterns are detected

### Alerts and Flags

A core value of the app is reducing manual monitoring time.

When a condition is met, agents can raise a flag and send a notification. Examples:

- "Injury mention detected for a tracked player"
- "Healthcare regulation update impacting watched financial entities"
- "Email requiring action before next calendar event"

Users get proactive insights instead of constantly checking feeds.

## Product Principles

- One dashboard instead of many fragmented tools
- Actionable summaries over information overload
- Configurable intelligence controlled by the user
- Real-time where possible, scheduled where needed
- Human-in-the-loop decision support, not autopilot

## Current Stack

- Python 3.12+
- FastAPI
- PostgreSQL
- Redis
- AWS SNS + SQS
- HTML + JavaScript UI
- OpenAI, Claude API, or GitHub Models