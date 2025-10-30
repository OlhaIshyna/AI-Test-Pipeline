# Configuration Guide

This guide explains how to configure the AI Test Pipeline for your Azure OpenAI environment.

## Azure OpenAI Setup

### 1. Azure OpenAI Endpoint

The endpoint is configured in `ai-tests/ai-test-config.yaml`:

```yaml
azure_openai:
  endpoint: https://olhaopenai.openai.azure.com/
  api_version: "2024-02-15-preview"
  deployment_name: gpt-4
```

**Configuration Parameters:**

- `endpoint`: Your Azure OpenAI resource endpoint URL
- `api_version`: The API version to use (recommended: `2024-02-15-preview`)
- `deployment_name`: The name of your deployed model (e.g., `gpt-4`, `gpt-35-turbo`)

### 2. API Key Configuration

#### Local Development

Set the environment variable:

```bash
export AZURE_OPENAI_API_KEY='your-api-key-here'
```

Or create a `.env` file (not committed to git):

```bash
AZURE_OPENAI_API_KEY=your-api-key-here
```

#### GitHub Actions (CI/CD)

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `AZURE_OPENAI_API_KEY`
5. Value: Your Azure OpenAI API key
6. Click **Add secret**

### 3. Finding Your Configuration Values

#### Finding Your Endpoint

1. Log in to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Go to **Keys and Endpoint**
4. Copy the **Endpoint** URL (e.g., `https://your-resource.openai.azure.com/`)

#### Finding Your Deployment Name

1. In Azure Portal, go to your Azure OpenAI resource
2. Navigate to **Model deployments** or use **Azure OpenAI Studio**
3. Note the deployment name (e.g., `gpt-4`, `my-gpt-4-deployment`)

#### Getting Your API Key

1. In Azure Portal, go to your Azure OpenAI resource
2. Navigate to **Keys and Endpoint**
3. Copy either **KEY 1** or **KEY 2**

## Test Configuration

### Adding New Test Cases

Edit `ai-tests/ai-test-config.yaml`:

```yaml
test_cases:
  - id: test_004
    name: New Location Test
    input:
      location: "Berlin, Germany"
    expected_output:
      contains:
        - "German"
      validation_type: primary_language
```

### Validation Criteria

Configure validation rules in the YAML:

```yaml
validation:
  criteria:
    - check_primary_language: true
    - response_length_min: 10        # Minimum response length
    - response_length_max: 500       # Maximum response length
    - response_time_max_seconds: 30  # Maximum response time
```

## Prompt Configuration

### Customizing the Prompt

Edit `ai-tests/prompts/language-recommendation.txt`:

```
You are a language recommendation assistant...

Location: {location}

Provide recommendations...
```

**Variables:**
- `{location}`: Replaced with the test case location

### Multiple Prompts

To use different prompts:

1. Create new prompt file: `ai-tests/prompts/custom-prompt.txt`
2. Update config: `prompt.template_file: prompts/custom-prompt.txt`

## Dataset Configuration

### Dataset Structure

Edit `ai-tests/datasets/language-dataset.json`:

```json
{
  "test_cases": [
    {
      "id": "test_001",
      "location": "Your Location",
      "expected_primary_language": "Expected Language",
      "expected_secondary_languages": ["Secondary", "Languages"],
      "description": "Description of this test case"
    }
  ],
  "metadata": {
    "version": "1.0",
    "description": "Dataset description",
    "date_created": "2025-10-30"
  }
}
```

## CI/CD Pipeline Configuration

### Workflow Triggers

Edit `.github/workflows/ai-tests.yml`:

```yaml
on:
  push:
    branches: [ main, develop ]  # Add your branches
  pull_request:
    branches: [ main ]
  workflow_dispatch:             # Manual trigger
  schedule:
    - cron: '0 0 * * *'          # Daily at midnight (optional)
```

### Python Version

Update the Python version:

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Change version here
```

### Workflow Permissions

If you need specific permissions:

```yaml
permissions:
  contents: read
  issues: write      # If you want to create issues on failure
  checks: write      # If you want to add check annotations
```

## Advanced Configuration

### Custom Test Runner Options

Edit `run_tests.py` to add custom options:

```python
class AITestRunner:
    def __init__(self, config_path: str, custom_option: bool = False):
        # Add custom initialization
        pass
```

### Environment-Specific Configs

Create multiple config files:

- `ai-test-config.yaml` (default)
- `ai-test-config.dev.yaml` (development)
- `ai-test-config.prod.yaml` (production)

Load with:

```bash
python run_tests.py --config ai-test-config.dev.yaml
```

### Timeout Configuration

For longer-running tests, adjust timeouts:

```yaml
validation:
  criteria:
    - response_time_max_seconds: 60  # Increase timeout
```

## Troubleshooting Configuration

### Issue: "Deployment not found"

**Solution:**
- Verify deployment name in Azure Portal
- Update `deployment_name` in `ai-test-config.yaml`

### Issue: "Authentication failed"

**Solution:**
- Check API key is correct
- Verify key is not expired
- Ensure key has proper permissions

### Issue: "Endpoint not accessible"

**Solution:**
- Verify endpoint URL format
- Check network/firewall settings
- Ensure Azure OpenAI resource is active

### Issue: Tests timing out

**Solution:**
- Increase `response_time_max_seconds`
- Check Azure OpenAI service status
- Verify network connectivity

## Security Best Practices

1. **Never commit API keys** to git
2. **Use GitHub secrets** for CI/CD
3. **Rotate keys regularly** in Azure Portal
4. **Use read-only keys** if possible
5. **Monitor usage** in Azure Portal

## Example Configurations

### Minimal Configuration

```yaml
azure_openai:
  endpoint: https://your-resource.openai.azure.com/
  deployment_name: gpt-4

test_cases:
  - id: test_001
    name: Basic Test
    input:
      location: "London, UK"
    expected_output:
      contains: ["English"]
```

### Full Configuration

See `ai-tests/ai-test-config.yaml` for a complete example with all options.

## Support

For configuration issues:
1. Check this guide
2. Review Azure OpenAI documentation
3. Open an issue on GitHub
