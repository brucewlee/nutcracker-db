import os
import yaml

def extract_data_from_config(config_path):
    """Extract specified data from a config.yaml file for the README table."""
    with open(config_path, encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    # Extract required fields with detailed sub-fields as necessary
    task_name = config_data.get('task_name', 'N/A')
    version = config_data.get('version', 'N/A')
    construction_class = config_data.get('construction', {}).get('class', 'N/A')
    construction_n_choices = config_data.get('construction', {}).get('n_choices', 'N/A')
    arxiv_link = config_data.get('arxiv', 'N/A')
    license_info = config_data.get('license', 'N/A')
    
    # Handling user_prompt_template as a string representation of the dict
    user_prompt_template = config_data.get('user_prompt_template', {})
    user_prompt_template_str = ", ".join([f"{k}: {v}" for k, v in user_prompt_template.items()])
    
    return {
        'task_name': task_name,
        'version': version,
        'construction': f"{construction_class}, {construction_n_choices}",
        'arxiv': arxiv_link,
        'license': license_info,
        'user_prompt_template': user_prompt_template_str
    }

def generate_readme_table(base_path):
    """Generate a Markdown table for README based on config.yaml files in each directory."""
    headers = ['Task Name', 'Version', 'Construction (Class, N choices)', 'Arxiv Link', 'License']
    table_data = [headers]
    
    for item in os.listdir(base_path):
        dir_path = os.path.join(base_path, item)
        if os.path.isdir(dir_path):
            config_path = os.path.join(dir_path, 'config.yaml')
            if os.path.exists(config_path):
                config_data = extract_data_from_config(config_path)
                table_data.append([
                    config_data['task_name'], 
                    config_data['version'],
                    config_data['construction'],
                    config_data['arxiv'],
                    config_data['license']
                ])
    
    # Convert table data to Markdown format
    markdown_table = generate_markdown_table(table_data)
    return markdown_table

def generate_markdown_table(data):
    """Convert a list of lists into a Markdown table."""
    markdown = []
    markdown.append('|' + '|'.join(data[0]) + '|')
    markdown.append('|' + '|'.join(['---'] * len(data[0])) + '|')
    for row in data[1:]:
        # Ensure each cell's data is converted to a string and sanitized for Markdown compatibility
        sanitized_row = [str(cell).replace('|', '\\|') for cell in row] 
        markdown.append('|' + '|'.join(sanitized_row) + '|')
    return '\n'.join(markdown)

def write_readme(base_path, readme_content):
    """Write README content to a file."""
    readme_path = os.path.join(base_path, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

# Example usage
base_path = '.'  # Adjust this path to your base directory
readme_table = generate_readme_table(base_path)
write_readme(base_path, readme_table)
print("README.md has been generated with the table of config.yaml files.")
