from usp.tree import sitemap_tree_for_homepage
import re

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)

# Get user input
homepage_url = input("Enter the homepage URL: ")
incl_str = input("Enter the string to include (optional): ").lower()  # Convert to lowercase
excl_strs_input = input("Enter strings to exclude, separated by commas (optional): ").lower()  # Convert to lowercase

# Parse exclusion strings
excl_strs = excl_strs_input.split(",") if excl_strs_input else []

# Initialize counters
total_urls = 0
excluded_urls = 0
included_urls = 0
errors = 0

# Fetch sitemap
try:
    tree = sitemap_tree_for_homepage(homepage_url)
    filtered_urls = []

    for page in tree.all_pages():
        total_urls += 1
        url = page.url.lower()  # Convert to lowercase for case-insensitive comparison

        if any(excl_str in url for excl_str in excl_strs):
            excluded_urls += 1
            continue
        
        if incl_str and incl_str in url:
            filtered_urls.append(page.url)  # Use original case for output
            included_urls += 1
        elif not incl_str:
            filtered_urls.append(page.url)  # Use original case for output
            included_urls += 1

    # Create filename
    filename_parts = [sanitize_filename(homepage_url)]
    if incl_str:
        filename_parts.append(f"_incl-{sanitize_filename(incl_str)}")
    if excl_strs:
        filename_parts.append(f"_excl-{sanitize_filename('-'.join(excl_strs))}")
    filename = ''.join(filename_parts) + '.txt'

    # Write to file
    with open(filename, 'w') as f:
        for url in filtered_urls:
            f.write(url + '\n')

    # Output summary
    print(f"\n--- Summary ---")
    print(f"Homepage URL: {homepage_url}")
    print(f"Total URLs in Sitemap: {total_urls}")
    print(f"Total Included URLs: {included_urls}")
    print(f"Total Excluded URLs: {excluded_urls}")
    print(f"Total Errors: {errors}")
    print(f"URLs written to {filename}")

except Exception as e:
    errors += 1
    print(f"An error occurred: {e}")
