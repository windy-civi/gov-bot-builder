# Gov Bot Builder - RSS Feed Processing Actions

A collection of GitHub Actions for ingesting RSS feeds, filtering/analyzing them, and publishing side effect artifacts, built on functional reactive programming principles.

## Overview

This repository contains a set of composable GitHub Actions that work together using a functional reactive programming approach:

1. **Feed Sources**: Import data from various sources and output standardized RSS artifacts
2. **Transformers**: Loop through each RSS file, transform and filter RSS data, and publish to artifact folder (windy-civi-pipeline-artifacts). These have standardized artifact input/ouputs so users don't need to worry about that part.
3. **Side Effects (Sinks)**: Consume RSS artifacts to produce external effects (publishing, notifications, etc.)

All actions use a standardized artifact format and can be chained together in any combination