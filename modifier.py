import os
import yaml
import fnmatch

def escape_newlines(data):
    """
    Recursively escape newline characters in string values within a nested dictionary.
    """
    if isinstance(data, dict):
        return {k: escape_newlines(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [escape_newlines(v) for v in data]
    elif isinstance(data, str):
        return data.replace('\n', '\\n')
    else:
        return data

def unescape_newlines_in_file(file_path):
    """
    Replace escaped newline placeholders in a file with actual newline characters.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('\\n', '\n')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def deep_update(source, updates):
    """
    Update a nested dictionary or similar mapping.
    Modify `source` in place.
    """
    for key, value in updates.items():
        if isinstance(value, dict) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = updates[key]
    return source

def modify_yaml_file(file_path, actions):
    """Load, modify/delete keys, and save a YAML file based on actions."""
    with open(file_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    for action in actions:
        if action['type'] == "modify":
            # Use deep_update for nested dictionaries
            #deep_update(data, action['data'])
            updated_data = escape_newlines(action['data'])
            data = deep_update(data, updated_data)
        elif action['type'] == "delete":
            for key in action['data']:
                if key in data:
                    del data[key]
                    print(f"Deleted key: {key}")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=True, width=50000)

def add_license_file(directory, license_content):
    """Add a license file to the specified directory."""
    license_file_path = os.path.join(directory, "LICENSE.txt")
    with open(license_file_path, 'w') as f:
        f.write(license_content)

def add_citation_file(directory, citation_content):
    """Add a citation file to the specified directory."""
    citation_file_path = os.path.join(directory, "CITATION.bib")
    with open(citation_file_path, 'w') as f:
        f.write(citation_content)

def process_directories(base_path, prefix, actions, license_content=None, citation_content=None):
    """Process directories, perform actions (modify/delete) on YAML configs, and optionally add a license file."""
    for item in os.listdir(base_path):
        dir_path = os.path.join(base_path, item)
        if os.path.isdir(dir_path) and fnmatch.fnmatch(item, prefix):
            print(f"Processing directory: {dir_path}")
            config_path = os.path.join(dir_path, "config.yaml")
            if os.path.exists(config_path):
                print(f"Modifying: {config_path}")
                modify_yaml_file(config_path, actions)
            if license_content:
                print(f"Adding license to: {dir_path}")
                add_license_file(dir_path, license_content)
            if citation_content:
                print(f"Adding citation to: {dir_path}")
                add_citation_file(dir_path, citation_content)

# Example usage
path_to_search = "db"  # Current directory
prefix = "math-*" #prefix then *

# Define actions as a list of modifications/deletions to perform
actions = [
    {"type": "modify", "data": {"abstract": "Measuring Mathematical Problem Solving With the MATH Dataset - Many intellectual endeavors require mathematical problem solving, but this skill remains beyond the capabilities of computers. To measure this ability in machine learning models, we introduce MATH, a new dataset of 12,500 challenging competition mathematics problems. Each problem in MATH has a full step-by-step solution which can be used to teach models to generate answer derivations and explanations. To facilitate future research and increase accuracy on MATH, we also contribute a large auxiliary pretraining dataset which helps teach models the fundamentals of mathematics. Even though we are able to increase accuracy on MATH, our results show that accuracy remains relatively low, even with enormous Transformer models. Moreover, we find that simply increasing budgets and model parameter counts will be impractical for achieving strong mathematical reasoning if scaling trends continue. While scaling Transformers is automatically solving most other text-based tasks, scaling is not currently solving MATH. To have more traction on mathematical problem solving we will likely need new algorithmic advancements from the broader research community."}},
    {"type": "modify", "data": {"arxiv": "https://arxiv.org/abs/2103.03874"}},
    {"type": "modify", "data": {"construction": {"class": "frq", "type": "simple"}}},
    {"type": "modify", "data": {"few_shot": 5}},
    {"type": "modify", "data": {"timeline": "~2021.11.18"}},
    {"type": "modify", "data": {"license": "mit"}},
    {"type": "modify", "data": {
        "web_source": {
            "file": {
                "dev": "train/*[:101]",
                "test": "test/*"
                }, 
            "location": "https://people.eecs.berkeley.edu/~hendrycks/MATH.tar"
            }
        }
    },
    {"type": "modify", "data": {
        "user_prompt_template": {
            "example": 'Question: {centerpiece} Answer: {answer}\n\n',
            "test": 'Question: {centerpiece} Answer: ',
            }
        }
    },
    
    #{"type": "delete", "data": ["citation"]}
]

license_content = """MIT License

Copyright (c) 2021 Dan Hendrycks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
citation_content = """@article{hendrycksmath2021,
  title={Measuring Mathematical Problem Solving With the MATH Dataset},
  author={Dan Hendrycks and Collin Burns and Saurav Kadavath and Akul Arora and Steven Basart and Eric Tang and Dawn Song and Jacob Steinhardt},
  journal={NeurIPS},
  year={2021}
}
"""
process_directories(path_to_search, prefix, actions, license_content, citation_content)
