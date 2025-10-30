#!/bin/bash

# Setup script for AI Test Pipeline
# This script helps you configure and test the AI pipeline

set -e

echo "======================================"
echo "AI Test Pipeline Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.11 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION ✓"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "Dependencies installed ✓"
echo ""

# Check for API key
echo "Checking Azure OpenAI configuration..."
if [ -z "$AZURE_OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: AZURE_OPENAI_API_KEY environment variable is not set"
    echo ""
    echo "To run tests with Azure OpenAI, you need to set your API key:"
    echo "  export AZURE_OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "Tests will run in 'skip' mode without the API key."
    echo ""
else
    echo "AZURE_OPENAI_API_KEY is set ✓"
    echo ""
fi

# Validate configuration files
echo "Validating configuration files..."
python3 -c "import yaml, json; yaml.safe_load(open('ai-tests/ai-test-config.yaml')); json.load(open('ai-tests/datasets/language-dataset.json')); print('Configuration files are valid ✓')"
echo ""

# Check deployment name
echo "Checking Azure OpenAI deployment configuration..."
DEPLOYMENT_NAME=$(python3 -c "import yaml; print(yaml.safe_load(open('ai-tests/ai-test-config.yaml'))['azure_openai']['deployment_name'])")
echo "Deployment name: $DEPLOYMENT_NAME"
echo ""
echo "⚠️  Make sure this matches your Azure OpenAI deployment name."
echo "   Update it in ai-tests/ai-test-config.yaml if needed."
echo ""

# Run tests
echo "======================================"
echo "Running AI Tests"
echo "======================================"
echo ""
cd ai-tests
python3 run_tests.py
cd ..
echo ""

# Summary
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Set AZURE_OPENAI_API_KEY if not already set"
echo "2. Update deployment_name in ai-tests/ai-test-config.yaml"
echo "3. Run tests: cd ai-tests && python run_tests.py"
echo ""
echo "For GitHub Actions CI/CD:"
echo "1. Add AZURE_OPENAI_API_KEY to repository secrets"
echo "2. Push changes to trigger the workflow"
echo ""
echo "Documentation:"
echo "- README.md - Overview and documentation"
echo "- USAGE.md - Usage examples"
echo "- CONFIGURATION.md - Configuration guide"
echo ""
