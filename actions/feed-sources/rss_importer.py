#!/usr/bin/env python3
import feedparser
import json
import os
import sys
from datetime import datetime
from dateutil import parser

def main():
    # Get inputs from environment variables
    feeds_input = os.environ.get('FEEDS_INPUT', '')
    output_folder = os.environ.get('OUTPUT_FOLDER', 'rss_artifacts')
    
    # Parse feeds list
    feeds = [feed.strip() for feed in feeds_input.split('\n') if feed.strip()]
    
    print(f'Processing {len(feeds)} feeds...')
    
    for i, feed_url in enumerate(feeds):
        try:
            print(f'Processing feed {i+1}/{len(feeds)}: {feed_url}')
            
            # Parse the RSS feed
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                print(f'Warning: Feed {feed_url} has parsing issues')
            
            # Extract feed metadata
            feed_info = {
                'title': getattr(feed.feed, 'title', 'Unknown'),
                'link': getattr(feed.feed, 'link', ''),
                'description': getattr(feed.feed, 'description', ''),
                'last_updated': getattr(feed.feed, 'updated', ''),
                'source_url': feed_url,
                'processed_at': datetime.now().isoformat(),
                'items': []
            }
            
            # Process each item
            for item in feed.entries:
                # Parse publication date
                pub_date = None
                if hasattr(item, 'published'):
                    try:
                        pub_date = parser.parse(item.published).isoformat()
                    except:
                        pass
                elif hasattr(item, 'pubDate'):
                    try:
                        pub_date = parser.parse(item.pubDate).isoformat()
                    except:
                        pass
                
                item_data = {
                    'title': getattr(item, 'title', ''),
                    'link': getattr(item, 'link', ''),
                    'description': getattr(item, 'description', ''),
                    'content': getattr(item, 'content', [{}])[0].get('value', '') if hasattr(item, 'content') else '',
                    'published': pub_date,
                    'author': getattr(item, 'author', ''),
                    'guid': getattr(item, 'id', ''),
                    'categories': [cat.term for cat in item.get('tags', [])] if hasattr(item, 'tags') else []
                }
                
                feed_info['items'].append(item_data)
            
            # Save to JSON file
            filename = f'feed_{i+1}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            output_path = os.path.join(output_folder, filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(feed_info, f, indent=2, ensure_ascii=False)
            
            print(f'Successfully processed {len(feed_info["items"])} items from {feed_url}')
            print(f'Saved to: {output_path}')
            
        except Exception as e:
            print(f'Error processing feed {feed_url}: {str(e)}')
            continue
    
    print('RSS import completed!')

if __name__ == '__main__':
    main() 