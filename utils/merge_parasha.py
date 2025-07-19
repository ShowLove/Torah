import json
import sys

def merge_parasha_files(parasha_names_file, parashot_details_file, output_file):
    # Load the ParashaNames data
    with open(parasha_names_file, 'r', encoding='utf-8') as f:
        parasha_data = json.load(f)

    # Load the Parashot data with Start and End info
    with open(parashot_details_file, 'r', encoding='utf-8') as f:
        parashot_details = json.load(f)

    # Create a dictionary for quick lookup of start/end by Name
    start_end_map = {p['Name']: {'Start': p['Start'], 'End': p['End']} for p in parashot_details['Parashot']}

    # Add Start and End info to ParashaNames entries
    for parasha in parasha_data['ParashaNames']:
        name = parasha['standard']
        if name in start_end_map:
            parasha['Start'] = start_end_map[name]['Start']
            parasha['End'] = start_end_map[name]['End']
        else:
            print(f"Warning: No start/end found for {name}")

    # Save the enriched data back to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parasha_data, f, indent=2, ensure_ascii=False)

    print(f"Merge complete! Output saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_parasha.py <parasha_names_file> <parashot_details_file> <output_file>")
        sys.exit(1)

    parasha_names_file = sys.argv[1]
    parashot_details_file = sys.argv[2]
    output_file = sys.argv[3]

    merge_parasha_files(parasha_names_file, parashot_details_file, output_file)
