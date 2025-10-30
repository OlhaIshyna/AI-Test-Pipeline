#!/usr/bin/env python3
import os
import json
import yaml
import sys
import time
from typing import Dict, Any

try:
    from openai import AzureOpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

# Optional fallback mapping for language recommendations
CITY_LANGUAGE_MAP = {
    "Montreal": "French",
    "Toronto": "English",
    "Paris": "French",
    "Berlin": "German"
}

class AITestRunner:
    def __init__(self, config_path: str):
        self.config = self._load_yaml(config_path)
        self.dataset = self._load_json(self.config['dataset']['file'])
        self.prompt_template = self._load_file(self.config['prompt']['template_file'])
        self.client = self._init_client()

    def _load_yaml(self, path: str):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _load_json(self, path: str):
        with open(path, 'r') as f:
            return json.load(f)

    def _load_file(self, path: str):
        with open(path, 'r') as f:
            return f.read()

    def _init_client(self):
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        if not api_key:
            print("Warning: AZURE_OPENAI_API_KEY not set. Running in offline mode.")
            return None
        return AzureOpenAI(
            api_key=api_key,
            api_version=self.config['azure_openai']['api_version'],
            azure_endpoint=self.config['azure_openai']['endpoint']
        )

    def run_test_case(self, case: Dict[str, Any]) -> Dict[str, Any]:
        location = case['input']['location']
        prompt = self.prompt_template.format(location=location)
        result = {"id": case['id'], "name": case['name'], "location": location}

        if not self.client:
            result.update({"status": "skipped", "message": "No API client"})
            return result

        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=self.config['azure_openai']['deployment_name'],
                messages=[
                    {"role": "system", "content": "You recommend languages."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            ai_text = response.choices[0].message.content
            result.update({
                "status": "passed",
                "response": ai_text,
                "time": round(time.time() - start, 2)
            })
        except Exception as e:
            # Fallback to local mapping
            fallback = CITY_LANGUAGE_MAP.get(location.split(",")[0], "Unknown")
            result.update({
                "status": "error",
                "error": str(e),
                "fallback_language": fallback
            })
        return result

    def run_all(self):
        summary = [self.run_test_case(tc) for tc in self.config['test_cases']]
        print(json.dumps(summary, indent=2))
        return summary

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "ai-test-config.yaml")
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)

    runner = AITestRunner(config_path)
    results = runner.run_all()
    sys.exit(1 if any(r['status'] == "error" for r in results) else 0)
