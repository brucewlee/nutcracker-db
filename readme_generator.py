import os
import yaml

def count_lines_in_file(file_path):
    """Count the number of lines in a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)

def extract_data_from_config(config_path, test_jsonl_path):
    """Extract specified data from a config.yaml file and count lines in test.jsonl."""
    with open(config_path, encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    # Count lines in test.jsonl for dataset size, if exists
    dataset_size = count_lines_in_file(test_jsonl_path) if os.path.exists(test_jsonl_path) else 'N/A'
    
    # Extract required fields with detailed sub-fields as necessary
    return {
        'task_name': config_data.get('task_name', 'N/A'),
        'version': config_data.get('version', 'N/A'),
        'construction': f"{config_data.get('construction', {}).get('class', 'N/A')}, {config_data.get('construction', {}).get('n_choices', 'N/A')}",
        'arxiv': config_data.get('arxiv', 'N/A'),
        'license': config_data.get('license', 'N/A'),
        'user_prompt_template': ", ".join([f"{k}: {v}" for k, v in config_data.get('user_prompt_template', {}).items()]),
        'dataset_size': dataset_size
    }

def generate_readme_table(base_path):
    """Generate a Markdown table for README based on config.yaml files in each directory, sorted and with dataset size."""
    headers = ['Index', 'Task Name', 'Version', 'Construction', 'Arxiv Link', 'License', 'Dataset Size']
    table_data = [headers]
    
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    sorted_directories = sorted(directories)  # Sort directories alphabetically
    
    for index, item in enumerate(sorted_directories, start=1):
        dir_path = os.path.join(base_path, item)
        config_path = os.path.join(dir_path, 'config.yaml')
        test_jsonl_path = os.path.join(dir_path, 'test.jsonl')
        if os.path.exists(config_path):
            config_data = extract_data_from_config(config_path, test_jsonl_path)
            table_data.append([
                str(index),
                config_data['task_name'],
                config_data['version'],
                config_data['construction'],
                config_data['arxiv'],
                config_data['license'],
                str(config_data['dataset_size'])
            ])
    
    return generate_markdown_table(table_data)

def generate_markdown_table(data):
    """Convert a list of lists into a Markdown table, with escaping for special characters."""
    markdown = ['|' + '|'.join(data[0]) + '|', '|' + '|'.join(['---'] * len(data[0])) + '|']
    for row in data[1:]:
        sanitized_row = [str(cell).replace('|', '\\|') for cell in row]
        markdown.append('|' + '|'.join(sanitized_row) + '|')
    return '\n'.join(markdown)

def write_readme(base_path, readme_content):
    """Write README content to a file."""
    readme_path = 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

# Example usage
base_path = 'db/'  # Adjust this path to your base directory
readme_table = generate_readme_table(base_path)
write_readme(base_path, readme_table)
print("README.md has been generated with the table of config.yaml files including dataset size.")
