#!/usr/bin/env python3
import json
import os
import glob
from datetime import datetime

def main():
    # Get inputs from environment variables
    input_folder = os.environ.get('INPUT_FOLDER', 'filtered_rss_artifacts')
    output_folder = os.environ.get('OUTPUT_FOLDER', 'count_artifacts')
    
    print(f'Counting RSS items in {input_folder}')
    
    # Find all JSON files in input folder
    json_files = glob.glob(os.path.join(input_folder, '*.json'))
    
    if not json_files:
        print(f'No JSON files found in {input_folder}')
        # Create empty count file
        count_data = {
            'total_items': 0,
            'feed_count': 0,
            'counted_at': datetime.now().isoformat(),
            'input_folder': input_folder
        }
    else:
        total_items = 0
        feed_details = []
        
        for json_file in json_files:
            try:
                print(f'Processing {json_file}')
                
                with open(json_file, 'r', encoding='utf-8') as f:
                    feed_data = json.load(f)
                
                item_count = len(feed_data.get('items', []))
                total_items += item_count
                
                feed_detail = {
                    'filename': os.path.basename(json_file),
                    'feed_title': feed_data.get('title', 'Unknown'),
                    'item_count': item_count,
                    'source_url': feed_data.get('source_url', '')
                }
                feed_details.append(feed_detail)
                
                print(f'  {feed_data.get("title", "Unknown")}: {item_count} items')
                
            except Exception as e:
                print(f'Error processing {json_file}: {e}')
                continue
        
        count_data = {
            'total_items': total_items,
            'feed_count': len(json_files),
            'feed_details': feed_details,
            'counted_at': datetime.now().isoformat(),
            'input_folder': input_folder
        }
    
    # Save count data to JSON file
    count_json_path = os.path.join(output_folder, 'count.json')
    with open(count_json_path, 'w', encoding='utf-8') as f:
        json.dump(count_data, f, indent=2, ensure_ascii=False)
    
    # Save simple count to text file
    count_txt_path = os.path.join(output_folder, 'count.txt')
    with open(count_txt_path, 'w', encoding='utf-8') as f:
        f.write(str(count_data['total_items']))
    
    print(f'Count completed! Total items: {count_data["total_items"]}')
    print(f'Count saved to: {count_txt_path}')

if __name__ == '__main__':
    main() 