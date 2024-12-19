import re

def remove_links(text):
    # Regular expression to match most URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    # Remove all URLs from the text
    text_without_links = re.sub(url_pattern, '', text)
    
    return text_without_links

def remove_links_from_file(input_file, output_file):
    # Read the content of the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        document_text = file.read()

    # Remove links from the document text
    cleaned_text = remove_links(document_text)
    
    # Write the cleaned content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
    
    print(f"Links removed and saved to {output_file}")

# Example Usage
input_file = 'C:\\Users\\nwoke\\Documents\\MS\\proof\\templates\\aolp.html'  # Replace with your input file path
output_file = 'C:\\Users\\nwoke\\Documents\\MS\\proof\\templates\\aolp1.html'  # Replace with your desired output file path

remove_links_from_file(input_file, output_file)
