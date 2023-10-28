from usp.tree import sitemap_tree_for_homepage
import re

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)

# Get user input
homepage_url = input("Enter the homepage URL: ")
incl_str = input("Enter the string to include (optional): ")
excl_str = input("Enter the string to exclude (optional): ")

# Fetch sitemap
tree = sitemap_tree_for_homepage(homepage_url)
filtered_urls = []

# Loop through all pages in the sitemap
for page in tree.all_pages():
    url = page.url
    if incl_str and excl_str:
        if incl_str in url and excl_str not in url:
            filtered_urls.append(url)
    elif incl_str:
        if incl_str in url:
            filtered_urls.append(url)
    elif excl_str:
        if excl_str not in url:
            filtered_urls.append(url)
    else:
        filtered_urls.append(url)

# Create filename
filename_parts = [sanitize_filename(homepage_url)]
if incl_str:
    filename_parts.append(f"_incl-{sanitize_filename(incl_str)}")
if excl_str:
    filename_parts.append(f"_excl-{sanitize_filename(excl_str)}")
filename = ''.join(filename_parts) + '.txt'

# Write to file
with open(filename, 'w') as f:
    for url in filtered_urls:
        f.write(url + '\n')

print(f"URLs written to {filename}")
