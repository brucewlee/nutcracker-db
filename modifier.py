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
prefix = "hhh-*" #prefix then *

# Define actions as a list of modifications/deletions to perform
actions = [
    {"type": "modify", "data": {"abstract": "A General Language Assistant as a Laboratory for Alignment - Given the broad capabilities of large language models, it should be possible to work towards a general-purpose, text-based assistant that is aligned with human values, meaning that it is helpful, honest, and harmless. As an initial foray in this direction we study simple baseline techniques and evaluations, such as prompting. We find that the benefits from modest interventions increase with model size, generalize to a variety of alignment evaluations, and do not compromise the performance of large models. Next we investigate scaling trends for several training objectives relevant to alignment, comparing imitation learning, binary discrimination, and ranked preference modeling. We find that ranked preference modeling performs much better than imitation learning, and often scales more favorably with model size. In contrast, binary discrimination typically performs and scales very similarly to imitation learning. Finally we study a `preference model pre-training' stage of training, with the goal of improving sample efficiency when finetuning on human preferences."}},
    {"type": "modify", "data": {"arxiv": "https://arxiv.org/abs/2112.00861"}},
    {"type": "modify", "data": {"construction": {"class": "mcq", "n_choices": 2}}},
    {"type": "modify", "data": {"few_shot": 0}},
    {"type": "modify", "data": {"timeline": "~2023.12.01"}},
    {"type": "modify", "data": {"license": "apache-2.0"}},
    {"type": "modify", "data": {
        "web_source": {
            "file": {
                "dev": None,
                "test": "data/*/task.json"
                }, 
            "location": "https://huggingface.co/datasets/HuggingFaceH4/hhh_alignment"
            }
        }
    },
    {"type": "modify", "data": {
        "user_prompt_template": {
            "start_note": None,
            "example": None,
            "mid_note": None,
            "test": "Question: \"{centerpiece}\" Answer: \n{options[0]}\n{options[1]} ",
            "end_note": None,
            }
        }
    },
    
    #{"type": "delete", "data": ["citation"]}
]

license_content = "Author did not provide a license file but confirmed that the work is released under Apache-2.0 license."
citation_content = """@article{askell2021general,
  title={A general language assistant as a laboratory for alignment},
  author={Askell, Amanda and Bai, Yuntao and Chen, Anna and Drain, Dawn and Ganguli, Deep and Henighan, Tom and Jones, Andy and Joseph, Nicholas and Mann, Ben and DasSarma, Nova and others},
  journal={arXiv preprint arXiv:2112.00861},
  year={2021}
}"""
process_directories(path_to_search, prefix, actions, license_content, citation_content)
