# analyze_deps.py
import json
from collections import defaultdict

def calculate_metrics(json_file):
    """Calculates Fan-in and Fan-out for each module from pydeps JSON."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file}'.")
        return None

    metrics = {}
    # Calculate Fan-out (imports) and initialize Fan-in count
    for module_name, details in data.items():
        # Skip internal/pseudo modules if needed, though pydeps usually handles this
        if not details or 'name' not in details:
            continue
            
        fan_out = len(details.get("imports", []))
        # Use the actual module name from the 'name' field
        metrics[details['name']] = {"fan_out": fan_out, "fan_in": 0} # Initialize fan_in

    # Calculate Fan-in (imported_by)
    for module_name, details in data.items():
         if not details or 'name' not in details:
            continue
            
         # Who imports this module? Add to their fan_in count.
         importers = details.get("imported_by", [])
         current_module_name = details['name']
         
         # Need to handle potential inconsistencies if a module name in 'imported_by'
         # doesn't exist as a primary key in the data dictionary. This can happen
         # with external dependencies or how pydeps structures things sometimes.
         # We directly count the length of the 'imported_by' list provided by pydeps.
         if current_module_name in metrics:
             metrics[current_module_name]["fan_in"] = len(importers)

    return metrics

def print_metrics(metrics, sort_by='fan_in', top_n=20):
    """Prints the calculated metrics, sorted."""
    if not metrics:
        return

    if sort_by not in ['fan_in', 'fan_out', 'name']:
        sort_by = 'fan_in' # Default sort

    # Sort items
    if sort_by == 'name':
        sorted_items = sorted(metrics.items())
    else:
         # Sort by the chosen metric (descending), then by name (ascending)
        sorted_items = sorted(metrics.items(), key=lambda item: (-item[1][sort_by], item[0]))

    print(f"\n--- Top {top_n} Modules Sorted by {sort_by.replace('_', '-').capitalize()} (Descending) ---")
    print(f"{'Module':<50} {'Fan-In':<10} {'Fan-Out':<10}")
    print("-" * 70)

    for i, (module, data) in enumerate(sorted_items):
        if i >= top_n:
            break
        print(f"{module:<50} {data['fan_in']:<10} {data['fan_out']:<10}")

if __name__ == "__main__":
    json_filename = "fastapi.json" # Make sure this matches your file name
    module_metrics = calculate_metrics(json_filename)

    if module_metrics:
         # Print top modules by Fan-in
         print_metrics(module_metrics, sort_by='fan_in', top_n=20)
         
         # Print top modules by Fan-out
         print_metrics(module_metrics, sort_by='fan_out', top_n=20)
