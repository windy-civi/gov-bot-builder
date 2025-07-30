# GitHub Workflows

This directory contains GitHub Actions workflows that automatically test the RSS processing pipeline.

## Workflows

### `simple-test.yml` - RSS Pipeline Test

**Triggers**: 
- Pull requests to `main` or `master` branch
- Pushes to `main` or `master` branch

**What it does**:
1. **Import RSS Feeds**: Processes RSS files from `.github/test-data/`
2. **Filter by Date**: Filters items with publication date >= 2025-07-01
3. **Count Items**: Counts the filtered RSS items
4. **Basic Validation**: Simple validation of output files

**Validation includes**:
- ✅ Check if `count.txt` exists and has content
- ✅ Display item count

## How to Use

### Automatic Testing

These workflows run automatically when:
- You create a pull request
- You push changes to the main branch
- You manually trigger them from the Actions tab

### Manual Testing

You can also run these workflows manually:

1. Go to the **Actions** tab in your GitHub repository
2. Select the workflow you want to run
3. Click **Run workflow**
4. Choose the branch and click **Run workflow**

### Viewing Results

After a workflow runs:

1. **Check the logs**: Click on the workflow run to see detailed logs
2. **View summary**: The workflow will show a summary of processed items



## Troubleshooting

### Common Issues

1. **Workflow fails on import**: Check that RSS test files exist in `.github/test-data/`
2. **Validation fails**: Check that the pipeline is generating the expected output files
3. **Date filtering issues**: Verify that RSS items have valid publication dates

### Debugging

1. **Check logs**: Look at the detailed logs in the Actions tab
2. **Download artifacts**: Examine the generated files to understand what went wrong
3. **Test locally**: Use the test script to debug issues locally before pushing

## Customization

To modify the workflows:

1. **Change test files**: Update the `feeds` input in the workflow
2. **Modify date filter**: Change the `date_filter` and `op` parameters
3. **Add validation**: Extend the validation steps to check additional requirements
4. **Change triggers**: Modify the `on` section to trigger on different events 