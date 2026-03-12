#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from google import genai
from google.genai import types

SYSTEM_PROMPT = """
You are 'Arbiter', a specialized prompt security and logic auditor. 
Your goal is to detect 'Interference Patterns' in LLM system prompts.

Interference occurs when:
1. CONFLICT: Two rules directly contradict each other (e.g., 'be concise' vs 'be verbose').
2. SHADOWING: A broad rule makes a specific rule unreachable.
3. REDUNDANCY: The same rule is stated multiple times across different files, wasting tokens.
4. AMBIGUITY: A rule is phrased so loosely that an agent might interpret it in dangerous ways.

Identify specific findings from the provided text.
For each finding, provide:
- TYPE: [Conflict|Shadowing|Redundancy|Ambiguity]
- DESCRIPTION: Why this is an issue.
- REMEDY: How to fix the rule or file.
"""

def load_context(directory):
    path = Path(directory)
    context = ""
    for f in path.glob("*.md"):
        if f.is_file():
            context += f"--- FILE: {f.name} ---\n{f.read_text()}\n\n"
    return context

def run_audit(directory, api_key, model):
    context = load_context(directory)
    if not context:
        print(f"Error: No markdown files found in {directory}")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=model,
            contents=f"SYSTEM CONTEXT:\n\n{context}",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=2048,
                temperature=0.2,
            )
        )
        return response.text
    except Exception as e:
        print(f"Error during audit: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Arbiter Linter: Detect interference in LLM system prompts.")
    parser.add_argument("directory", help="Directory containing system prompt markdown files.")
    parser.add_argument("--key", help="Gemini API Key (or set GEMINI_API_KEY env var).")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model to use.")
    parser.add_argument("--output", help="Save report to file.")

    args = parser.parse_args()
    api_key = args.key or os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Error: Gemini API Key is required via --key or GEMINI_API_KEY env var.")
        sys.exit(1)

    print(f"🔍 Arbiter: Scouring {args.directory} for prompt interference...")
    report = run_audit(args.directory, api_key, args.model)

    print("\n" + "="*50)
    print("⚖️ ARBITER LINT REPORT")
    print("="*50 + "\n")
    print(report)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport saved to {args.output}")

if __name__ == "__main__":
    main()
