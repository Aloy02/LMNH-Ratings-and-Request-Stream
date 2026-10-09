# Museum Visitor Data Platform

A complete data platform for processing and visualising museum kiosk analytics. This project demonstrates end-to-end data engineering: from raw exhibition and visitor request data through ETL pipelines to real-time Tableau dashboards.

## What's Inside

- **Infrastructure** (`main.tf`, `variables.tf`) — AWS infrastructure managed with Terraform: VPC, subnets, and compute resources
- **Pipeline** (`pipeline/`) — ETL workflows that extract, validate, transform, and load exhibition and request data into a database
- **Dashboard** (`dashboard/`) — Real-time consumer that subscribes to Kafka topics and visualises data in Tableau
- **Raw Data** (`pipeline/raw_data/`) — Sample datasets: exhibition metadata and visitor request records

## Quick Start

```bash
# Deploy infrastructure
terraform init && terraform apply

# Run the data pipeline
cd pipeline && python pipeline.py

# Start the dashboard consumer
cd dashboard && pip install -r requirements.txt && python pipeline.py
```

Built with Python, Terraform, AWS, and Tableau.
