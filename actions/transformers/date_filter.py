#!/usr/bin/env python3
import json
import os
import glob
from datetime import datetime
from dateutil import parser

def main():
    # Get inputs from environment variables
    input_folder = os.environ.get('INPUT_FOLDER', 'rss_artifacts')
    output_folder = os.environ.get('OUTPUT_FOLDER', 'filtered_rss_artifacts')
    op = os.environ.get('OP', 'GTE')
    date_filter_str = os.environ.get('DATE_FILTER', '')
    
    # Parse the filter date
    try:
        filter_date = datetime.strptime(date_filter_str, '%Y-%m-%d').date()
    except ValueError:
        print(f'Error: Invalid date format. Expected YYYY-MM-DD, got {date_filter_str}')
        exit(1)
    
    print(f'Filtering RSS items with {op} {date_filter_str}')
    
    # Find all JSON files in input folder
    json_files = glob.glob(os.path.join(input_folder, '*.json'))
    
    if not json_files:
        print(f'No JSON files found in {input_folder}')
        exit(0)
    
    total_items = 0
    filtered_items = 0
    
    for json_file in json_files:
        try:
            print(f'Processing {json_file}')
            
            with open(json_file, 'r', encoding='utf-8') as f:
                feed_data = json.load(f)
            
            original_items = len(feed_data.get('items', []))
            total_items += original_items
            
            # Filter items based on publication date
            filtered_items_list = []
            
            for item in feed_data.get('items', []):
                item_date_str = item.get('published')
                
                if not item_date_str:
                    # Skip items without publication date
                    continue
                
                try:
                    # Parse item date
                    item_date = parser.parse(item_date_str).date()
                    
                    # Apply filter based on operator
                    include_item = False
                    
                    if op == 'GTE':  # Greater than or equal
                        include_item = item_date >= filter_date
                    elif op == 'LTE':  # Less than or equal
                        include_item = item_date <= filter_date
                    elif op == 'EQ':   # Equal
                        include_item = item_date == filter_date
                    elif op == 'GT':   # Greater than
                        include_item = item_date > filter_date
                    elif op == 'LT':   # Less than
                        include_item = item_date < filter_date
                    else:
                        print(f'Warning: Unknown operator {op}, skipping item')
                        continue
                    
                    if include_item:
                        filtered_items_list.append(item)
                        filtered_items += 1
                        
                except Exception as e:
                    print(f'Warning: Could not parse date {item_date_str}: {e}')
                    continue
            
            # Update feed data with filtered items
            feed_data['items'] = filtered_items_list
            feed_data['filtered_at'] = datetime.now().isoformat()
            feed_data['filter_operator'] = op
            feed_data['filter_date'] = date_filter_str
            feed_data['original_item_count'] = original_items
            feed_data['filtered_item_count'] = len(filtered_items_list)
            
            # Save filtered data to output folder
            filename = os.path.basename(json_file)
            output_path = os.path.join(output_folder, filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(feed_data, f, indent=2, ensure_ascii=False)
            
            print(f'  Original: {original_items} items, Filtered: {len(filtered_items_list)} items')
            
        except Exception as e:
            print(f'Error processing {json_file}: {e}')
            continue
    
    print(f'Date filtering completed!')
    print(f'Total items processed: {total_items}')
    print(f'Total items after filtering: {filtered_items}')

if __name__ == '__main__':
    main() 