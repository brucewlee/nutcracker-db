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
path_to_search = "."  # Current directory
prefix = "htest*" #prefix then *

# Define actions as a list of modifications/deletions to perform
actions = [
    {"type": "modify", "data": {"abstract": "WinoGrande: An Adversarial Winograd Schema Challenge at Scale - The Winograd Schema Challenge (WSC) (Levesque, Davis, and Morgenstern 2011), a benchmark for commonsense reasoning, is a set of 273 expert-crafted pronoun resolution problems originally designed to be unsolvable for statistical models that rely on selectional preferences or word associations. However, recent advances in neural language models have already reached around 90% accuracy on variants of WSC. This raises an important question whether these models have truly acquired robust commonsense capabilities or whether they rely on spurious biases in the datasets that lead to an overestimation of the true capabilities of machine commonsense. To investigate this question, we introduce WinoGrande, a large-scale dataset of 44k problems, inspired by the original WSC design, but adjusted to improve both the scale and the hardness of the dataset. The key steps of the dataset construction consist of (1) a carefully designed crowdsourcing procedure, followed by (2) systematic bias reduction using a novel AfLite algorithm that generalizes human-detectable word associations to machine-detectable embedding associations. The best state-of-the-art methods on WinoGrande achieve 59.4-79.1%, which are 15-35% below human performance of 94.0%, depending on the amount of the training data allowed. Furthermore, we establish new state-of-the-art results on five related benchmarks - WSC (90.1%), DPR (93.1%), COPA (90.6%), KnowRef (85.6%), and Winogender (97.1%). These results have dual implications: on one hand, they demonstrate the effectiveness of WinoGrande when used as a resource for transfer learning. On the other hand, they raise a concern that we are likely to be overestimating the true capabilities of machine commonsense across all these benchmarks. We emphasize the importance of algorithmic bias reduction in existing and future benchmarks to mitigate such overestimation."}},
    {"type": "modify", "data": {"arxiv": "https://arxiv.org/abs/1907.10641"}},
    {"type": "modify", "data": {"construction": {"class": "mcq", "n_choices": 2}}},
    {"type": "modify", "data": {"license": "apache-2.0"}},
    {"type": "modify", "data": {"web_source": {"file": {"dev": "winogrande_1.1/train.jsonl[:101]", "test": "winogrande_1.1/dev.jsonl"}, "location": "https://winogrande.allenai.org/"}}},
    #{"type": "delete", "data": ["citation"]}
]

license_content = None
citation_content = None
process_directories(path_to_search, prefix, actions, license_content, citation_content)
