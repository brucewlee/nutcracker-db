import os
import yaml
from datetime import datetime

def count_lines_in_file(file_path):
    """Count the number of lines in a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)

def extract_data_from_config(config_path, test_jsonl_path):
    """Extract specified data from a config.yaml file and count lines in test.jsonl."""
    with open(config_path, encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    dataset_size = count_lines_in_file(test_jsonl_path) if os.path.exists(test_jsonl_path) else 'N/A'
    
    return {
        'task_name': config_data.get('task_name', 'N/A'),
        'version': config_data.get('version', 'N/A'),
        'construction': f"{config_data.get('construction', {}).get('class', 'N/A')}, {config_data.get('construction', {}).get('n_choices', 'N/A')}",
        'arxiv': config_data.get('arxiv', 'N/A'),
        'license': config_data.get('license', 'N/A'),
        'user_prompt_template': ", ".join([f"{k}: {v}" for k, v in config_data.get('user_prompt_template', {}).items()]),
        'dataset_size': dataset_size
    }

def generate_markdown_table(data):
    """Convert a list of lists into a Markdown table."""
    markdown = ['|' + '|'.join(data[0]) + '|', '|' + '|'.join(['---'] * len(data[0])) + '|']
    for row in data[1:]:
        sanitized_row = [str(cell).replace('|', '\\|') for cell in row]
        markdown.append('|' + '|'.join(sanitized_row) + '|')
    return '\n'.join(markdown)

def write_readme(base_path, readme_table, total_tasks, total_instances):
    readme_path = 'README.md'  # Ensure the README.md is written to the base path
    latest_update = datetime.now().strftime("%Y-%m-%d")
    latest_change = "Added sanity checker."

    readme_content = f"""# Nutcracker-DB

## Latest Update
- Date: {latest_update}
- Change: {latest_change}

## Database Statistics
- Total Number of Tasks: {total_tasks}
- Total Number of Instances: {total_instances}

## Dataset Overview
{readme_table}

"""
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

def generate_readme_table_and_stats(base_path):
    headers = ['Index', 'Task Name', 'Version', 'Construction', 'Arxiv Link', 'License', 'Dataset Size']
    table_data = [headers]
    total_tasks = 0
    total_instances = 0
    
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    sorted_directories = sorted(directories)
    
    for index, item in enumerate(sorted_directories, start=1):
        dir_path = os.path.join(base_path, item)
        config_path = os.path.join(dir_path, 'config.yaml')
        test_jsonl_path = os.path.join(dir_path, 'test.json')
        if os.path.exists(config_path):
            config_data = extract_data_from_config(config_path, test_jsonl_path)
            dataset_size = 0 if config_data['dataset_size'] == 'N/A' else int(config_data['dataset_size'])
            total_instances += dataset_size
            total_tasks += 1
            table_data.append([
                str(index),
                config_data['task_name'],
                config_data['version'],
                config_data['construction'],
                config_data['arxiv'],
                config_data['license'],
                str(config_data['dataset_size'])
            ])
    
    markdown_table = generate_markdown_table(table_data)
    return markdown_table, total_tasks, total_instances

# Adjusted example usage
base_path = 'db/'  # Adjust this path to your base directory
readme_table, total_tasks, total_instances = generate_readme_table_and_stats(base_path)
write_readme(base_path, readme_table, total_tasks, total_instances)
print("README.md has been generated with the table of config.yaml files including dataset size and database statistics.")