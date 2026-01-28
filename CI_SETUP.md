# CI/CD Setup Guide

## GitHub Actions End-to-End Testing

This repository includes automated end-to-end testing for PRs that validates the Raindrops integration (and other search sources if configured).

### Overview

The PR E2E test workflow (`.github/workflows/pr-e2e-test.yml`) runs on every pull request and tests:

1. **Raindrops search** - If `RAINDROP_API_KEY` is configured
2. **All sources** - If all API keys are configured (Reddit + X + Raindrops)
3. **Fallback mode** - Web-only search when no API keys are available
4. **Output formats** - JSON and compact emit modes

### Setting Up API Keys (Repository Secrets)

To enable full end-to-end testing, configure repository secrets:

#### Step 1: Access Repository Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

#### Step 2: Add Required Secrets

| Secret Name | Required? | Description | Where to Get It |
|-------------|-----------|-------------|-----------------|
| `RAINDROP_API_KEY` | **Recommended** | Raindrop.io API token for bookmark search | [Get Token](https://app.raindrop.io/settings/integrations) |
| `OPENAI_API_KEY` | Optional | OpenAI API key for Reddit search | [Get Key](https://platform.openai.com/api-keys) |
| `XAI_API_KEY` | Optional | xAI API key for X/Twitter search | [Get Key](https://console.x.ai/) |

#### Step 3: Getting Your Raindrop.io API Token

1. Visit https://app.raindrop.io/settings/integrations
2. Click **"Create new app"** or use an existing app
3. Click **"Create test token"** for quick access
4. Copy the generated token
5. Add it as `RAINDROP_API_KEY` in GitHub Secrets

**Note:** Test tokens have access to your personal bookmarks only. For production use or public collection access, implement full OAuth flow.

### What Gets Tested

#### 1. Raindrops Search Test
```bash
python3 scripts/last30days.py "AI tools" --sources=raindrops --quick --emit=json
```
Validates:
- API connection works
- JSON output is valid
- Expected fields are present
- Raindrops data structure is correct

#### 2. All Sources Test (if all keys available)
```bash
python3 scripts/last30days.py "Python libraries" --sources=all --quick --emit=json
```
Validates:
- Reddit, X, and Raindrops all work together
- Parallel execution succeeds
- Results are properly merged

#### 3. Fallback Mode Test
```bash
python3 scripts/last30days.py "test topic" --sources=auto --emit=json
```
Validates:
- Web-only mode works without API keys
- Graceful degradation

#### 4. Output Format Tests
- JSON emit mode produces valid JSON
- Compact emit mode produces markdown

### Test Results

Test results are:
- **Summarized** in the GitHub Actions summary
- **Artifacts** uploaded for 7 days (JSON outputs)
- **Status checks** reported to the PR

### Workflow Triggers

The E2E test workflow runs:
- **Automatically** on every pull request to main/master
- **Manually** via workflow_dispatch (Actions tab → "Run workflow")

### Skipped Tests

Tests are automatically skipped if the required API keys are not configured:
- ⚠️ No `RAINDROP_API_KEY` → Raindrops test skipped
- ⚠️ No `OPENAI_API_KEY` → Reddit test skipped
- ⚠️ No `XAI_API_KEY` → X test skipped
- ℹ️ No keys at all → Falls back to web-only mode test

### Security Considerations

- **Secrets are encrypted** - GitHub encrypts secrets at rest and in transit
- **Not exposed in logs** - Secret values are masked in workflow logs
- **PR restrictions** - Secrets from forks don't have access to repository secrets (security best practice)
- **Rate limits** - Be mindful of API rate limits; use `--quick` flag in tests

### Troubleshooting

#### Test fails with "API error"
- Verify the API key is correctly copied (no extra spaces)
- Check the API key hasn't expired
- Ensure you have bookmarks in your Raindrop.io account

#### Test skipped
- Check that the secret name matches exactly (case-sensitive)
- Verify the secret is set at the repository level (not environment level)

#### Invalid JSON error
- This might indicate a breaking change in the API response format
- Check the uploaded artifacts to inspect the raw output

### Local Testing

To test the workflow locally before pushing:

```bash
# Set up environment
mkdir -p ~/.config/last30days
echo "RAINDROP_API_KEY=your_token" > ~/.config/last30days/.env

# Run the same tests as CI
python3 scripts/last30days.py "AI tools" --sources=raindrops --quick --emit=json

# Validate JSON
python3 -m json.tool output.json
```

### Contributing

When adding new features:
1. Update the E2E test workflow to cover new functionality
2. Document any new required secrets in this guide
3. Ensure tests pass both with and without optional API keys
