# file-indexer-py
A Python script to index a large folder into a parquet file, along with metadata

## Description

This script is useful for searching for files stored on a reasonably slow disk
from backups, especially in where you aren't sure about the files are are
searching for.

Use tools like DBeaver and DuckDB to query and explore the generated index.

## Usage

```bash
pip install file_indexer

python3 -m file_indexer -i /path/to/input/folder -o /path/to/output/folder
# --or--
file_indexer -i /path/to/input/folder -o /path/to/output/folder
```

## Metadata Indexed and Output

The output parquet files have the following columns:

    * file_path
    * folder_path
    * file_name
    * file_size_bytes
    * md5_hash_hex
    * sha256_base64
    * date_created
    * date_modified
    * date_accessed
    * magic_file_type_1
    * first_100_bytes
    * last_100_bytes
    * timestamp_crawled
    * indexing_start_timestamp

The parquet files are stored to the output folder with the following naming convention: `partial_file_index_{datetime}.parquet`

At the end of the execution, the individual parquet files are unioned into a single parquet file, with the following name: `00_complete_file_index.parquet`
