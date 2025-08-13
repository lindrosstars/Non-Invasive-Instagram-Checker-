import json
import os # Import the os module for path checking

def get_values_from_json(filepath):
    """
    Reads a JSON file and extracts all 'href' fields from 'string_list_data'
    into a set. Handles duplicates and provides efficient lookups.
    Normalizes URLs by stripping trailing slashes.
    This version handles both top-level list and top-level dictionary with 'relationships_following'.
    """
    values = set()
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}. Please check the path.")
        return values

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
            items_to_process = []
            if isinstance(data, list):
                # If the top-level is already a list (like followers_1.json)
                items_to_process = data
            elif isinstance(data, dict) and 'relationships_following' in data and isinstance(data['relationships_following'], list):
                # If the top-level is a dictionary with 'relationships_following' key (like following.json)
                items_to_process = data['relationships_following']
            else:
                print(f"Warning: Unexpected top-level JSON structure in {filepath}. Expected a list or a dictionary with 'relationships_following' key. Skipping extraction.")
                return values

            for i, item in enumerate(items_to_process):
                if not isinstance(item, dict):
                    print(f"Warning: Item at index {i} in {filepath} is not a dictionary. Skipping.")
                    continue

                if 'string_list_data' in item and isinstance(item['string_list_data'], list):
                    for j, sub_item in enumerate(item['string_list_data']):
                        if not isinstance(sub_item, dict):
                            print(f"Warning: Sub-item at index {j} within string_list_data of item {i} in {filepath} is not a dictionary. Skipping.")
                            continue
                        if 'href' in sub_item:
                            # Normalize the URL by stripping trailing slashes for consistent comparison
                            normalized_href = sub_item['href'].rstrip('/')
                            values.add(normalized_href)
                        else:
                            print(f"Warning: 'href' key not found in sub-item {j} of item {i} in {filepath}. Skipping.")
                else:
                    print(f"Warning: 'string_list_data' key (or it's not a list) not found in item {i} in {filepath}. Skipping.")

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}. Please check the file content.")
    except Exception as e:
        print(f"An unexpected error occurred while processing {filepath}: {e}")
    return values

def analyze_instagram_lists(followers_file, following_file, output_file):
    """
    Analyzes followers and following lists and writes the comparison to an output file.
    """
    print(f"Attempting to read followers data from: {followers_file}")
    followers = get_values_from_json(followers_file)
    print(f"Extracted {len(followers)} entries from {followers_file}")

    print(f"Attempting to read following data from: {following_file}")
    following = get_values_from_json(following_file)
    print(f"Extracted {len(following)} entries from {following_file}")

    if not followers and not following:
        print("No data extracted from either file. Exiting.")
        return

    # Find mutuals (intersection)
    mutuals = followers.intersection(following)

    # Find users you follow who don't follow you back (following - followers)
    # This means items in 'following' that are NOT in 'followers'
    not_following_back = following.difference(followers)

    # Find users who follow you that you don't follow back (followers - following)
    # This means items in 'followers' that are NOT in 'following'
    you_dont_follow_back = followers.difference(following)

    try:
        with open(output_file, 'w') as out_f:
            out_f.write("--- Instagram List Analysis ---\n\n")

            out_f.write("Users you follow who DO NOT follow you back:\n")
            if not_following_back:
                for user in sorted(list(not_following_back)):
                    out_f.write(f"- {user}\n")
            else:
                out_f.write("- None\n")
            out_f.write("\n")

            out_f.write("Users who follow you that you DO NOT follow back:\n")
            if you_dont_follow_back:
                for user in sorted(list(you_dont_follow_back)):
                    out_f.write(f"- {user}\n")
            else:
                out_f.write("- None\n")
            out_f.write("\n")

            out_f.write("Mutual followers (you follow each other):\n")
            if mutuals:
                for user in sorted(list(mutuals)):
                    out_f.write(f"- {user}\n")
            else:
                out_f.write("- None\n")
            out_f.write("\n")

        print(f"Analysis complete. Results saved to {output_file}")

    except IOError:
        print(f"Error: Could not write to output file {output_file}")

# --- Configuration ---
followers_file_path = 'followers_1.json'
following_file_path = 'following.json'
output_results_file = 'instagram_analysis.txt'

# --- Run the analysis ---
analyze_instagram_lists(followers_file_path, following_file_path, output_results_file)
