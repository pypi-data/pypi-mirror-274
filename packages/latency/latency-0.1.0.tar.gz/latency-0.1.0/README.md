# Onetick latency simulation library

## Overview

This library has various fonctionnality such a latency simulator as well as a query script for querying nbbo data from 
OneTick software. 

## Installation and requirements

This library requires OneTick software installed.

- [ ] pip install the wheel for this package
- [ ] pip install the requirements for this package


## Latency Module
The Latency module is designed to simulate network latency based on trading volumes and activity. It adjusts DataFrame timestamps to mimic realistic network delays by applying generated latency values drawn from a Gaussian normal distribution.

### Key Features:

- Flexible parameter inputs including date range (format: "yyyy-mm-dd") , symbol, batch size, and timezone.
- Configurable min/max latency values to reflect observed extremes.
- Mean and standard deviation settings for latency mirroring observed data characteristics.
- Jitter factor to simulate real-life network behavior.
- Options to plot latency distributions and trading volume over time.
- Metrics display for simulation analysis.

## Timestamp Crossover Module
This module detects timestamp anomalies where entries are out of chronological order—a common issue in high-frequency trading data that can lead to significant analytical errors.

### Functionality:

- Identifies and reports rows where timestamps are not sequential.
- Provides detailed reports of timestamp crossover incidents to aid in data cleansing.

## Volume Analyser Module
The Volume Analyser module evaluates trading volumes over specified intervals to identify periods of high activity. This analysis is crucial for adjusting latency in the simulation model to reflect real-world conditions.

### Capabilities:

- Calculates and analyzes trade counts over rolling time windows.
- Identifies high activity periods using percentile-based thresholds.
- Visualizes trading activity to assist in understanding market dynamics.


## NBBO Query Module
This module facilitates efficient querying of NBBO (National Best Bid and Offer) data through the OneTick platform, providing crucial market data for further analysis.

### Utilization:

- Streamlines the data retrieval process for NBBO queries.
- Supports extensive customization of query parameters to target specific data needs.
- Efficiently handles large datasets, ensuring timely processing and analysis.




