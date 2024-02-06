import os
import yaml
import fnmatch

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
            deep_update(data, action['data'])
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
prefix = "htest-*" #prefix then *

# Define actions as a list of modifications/deletions to perform
actions = [
    {"type": "delete", "data": ["user_prompt_template"]},
    {"type": "modify", "data": {
        "user_prompt_template": {
            "example": "Question: \"{centerpiece}\" Answer: {correct_options[0]} \n\n",
            "test": "Question: \"{centerpiece}\" Answer: \n{options[0]}\n{options[1]} (Respond in one letter and nothing else)",
            }
        }
    },
    
    #{"type": "delete", "data": ["citation"]}
]

license_content = None
citation_content = None
process_directories(path_to_search, prefix, actions, license_content, citation_content)
