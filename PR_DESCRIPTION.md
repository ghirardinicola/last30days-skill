# Add Raindrop.io Integration for Personal/Public Bookmark Search

## 🎯 Overview

This PR adds comprehensive Raindrop.io support to the last30days-skill, enabling users to search their personal bookmarks and public collections alongside Reddit, X, and web sources.

## ✨ Features

### 1. **Full Raindrop.io API Integration**
- Direct REST API integration (no LLM required - faster & cheaper!)
- Search personal bookmarks with exact timestamps
- Support for public collection searches
- Date filtering using `created:>YYYY-MM-DD` syntax
- Collection-based filtering (all bookmarks, unsorted, or specific collections)

### 2. **Parallel Execution**
- Runs in parallel with Reddit and X searches (3 workers)
- No performance impact on existing functionality
- Graceful error handling per source

### 3. **Rich Data Model**
- Tags, personal notes, and favorites
- Content type detection (link/article/video/document/image/audio)
- Exact bookmark creation timestamps (high date confidence)
- Collection organization preserved

### 4. **Smart Scoring**
- **60% Relevance** - Search match quality
- **30% Recency** - Bookmark creation date
- **10% Importance** - Favorite flag bonus
- Source priority: Reddit > X > Raindrops > WebSearch

### 5. **Beautiful Rendering**
- Tags displayed inline: `#tag1, #tag2`
- Favorite indicators: ❤️
- Content type badges: `[article]`, `[video]`
- Personal notes shown as: 📝 Note excerpt...

## 📦 Changes

### New Files
- `scripts/lib/raindrops_search.py` - Raindrop.io API client (208 lines)
- `.github/workflows/pr-e2e-test.yml` - E2E testing workflow
- `.github/pull_request_template.md` - PR template with setup instructions
- `CI_SETUP.md` - Comprehensive CI/CD setup guide

### Modified Files
- `scripts/lib/schema.py` - Added `RaindropItem` dataclass
- `scripts/lib/normalize.py` - Added Raindrop normalization
- `scripts/lib/score.py` - Added importance-based scoring
- `scripts/lib/render.py` - Added rich Raindrop rendering
- `scripts/lib/env.py` - Added Raindrop config handling
- `scripts/lib/ui.py` - Updated progress display
- `scripts/last30days.py` - Integrated parallel execution
- `SKILL.md` & `SPEC.md` - Updated documentation

## 🚀 Usage

### Basic Usage
```bash
# Search only your Raindrops
./scripts/last30days.py "AI tools" --sources=raindrops

# Search everything (Reddit + X + Raindrops + Web)
./scripts/last30days.py "Claude Code" --sources=all

# Auto mode (uses available API keys)
./scripts/last30days.py "design systems" --sources=auto
```

### Configuration

Add to `~/.config/last30days/.env`:
```bash
RAINDROP_API_KEY=your_token_here
RAINDROP_COLLECTION_ID=0  # 0 = all bookmarks (default)
```

**Get API Token:** https://app.raindrop.io/settings/integrations

### Search Specific Collections
```bash
# Search a specific collection
RAINDROP_COLLECTION_ID=12345 ./scripts/last30days.py "photography"

# Search unsorted bookmarks only
RAINDROP_COLLECTION_ID=-1 ./scripts/last30days.py "articles"
```

## 🧪 Testing

### Manual Testing
```bash
# Test with mock data
./scripts/last30days.py "test" --sources=raindrops --mock

# Test with real API
./scripts/last30days.py "AI tools" --sources=raindrops --quick

# Test JSON output
./scripts/last30days.py "topic" --sources=raindrops --emit=json | python3 -m json.tool
```

### Automated E2E Testing

This PR includes a GitHub Actions workflow that automatically tests the Raindrops integration on every PR.

## ⚙️ GitHub Actions Setup (For Repository Maintainers)

To enable automated end-to-end testing in PRs, configure repository secrets:

### Step 1: Access Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**

### Step 2: Add Secrets

| Secret Name | Required? | Where to Get It |
|-------------|-----------|-----------------|
| `RAINDROP_API_KEY` | **Recommended** | https://app.raindrop.io/settings/integrations |
| `OPENAI_API_KEY` | Optional | https://platform.openai.com/api-keys |
| `XAI_API_KEY` | Optional | https://console.x.ai/ |

### Step 3: Get Raindrop.io API Token

1. Visit https://app.raindrop.io/settings/integrations
2. Click **"Create new app"** or use existing
3. Click **"Create test token"**
4. Copy the token
5. Add as `RAINDROP_API_KEY` in GitHub Secrets

**Note:** Test tokens work for personal bookmarks only. The workflow will automatically skip tests if keys are not configured.

### What Gets Tested

The E2E workflow tests:
- ✅ Raindrops search with real API calls
- ✅ All sources together (Reddit + X + Raindrops)
- ✅ Fallback to web-only mode without keys
- ✅ JSON and compact output formats
- ✅ Proper error handling

### Test Results

- **Summary** shown in PR checks
- **Artifacts** uploaded (7-day retention)
- **Graceful skipping** when keys are missing

## 📊 Example Output

### Compact Format
```markdown
### Raindrop Bookmarks

**RD1234** [RAINDROP] (score:78) github.com (2026-01-15) ❤️ [article]
  Getting Started with Claude Code
  https://github.com/anthropics/claude-code
  📝 Note: Great tutorial for beginners...
  Comprehensive guide to using Claude Code for software development
  [tags: claude, ai, development]

**RD1235** [RAINDROP] (score:72) anthropic.com (2026-01-14) [article]
  Claude API Documentation
  https://docs.anthropic.com/claude/docs
  Official documentation for the Claude API with examples
  [tags: api, documentation]
```

### JSON Format
```json
{
  "raindrops": [
    {
      "id": "RD1234",
      "title": "Getting Started with Claude Code",
      "link": "https://github.com/anthropics/claude-code",
      "domain": "github.com",
      "excerpt": "Comprehensive guide...",
      "note": "Great tutorial for beginners",
      "tags": ["claude", "ai", "development"],
      "type": "article",
      "created": "2026-01-15",
      "date_confidence": "high",
      "important": true,
      "score": 78,
      "subs": {
        "relevance": 85,
        "recency": 95,
        "engagement": 100
      }
    }
  ]
}
```

## 🔒 Security

- Secrets are encrypted by GitHub
- Secret values masked in logs
- PR forks don't have access to repository secrets
- Uses `--quick` flag in tests to minimize API usage

## 🎁 Benefits

- **Personal Knowledge Base** - Search your curated bookmarks
- **Quality over Quantity** - Pre-vetted content
- **Rich Context** - Tags, notes, organizational structure
- **Fast & Cheap** - Direct API, no LLM costs
- **Privacy-Friendly** - Search private bookmarks securely

## 📚 Documentation

See [`CI_SETUP.md`](./CI_SETUP.md) for detailed CI/CD setup instructions.

## ✅ Testing Checklist

- [x] Tested locally with mock data
- [x] Tested with real Raindrop.io API
- [x] All existing tests pass
- [x] Added E2E test workflow
- [x] Documentation updated
- [x] PR template created

## 🚢 Ready for Review

This PR is ready for review and includes:
- ✅ Complete Raindrop.io integration
- ✅ Automated E2E testing
- ✅ Comprehensive documentation
- ✅ Setup instructions for maintainers

---

**Note:** The E2E tests will run automatically when this PR is opened. If no API keys are configured yet, the workflow will gracefully skip Raindrop tests and fall back to web-only mode testing.
