# Dataset

This project uses a public supermarket sales dataset containing 1,000 transactions from three supermarket branches.

The dataset covers sales from January through March 2019.

The source includes fields such as:

- invoice ID
- branch
- city
- customer type
- gender
- product line
- unit price
- quantity
- tax
- total
- sale date
- sale time
- payment method
- cost of goods sold
- gross income
- rating

The original column names were converted to `snake_case` before ingestion.

The source dataset and generated CSV batches are intentionally not committed to this repository.

`python/create_test_batches.py` can be used locally to split the cleaned source file into an initial batch and a later incremental batch for pipeline testing.