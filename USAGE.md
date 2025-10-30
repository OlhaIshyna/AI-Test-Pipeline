# Usage Guide

## Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Azure OpenAI API key
export AZURE_OPENAI_API_KEY='your-api-key-here'
```

### 2. Configure Your Deployment

Edit `ai-tests/ai-test-config.yaml`:

```yaml
azure_openai:
  endpoint: https://olhaopenai.openai.azure.com/
  api_version: "2024-02-15-preview"
  deployment_name: your-deployment-name  # Change this
```

### 3. Run Tests

```bash
cd ai-tests
python run_tests.py
```

## Expected Output

```
============================================================
AI Test Suite: Language Recommendation System
============================================================

Running test: Switzerland Zurich Language Test (ID: test_001)
Location: Switzerland, Zurich
Response: For a client in Zurich, Switzerland, I recommend using German as the primary language...
Response Time: 2.34s
Status: PASSED

Running test: Toronto Canada Language Test (ID: test_002)
Location: Toronto, Canada
Response: For a client in Toronto, Canada, I recommend using English as the primary language...
Response Time: 1.89s
Status: PASSED

Running test: Montreal Canada Language Test (ID: test_003)
Location: Canada, Montreal
Response: For a client in Montreal, Canada, I recommend using French as the primary language...
Response Time: 2.12s
Status: PASSED

============================================================
Test Summary
============================================================
Total Tests: 3
Passed: 3
Failed: 0
Errors: 0
Skipped: 0

Results saved to: ai-tests/test-results.json
```

## Understanding Test Results

The `test-results.json` file contains detailed information:

```json
{
  "total_tests": 3,
  "passed": 3,
  "failed": 0,
  "errors": 0,
  "skipped": 0,
  "results": [
    {
      "test_id": "test_001",
      "test_name": "Switzerland Zurich Language Test",
      "location": "Switzerland, Zurich",
      "status": "passed",
      "response": "For a client in Zurich, Switzerland...",
      "response_time": 2.34,
      "validation": true,
      "timestamp": "2025-10-30 14:54:15"
    }
  ]
}
```

## Adding Custom Test Cases

### Step 1: Add to Configuration

Edit `ai-tests/ai-test-config.yaml`:

```yaml
test_cases:
  - id: test_004
    name: Paris France Language Test
    input:
      location: "Paris, France"
    expected_output:
      contains:
        - "French"
      validation_type: primary_language
```

### Step 2: Add to Dataset

Edit `ai-tests/datasets/language-dataset.json`:

```json
{
  "id": "test_004",
  "location": "Paris, France",
  "expected_primary_language": "French",
  "expected_secondary_languages": ["English"],
  "description": "Paris is in France, a French-speaking country"
}
```

### Step 3: Run Tests

```bash
cd ai-tests
python run_tests.py
```

## CI/CD Integration

### Setup GitHub Actions

1. **Add API Key Secret**:
   - Repository Settings → Secrets → Actions
   - New secret: `AZURE_OPENAI_API_KEY`

2. **Trigger Pipeline**:
   ```bash
   git add .
   git commit -m "Add new test case"
   git push
   ```

3. **View Results**:
   - GitHub Actions tab
   - Select the workflow run
   - Download artifacts: `ai-test-results`

## Troubleshooting

### Issue: Tests are skipped

**Cause**: API key not set

**Solution**:
```bash
export AZURE_OPENAI_API_KEY='your-key'
```

### Issue: Deployment not found

**Cause**: Incorrect deployment name

**Solution**: Update `deployment_name` in `ai-test-config.yaml`

### Issue: Response validation failed

**Cause**: AI response doesn't contain expected keyword

**Solution**: 
- Check if the expected keyword is too specific
- Review the AI response in the output
- Adjust expected keywords if needed

## Best Practices

1. **Keep prompts clear and specific**: Better prompts = better AI responses
2. **Use meaningful test IDs**: Makes debugging easier
3. **Test incrementally**: Add one test case at a time
4. **Review failed tests**: Understand why they failed before adjusting
5. **Version your prompts**: Track changes to prompt templates

## Advanced Usage

### Custom Validation

Edit `run_tests.py` to add custom validation logic:

```python
def _validate_response(self, response: str, expected: Dict[str, Any]) -> bool:
    # Add your custom validation here
    pass
```

### Multiple Prompts

1. Create new prompt file in `prompts/`
2. Add new test configuration
3. Update `run_tests.py` to handle multiple prompts

### Integration with Other Systems

The test runner can be imported and used programmatically:

```python
from run_tests import AITestRunner

runner = AITestRunner('ai-test-config.yaml')
summary = runner.run_all_tests()
print(f"Passed: {summary['passed']}/{summary['total_tests']}")
```

## Support

For questions or issues:
1. Check this usage guide
2. Review the main README.md
3. Open an issue on GitHub
