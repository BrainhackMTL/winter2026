import json
import os
from pathlib import Path

from markdown_it import MarkdownIt

md = MarkdownIt()


def parse_issue_body(body: str) -> dict[str, str | None]:
    """
    Parses a GitHub Issue Form body (Markdown) into a dictionary.
    Assumes headers are denoted by '### '.
    """
    data: dict[str, str | None] = {}
    current_key = None
    current_value: list[str] = []

    # Helper function to clean text and remove default GitHub placeholder
    def clean_text(lines_list: list[str]) -> str | None:
        text = "\n".join(lines_list).strip()
        # Check for the specific GitHub placeholder
        if text == "_No response_":
            return None
        return md.render(text)

    # Split the body by lines
    lines = body.splitlines()

    for line in lines:
        line = line.strip()

        # Check if the line is a header (Question)
        if line.startswith("### "):
            # If we were already collecting a value for a previous key, save it
            if current_key:
                data[current_key] = clean_text(current_value)

            # Set the new key (removing the ### and whitespace)
            current_key = line[4:].strip()
            current_value = []
        else:
            # If we are inside a section, append the line to the value
            if current_key:
                current_value.append(line)

    # Save the last section
    if current_key:
        data[current_key] = clean_text(current_value)

    return data


def main():
    # 1. Get environment variables passed from the GitHub Action
    issue_body = os.environ.get("ISSUE_BODY", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "0")

    if not issue_body:
        print("No issue body found.")
        return

    # 2. Parse the body
    parsed_data = parse_issue_body(issue_body)

    # Add metadata
    parsed_data["issue_number"] = issue_number

    # 3. Ensure the output directory exists
    output_dir = Path("data/projects")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 4. Save to JSON file (e.g., data/projects/project_123.json)
    filename = f"project_{issue_number}.json"
    file_path = output_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved project data to {file_path}")


if __name__ == "__main__":
    main()
