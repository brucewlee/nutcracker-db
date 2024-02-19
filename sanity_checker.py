import os
import json
import yaml

def check_mcq_files(directory):
    for root, dirs, files in os.walk(directory):
        for sub_dir in dirs:
            dir_path = os.path.join(root, sub_dir)
            config_path = os.path.join(dir_path, 'config.yaml')
            test_path = os.path.join(dir_path, 'test.json')
            dev_path = os.path.join(dir_path, 'dev.json')

            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    if config['construction']['class'].lower() == 'mcq':
                        n_choices = config['construction'].get('n_choices', 'mixed')
                        print(f"Checking {sub_dir}...")
                        if os.path.exists(test_path):
                            check_file(test_path, n_choices)
                        if os.path.exists(dev_path):
                            check_file(dev_path, n_choices)

def check_file(file_path, n_choices):
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            checks = [
                'centerpiece' in data,
                isinstance(data.get('options', []), list),
                isinstance(data.get('correct_options', []), list),
                isinstance(data.get('correct_options_literal', []), list),
                isinstance(data.get('correct_options_idx', []), list)
            ]
            
            if not all(checks):
                print(f"Missing or incorrect fields in {file_path}")
                continue
            
            if n_choices != 'mixed':
                if not all(len(data['options']) == n_choices for key in ['options', 'correct_options', 'correct_options_literal', 'correct_options_idx']):
                    print(f"Element count mismatch in {file_path}")
                if not len(data['correct_options']) == len(data['correct_options_literal']) == len(data['correct_options_idx']):
                    print(f"Correct options count mismatch in {file_path}")

# Example usage
directory = 'db'
check_mcq_files(directory)
