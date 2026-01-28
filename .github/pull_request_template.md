## Description

<!-- Describe your changes here -->

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

<!-- Describe how you tested your changes -->

- [ ] Tested locally with mock data
- [ ] Tested with real API keys
- [ ] All existing tests pass
- [ ] Added new tests for new functionality

## API Keys Required

<!-- Check which API keys are needed to test this PR -->

- [ ] None (works without API keys)
- [ ] `RAINDROP_API_KEY` - For Raindrop.io bookmark search
- [ ] `OPENAI_API_KEY` - For Reddit search via OpenAI
- [ ] `XAI_API_KEY` - For X/Twitter search via xAI

## GitHub Actions Setup (for maintainers)

To enable end-to-end testing in PRs, add these repository secrets:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets:

| Secret Name | Description | Where to Get It |
|-------------|-------------|-----------------|
| `RAINDROP_API_KEY` | Raindrop.io API token | https://app.raindrop.io/settings/integrations |
| `OPENAI_API_KEY` | OpenAI API key (optional) | https://platform.openai.com/api-keys |
| `XAI_API_KEY` | xAI API key (optional) | https://console.x.ai/ |

**Note:** These secrets are optional. The workflow will skip tests for sources without configured keys and fall back to web-only mode if no keys are available.

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
