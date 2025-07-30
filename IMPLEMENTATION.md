# Gov Bot Builder - RSS Processing Implementation

This document describes the implementation of the RSS feed processing pipeline based on functional reactive programming principles.

## Architecture Overview

The implementation follows the architecture described in the README.md:

1. **Feed Sources**: Import data from RSS feeds and output standardized JSON artifacts
2. **Transformers**: Process and filter RSS data, publishing to artifact folders
3. **Side Effects**: Consume RSS artifacts to produce external effects (counting, notifications, etc.)

## Directory Structure

```
gov-bot-builder/
├── actions/feed-sources/
│   └── rss-importer.yml          # RSS feed importer action
├── actions/transformers/
│   └── date-filter.yml           # Date filtering transformer
├── actions/side-effects/
│   └── item-counter.yml          # Item counting side effect
├── .github/
│   ├── workflows/
│   │   └── simple-test.yml       # GitHub workflow for testing
│   ├── test-data/
│   │   ├── presidential-actions.rss
│   │   └── supereme-court-rulings.rss
│   └── README.md                 # Workflow documentation
├── requirements.txt
└── README.md
```

## Components

### 1. RSS Importer (`actions/feed-sources/rss-importer.yml`)

**Purpose**: Import RSS feeds from URLs or local files and convert them to standardized JSON artifacts.

**Inputs**:
- `feeds`: List of RSS feed URLs or file paths (one per line)
- `output_folder`: Output folder for RSS artifacts (default: 'rss_artifacts')

**Output**: JSON files containing standardized RSS feed data with the following structure:

```json
{
  "title": "Feed Title",
  "link": "Feed URL",
  "description": "Feed Description",
  "last_updated": "Last Update Time",
  "source_url": "Original Source URL",
  "processed_at": "Processing Timestamp",
  "items": [
    {
      "title": "Item Title",
      "link": "Item URL",
      "description": "Item Description",
      "content": "Full Content",
      "published": "Publication Date (ISO format)",
      "author": "Author",
      "guid": "Unique Identifier",
      "categories": ["Category1", "Category2"]
    }
  ]
}
```

**Features**:
- Handles both local RSS files and remote URLs
- Robust date parsing for various RSS date formats
- Error handling for malformed feeds
- Standardized output format for downstream processing

### 2. Date Filter (`actions/transformers/date-filter.yml`)

**Purpose**: Filter RSS items based on publication date using various comparison operators.

**Inputs**:
- `input_folder`: Input folder containing RSS artifacts (default: 'rss_artifacts')
- `output_folder`: Output folder for filtered artifacts (default: 'filtered_rss_artifacts')
- `op`: Date comparison operator (GTE, LTE, EQ, GT, LT)
- `date_filter`: Date to filter by (YYYY-MM-DD format)

**Output**: Filtered JSON files with additional metadata:

```json
{
  // ... original feed data ...
  "filtered_at": "Filtering Timestamp",
  "filter_operator": "GTE",
  "filter_date": "2025-07-01",
  "original_item_count": 10,
  "filtered_item_count": 5
}
```

**Features**:
- Multiple date comparison operators (GTE, LTE, EQ, GT, LT)
- Robust date parsing with fallback handling
- Preserves original feed metadata
- Adds filtering metadata for traceability

### 3. Item Counter (`actions/side-effects/item-counter.yml`)

**Purpose**: Count RSS items and output count data to files.

**Inputs**:
- `input_folder`: Input folder containing RSS artifacts (default: 'filtered_rss_artifacts')
- `output_folder`: Output folder for count artifacts (default: 'count_artifacts')

**Output**: Two files:
- `count.txt`: Simple text file with total item count
- `count.json`: Detailed count data with feed breakdown

```json
{
  "total_items": 15,
  "feed_count": 3,
  "feed_details": [
    {
      "filename": "feed_1_20250101_120000.json",
      "feed_title": "Presidential Actions",
      "item_count": 10,
      "source_url": "source_url"
    }
  ],
  "counted_at": "Counting Timestamp",
  "input_folder": "input_folder_path"
}
```

**Features**:
- Aggregates counts across multiple feeds
- Provides detailed breakdown by feed
- Simple text output for easy consumption
- JSON output for detailed analysis

## Usage Example

The GitHub workflow (`.github/workflows/simple-test.yml`) demonstrates the complete workflow and automatically tests the pipeline on pull requests and pushes to main branches.

```yaml
name: Simple RSS Pipeline Test

on:
  pull_request:
    branches: [ main, master ]
  push:
    branches: [ main, master ]

jobs:
  test-rss-pipeline:
    name: Test RSS Processing Pipeline
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Import Feeds
        id: import-feeds
        uses: ./actions/feed-sources/rss-importer.yml
        with:
          feeds: |
            ./.github/test-data/presidential-actions.rss
            ./.github/test-data/supereme-court-rulings.rss

      - name: Filter by date
        id: filter-date
        uses: ./actions/transformers/date-filter.yml
        with:
          input_folder: ${{ steps.import-feeds.outputs.output_folder }}
          op: GTE
          date_filter: "2025-07-01"

      - name: Count items
        id: count-items
        uses: ./actions/side-effects/item-counter.yml
        with:
          input_folder: ${{ steps.filter-date.outputs.output_folder }}
          output_folder: "windy_civi_rss_artifacts"

      - name: Validate basic output
        run: |
          echo "Validating RSS processing artifacts..."
          
          # Check if count file exists and has content
          if [ ! -f "windy_civi_rss_artifacts/count.txt" ]; then
            echo "❌ Error: count.txt file not found"
            exit 1
          fi
          
          count=$(cat windy_civi_rss_artifacts/count.txt)
          if [ -z "$count" ]; then
            echo "❌ Error: count.txt is empty"
            exit 1
          fi
          
          echo "✅ Found $count RSS items"
          echo "✅ Pipeline completed successfully!"
```

## Testing

### Local Testing

A test script (`test_implementation.py`) is provided to verify the implementation:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_implementation.py
```

### Automated Testing

GitHub workflows automatically test the pipeline:

- **`simple-test.yml`**: Basic test with essential validation

These workflows run automatically on:
- Pull requests to main/master branches
- Pushes to main/master branches
- Manual triggers from the Actions tab

See `.github/README.md` for detailed workflow documentation.

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_implementation.py
```

The test script:
1. Tests RSS import functionality
2. Tests date filtering with GTE operator
3. Tests item counting
4. Generates test output files in `test_output/` directory

## Dependencies

- `feedparser==6.0.10`: RSS/Atom feed parsing
- `requests==2.31.0`: HTTP requests for remote feeds
- `python-dateutil==2.8.2`: Date parsing and manipulation

## Functional Reactive Programming Principles

The implementation follows FRP principles:

1. **Data Flow**: RSS feeds → Import → Filter → Count → Output
2. **Composability**: Each action can be chained with any other action
3. **Standardized Artifacts**: All actions use consistent JSON format
4. **Side Effects**: Clear separation between data processing and side effects
5. **Reactivity**: Actions automatically process new data as it becomes available

## Extensibility

The architecture is designed for easy extension:

- **New Feed Sources**: Add new importers in `actions/feed-sources/`
- **New Transformers**: Add new processors in `actions/transformers/`
- **New Side Effects**: Add new outputs in `actions/side-effects/`

Each component follows the same pattern:
- Standardized input/output folders
- JSON artifact format
- Error handling and logging
- GitHub Actions integration 