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
python3 -m pip install -r requirements.txt
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
if python3 -c "import yaml; yaml.safe_load(open('ai-tests/ai-test-config.yaml'))" 2>/dev/null; then
    echo "  ai-test-config.yaml is valid ✓"
else
    echo "  ❌ Error: ai-test-config.yaml is invalid or missing"
    exit 1
fi

if python3 -c "import json; json.load(open('ai-tests/datasets/language-dataset.json'))" 2>/dev/null; then
    echo "  language-dataset.json is valid ✓"
else
    echo "  ❌ Error: language-dataset.json is invalid or missing"
    exit 1
fi
echo ""

# Check deployment name
echo "Checking Azure OpenAI deployment configuration..."
GET_DEPLOYMENT_CMD='import yaml; config = yaml.safe_load(open("ai-tests/ai-test-config.yaml")); print(config.get("azure_openai", {}).get("deployment_name", "NOT_SET"))'
if DEPLOYMENT_NAME=$(python3 -c "$GET_DEPLOYMENT_CMD" 2>/dev/null); then
    if [ "$DEPLOYMENT_NAME" = "NOT_SET" ]; then
        echo "  ⚠️  Warning: Deployment name not found in configuration"
    else
        echo "  Deployment name: $DEPLOYMENT_NAME"
    fi
else
    echo "  ⚠️  Warning: Could not read deployment name from configuration"
fi
echo ""
echo "⚠️  Make sure the deployment name matches your Azure OpenAI deployment."
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
