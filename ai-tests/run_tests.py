#!/usr/bin/env python3
"""
AI Test Runner for Language Recommendation System
Connects to Azure OpenAI and validates responses against test dataset
"""

import os
import json
import yaml
import sys
from typing import Dict, List, Any
import time

try:
    from openai import AzureOpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)


class AITestRunner:
    def __init__(self, config_path: str):
        """Initialize the test runner with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Load dataset
        dataset_path = os.path.join(
            os.path.dirname(config_path),
            self.config['dataset']['file']
        )
        with open(dataset_path, 'r') as f:
            self.dataset = json.load(f)
        
        # Load prompt template
        prompt_path = os.path.join(
            os.path.dirname(config_path),
            self.config['prompt']['template_file']
        )
        with open(prompt_path, 'r') as f:
            self.prompt_template = f.read()
        
        # Initialize Azure OpenAI client
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Azure OpenAI client with credentials from environment."""
        api_key = os.environ.get('AZURE_OPENAI_API_KEY')
        if not api_key:
            print("Warning: AZURE_OPENAI_API_KEY not set. Skipping API calls.")
            return
        
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=self.config['azure_openai']['api_version'],
            azure_endpoint=self.config['azure_openai']['endpoint']
        )
    
    def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case."""
        test_id = test_case['id']
        location = test_case['input']['location']
        
        print(f"\nRunning test: {test_case['name']} (ID: {test_id})")
        print(f"Location: {location}")
        
        # Create prompt from template
        prompt = self.prompt_template.replace('{location}', location)
        
        result = {
            'test_id': test_id,
            'test_name': test_case['name'],
            'location': location,
            'status': 'pending',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if not self.client:
            result['status'] = 'skipped'
            result['message'] = 'Azure OpenAI client not initialized'
            print(f"Status: SKIPPED (no API key)")
            return result
        
        try:
            # Call Azure OpenAI
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.config['azure_openai']['deployment_name'],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides language recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            end_time = time.time()
            
            ai_response = response.choices[0].message.content
            response_time = end_time - start_time
            
            result['response'] = ai_response
            result['response_time'] = response_time
            
            # Validate response
            validation_passed = self._validate_response(
                ai_response,
                test_case['expected_output']
            )
            
            result['status'] = 'passed' if validation_passed else 'failed'
            result['validation'] = validation_passed
            
            print(f"Response: {ai_response}")
            print(f"Response Time: {response_time:.2f}s")
            print(f"Status: {'PASSED' if validation_passed else 'FAILED'}")
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            print(f"Status: ERROR - {e}")
        
        return result
    
    def _validate_response(self, response: str, expected: Dict[str, Any]) -> bool:
        """Validate AI response against expected criteria."""
        # Check if response contains expected keywords
        contains = expected.get('contains', [])
        for keyword in contains:
            if keyword.lower() not in response.lower():
                print(f"  Validation failed: '{keyword}' not found in response")
                return False
        
        # Check response length
        validation = self.config.get('validation', {})
        criteria = validation.get('criteria', [])
        
        for criterion in criteria:
            if isinstance(criterion, dict):
                if 'response_length_min' in criterion:
                    if len(response) < criterion['response_length_min']:
                        print(f"  Validation failed: Response too short")
                        return False
                if 'response_length_max' in criterion:
                    if len(response) > criterion['response_length_max']:
                        print(f"  Validation failed: Response too long")
                        return False
        
        return True
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test cases and generate report."""
        print("=" * 60)
        print("AI Test Suite: Language Recommendation System")
        print("=" * 60)
        
        results = []
        for test_case in self.config['test_cases']:
            result = self.run_test_case(test_case)
            results.append(result)
        
        # Generate summary
        summary = {
            'total_tests': len(results),
            'passed': sum(1 for r in results if r['status'] == 'passed'),
            'failed': sum(1 for r in results if r['status'] == 'failed'),
            'errors': sum(1 for r in results if r['status'] == 'error'),
            'skipped': sum(1 for r in results if r['status'] == 'skipped'),
            'results': results
        }
        
        # Print summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Errors: {summary['errors']}")
        print(f"Skipped: {summary['skipped']}")
        
        # Save results
        output_file = self.config.get('reporting', {}).get('output_file', 'test-results.json')
        output_path = os.path.join(os.path.dirname(sys.argv[0]), output_file)
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\nResults saved to: {output_path}")
        
        return summary


def main():
    """Main entry point."""
    config_path = os.path.join(
        os.path.dirname(__file__),
        'ai-test-config.yaml'
    )
    
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)
    
    runner = AITestRunner(config_path)
    summary = runner.run_all_tests()
    
    # Exit with error code if any tests failed
    if summary['failed'] > 0 or summary['errors'] > 0:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
