# last30days Skill Specification

## Overview

`last30days` is a Claude Code skill that researches a given topic across Reddit, X (Twitter), Raindrop.io bookmarks, and the web using multiple APIs. It enforces a strict 30-day recency window, popularity-aware ranking, and produces actionable outputs including best practices, a prompt pack, and a reusable context snippet.

The skill operates in multiple modes depending on available API keys:
- **reddit-only** (OpenAI key): Reddit threads only
- **x-only** (xAI key): X/Twitter posts only
- **raindrops-only** (Raindrop key): Personal/public bookmarks only
- **both** (OpenAI + xAI keys): Reddit + X cross-validation
- **all** (all keys): Reddit + X + Raindrops + Web for comprehensive coverage

It uses automatic model selection to stay current with the latest models from both providers, with optional pinning for stability.

## Architecture

The orchestrator (`last30days.py`) coordinates discovery, enrichment, normalization, scoring, deduplication, and rendering. Each concern is isolated in `scripts/lib/`:

- **env.py**: Load and validate API keys from `~/.config/last30days/.env`
- **dates.py**: Date range calculation and confidence scoring
- **cache.py**: 24-hour TTL caching keyed by topic + date range
- **http.py**: stdlib-only HTTP client with retry logic
- **models.py**: Auto-selection of OpenAI/xAI models with 7-day caching
- **openai_reddit.py**: OpenAI Responses API + web_search for Reddit
- **xai_x.py**: xAI Responses API + x_search for X
- **raindrops_search.py**: Raindrop.io REST API for personal/public bookmarks
- **reddit_enrich.py**: Fetch Reddit thread JSON for real engagement metrics
- **normalize.py**: Convert raw API responses to canonical schema
- **score.py**: Compute popularity-aware scores (relevance + recency + engagement/importance)
- **dedupe.py**: Near-duplicate detection via text similarity
- **render.py**: Generate markdown and JSON outputs
- **schema.py**: Type definitions and validation

## Embedding in Other Skills

Other skills can import the research context in several ways:

### Inline Context Injection
```markdown
## Recent Research Context
!python3 ~/.claude/skills/last30days/scripts/last30days.py "your topic" --emit=context
```

### Read from File
```markdown
## Research Context
!cat ~/.local/share/last30days/out/last30days.context.md
```

### Get Path for Dynamic Loading
```bash
CONTEXT_PATH=$(python3 ~/.claude/skills/last30days/scripts/last30days.py "topic" --emit=path)
cat "$CONTEXT_PATH"
```

### JSON for Programmatic Use
```bash
python3 ~/.claude/skills/last30days/scripts/last30days.py "topic" --emit=json > research.json
```

## CLI Reference

```
python3 ~/.claude/skills/last30days/scripts/last30days.py <topic> [options]

Options:
  --refresh           Bypass cache and fetch fresh data
  --mock              Use fixtures instead of real API calls
  --emit=MODE         Output mode: compact|json|md|context|path (default: compact)
  --sources=MODE      Source selection: auto|reddit|x|both|raindrops|all (default: auto)
  --quick             Faster research with fewer sources (8-15 items)
  --deep              Comprehensive research with more sources (50-100 items)
```

### Raindrop.io Setup

To use Raindrops (personal bookmarks) as a source:

1. Get your API token from https://app.raindrop.io/settings/integrations
2. Add to `~/.config/last30days/.env`:
   ```
   RAINDROP_API_KEY=your_token_here
   RAINDROP_COLLECTION_ID=0  # 0 = all bookmarks, or specific collection ID
   ```
3. Run with `--sources=raindrops` or `--sources=all`

## Output Files

All outputs are written to `~/.local/share/last30days/out/`:

- `report.md` - Human-readable full report
- `report.json` - Normalized data with scores
- `last30days.context.md` - Compact reusable snippet for other skills
- `raw_openai.json` - Raw OpenAI API response
- `raw_xai.json` - Raw xAI API response
- `raw_reddit_threads_enriched.json` - Enriched Reddit thread data
