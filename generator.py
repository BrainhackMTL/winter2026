__author__ = "akeshavan"
import glob
import json
import os

from jinja2 import Environment, FileSystemLoader


def load_json(filename):
    """Load data from a json file"""
    with open(filename, "r") as fp:
        data = json.load(fp)
    return data


def load_projects(directory):
    """
    Scans the 'data/projects' directory for JSON files,
    loads them, and adds a link to the original GitHub issue.
    """
    projects = []
    # Check if directory exists to avoid errors on fresh clones
    if not os.path.exists(directory):
        print(f"Warning: Directory {directory} not found. No projects loaded.")
        return projects

    # Glob all json files
    for filename in glob.glob(os.path.join(directory, "*.json")):
        try:
            data = load_json(filename)

            # Construct the issue URL based on the repo name
            # You can also customize this if your repo changes
            if "issue_number" in data:
                data["issue_url"] = (
                    f"https://github.com/BrainhackMTL/winter2026/issues/{data['issue_number']}"
                )

            projects.append(data)
        except Exception as e:
            print(f"Skipping {filename}: {e}")

    # Optional: Sort projects by issue number (earliest first)
    projects.sort(key=lambda x: int(x.get("issue_number", 0)))
    return projects


files_to_generate = [
    {"filename": "index.html.j2", "location": "./_site"},
    {"filename": "projects.html.j2", "location": "./_site"},  # New projects page
    {"filename": "css/stylish-portfolio.css.j2", "location": "./_site"},
]

env = Environment(loader=FileSystemLoader("./_site"))
info = load_json("data.json")

# Load the project data and add it to the 'info' dictionary
info["projects"] = load_projects("data/projects")

for f in files_to_generate:
    try:
        template = env.get_template(f["filename"])
        # Handle the output filename (remove .j2)
        outfile_name = f["filename"].replace(".j2", "")
        outfile = os.path.join(f["location"], outfile_name)

        print("writing", outfile)
        with open(outfile, "w", encoding="utf-8") as q:
            q.write(template.render(**info))
    except Exception as e:
        print(f"Error generating {f['filename']}: {e}")
