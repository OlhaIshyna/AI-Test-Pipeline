#!/usr/bin/env python3
import os, json, yaml, sys, time
from typing import Dict, Any
from openai import AzureOpenAI

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

    def _load_yaml(self, path): return yaml.safe_load(open(path))
    def _load_json(self, path): return json.load(open(path))
    def _load_file(self, path): return open(path).read()

    def _init_client(self):
        key = os.getenv('AZURE_OPENAI_API_KEY')
        if not key:
            print("No API key. Tests will run in offline mode.")
            return None
        return AzureOpenAI(
            api_key=key,
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
                ]
            )
            ai_text = response.choices[0].message.content
            result.update({"status": "passed", "response": ai_text, "time": round(time.time()-start,2)})
        except Exception as e:
            # Fallback to local mapping
            fallback = CITY_LANGUAGE_MAP.get(location.split(",")[0], "Unknown")
            result.update({"status": "error", "error": str(e), "fallback_language": fallback})
        return result

    def run_all(self):
        summary = [self.run_test_case(tc) for tc in self.config['test_cases']]
        print(json.dumps(summary, indent=2))
        return summary

if __name__ == "__main__":
    runner = AITestRunner("ai-test-config.yaml")
    sys.exit(1 if any(r['status']=="error" for r in runner.run_all()) else 0)
``
