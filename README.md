# AI-Test-Pipeline

An automated testing pipeline for AI language recommendations using Azure OpenAI, with CI/CD integration via GitHub Actions.

## Overview

This project provides an AI-powered system that recommends appropriate languages for client communication based on their geographic location. It includes:

- **AI Prompt Template**: Intelligent language recommendation based on location
- **Test Dataset**: Predefined test cases for Switzerland (Zurich), Toronto, and Montreal
- **Automated Testing**: YAML-based test configuration with validation
- **CI/CD Pipeline**: Automated testing via GitHub Actions
- **Azure OpenAI Integration**: Connected to Azure OpenAI endpoint

## Project Structure

```
AI-Test-Pipeline/
├── ai-tests/
│   ├── prompts/
│   │   └── language-recommendation.txt    # AI prompt template
│   ├── datasets/
│   │   └── language-dataset.json          # Test dataset
│   ├── ai-test-config.yaml                # Test configuration
│   └── run_tests.py                       # Test runner script
├── .github/
│   └── workflows/
│       └── ai-tests.yml                   # CI/CD pipeline
├── requirements.txt                        # Python dependencies
└── README.md                              # This file
```

## Test Cases

The system tests language recommendations for:

1. **Switzerland, Zurich** → Expects: German (primary)
2. **Toronto, Canada** → Expects: English (primary)
3. **Canada, Montreal** → Expects: French (primary)

## Azure OpenAI Configuration

- **Endpoint**: `https://olhaopenai.openai.azure.com/`
- **API Version**: `2024-02-15-preview`
- **Deployment**: GPT-4 (configurable in `ai-test-config.yaml`)

## Setup Instructions

### Prerequisites

- Python 3.11+
- Azure OpenAI API access
- GitHub repository with Actions enabled

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/OlhaIshyna/AI-Test-Pipeline.git
   cd AI-Test-Pipeline
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Azure OpenAI credentials**:
   ```bash
   export AZURE_OPENAI_API_KEY='your-api-key-here'
   ```

4. **Update deployment name** (if needed):
   Edit `ai-tests/ai-test-config.yaml` and set your Azure OpenAI deployment name:
   ```yaml
   azure_openai:
     deployment_name: your-deployment-name
   ```

5. **Run tests locally**:
   ```bash
   cd ai-tests
   python run_tests.py
   ```

### CI/CD Setup

1. **Add GitHub Secret**:
   - Go to your repository Settings → Secrets and variables → Actions
   - Add a new secret named `AZURE_OPENAI_API_KEY`
   - Set the value to your Azure OpenAI API key

2. **Configure Azure OpenAI deployment**:
   - Update `ai-tests/ai-test-config.yaml` with your deployment name

3. **Trigger the pipeline**:
   - Push to `main` or `develop` branch
   - Create a pull request to `main`
   - Manually trigger from Actions tab

## Test Configuration

The `ai-test-config.yaml` file defines:

- **Azure OpenAI settings**: Endpoint, API version, deployment name
- **Prompt template**: Reference to the prompt file
- **Test cases**: Input locations and expected outputs
- **Validation criteria**: Response validation rules
- **Reporting**: Output format and file location

### Example Test Case

```yaml
test_cases:
  - id: test_001
    name: Switzerland Zurich Language Test
    input:
      location: "Switzerland, Zurich"
    expected_output:
      contains:
        - "German"
      validation_type: primary_language
```

## Dataset Format

The dataset (`language-dataset.json`) includes:

```json
{
  "test_cases": [
    {
      "id": "test_001",
      "location": "Switzerland, Zurich",
      "expected_primary_language": "German",
      "expected_secondary_languages": ["English", "French"],
      "description": "Zurich is in the German-speaking region of Switzerland"
    }
  ]
}
```

## Running Tests

### Local Execution

```bash
cd ai-tests
python run_tests.py
```

Output:
- Console output with test results
- `test-results.json` file with detailed results

### CI/CD Execution

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main`
- Manual workflow dispatch

Results are uploaded as artifacts in the GitHub Actions run.

## Test Results

The test runner generates a JSON report with:

- Total tests executed
- Passed/failed/error counts
- Individual test results
- AI responses and validation status
- Response times

Example output:
```json
{
  "total_tests": 3,
  "passed": 3,
  "failed": 0,
  "errors": 0,
  "skipped": 0,
  "results": [...]
}
```

## Extending the System

### Adding New Test Cases

1. Edit `ai-tests/ai-test-config.yaml`
2. Add a new test case:
   ```yaml
   - id: test_004
     name: New Location Test
     input:
       location: "Your Location"
     expected_output:
       contains:
         - "Expected Language"
   ```

3. Update the dataset in `ai-tests/datasets/language-dataset.json`

### Modifying the Prompt

Edit `ai-tests/prompts/language-recommendation.txt` to customize the AI behavior.

## Troubleshooting

### API Key Issues

If tests are skipped:
- Verify `AZURE_OPENAI_API_KEY` is set (locally) or configured as a GitHub secret
- Check the API key has proper permissions

### Deployment Name Errors

If you get deployment errors:
- Update `deployment_name` in `ai-test-config.yaml` to match your Azure OpenAI deployment

### Test Failures

Check the following:
- AI response contains expected keywords
- Response meets validation criteria (length, timing)
- Azure OpenAI endpoint is accessible

## License

This project is part of the AI-Test-Pipeline repository.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions, please open an issue in the GitHub repository.
