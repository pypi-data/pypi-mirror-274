import os
import hashlib
import base64
from datetime import datetime, timedelta
import argparse
from pathlib import Path
from contextlib import contextmanager
import binascii
import itertools
from dataclasses import dataclass
import uuid
import shutil

from loguru import logger
import magic
import polars as pl
from tqdm import tqdm

BIG_FILE_SIZE_THRESHOLD_BYTES = 512 * 1024  # 512 KiB
ENABLE_STORING_LAST_100_BYTES = False
DATETIME_FORMAT_FILES = "%Y-%m-%d_%H-%M-%SZ"

indexing_start_timestamp = datetime.utcnow()


@contextmanager
def add_time_taken(time_taken_store: dict[str, timedelta], key_name: str):
    start_time = datetime.utcnow()
    try:
        yield
    finally:
        end_time = datetime.utcnow()
        elapsed: timedelta = end_time - start_time
        if key_name in time_taken_store.keys():
            time_taken_store[key_name] += elapsed
        else:
            time_taken_store[key_name] = elapsed


@dataclass
class CrawlerProgressStoreSingleton:
    total_file_count: int = 0
    failed_file_count: int = 0
    link_file_count: int = 0
    notfile_file_count: int = 0
    success_file_count: int = 0
    parquet_saved_count: int = 0

    @property
    def files_per_sec(self) -> float:
        real_total_time_taken = datetime.utcnow() - indexing_start_timestamp
        files_per_sec = (
            self.total_file_count / (real_total_time_taken).total_seconds()
        )
        return files_per_sec

    def make_progress_string(self) -> str:
        return " ".join(
            [
                f"{self.total_file_count:,} files processed @ {self.files_per_sec:.2f} files/sec.",  # noqa
                f"{self.failed_file_count:,} failed ({self.failed_file_count/self.total_file_count:.2%}).",  # noqa
                f"{self.parquet_saved_count:,} parquets saved.",
                f"{self.link_file_count:,} links skipped.",
                f"{self.notfile_file_count:,} notfiles skipped (e.g., named pipes).",  # noqa
                f"{self.success_file_count:,} successful files indexed.",
            ]
        )


def run_file_indexer(
    input_folder: Path, output_folder: Path, strip_prefix: bool = False
) -> None:
    unwritten_file_data = []

    logger.info(f"Crawling {input_folder}...")

    progress = CrawlerProgressStoreSingleton()
    last_progress_log = datetime.utcnow()
    time_taken_log: dict[str, timedelta] = {}

    logger.info(
        "Pre-counting the total number of files... (press Ctrl-C to abort "
        "this pre-count and move on)"
    )
    with add_time_taken(time_taken_log, "precrawl_file_count"):
        file_counts_in_folders: list[int] = []
        try:
            for _, _, files in os.walk(input_folder):
                file_counts_in_folders.append(len(files))
        except KeyboardInterrupt:
            total_precrawl_file_count = sum(file_counts_in_folders)
            total_precrawl_file_count_is_accurate = False
            logger.error(
                "Keyboard interrupt. Exiting pre-crawling file count loop."
            )
            logger.info(
                "Before Keyboard interrupt, already counted "
                f"{total_precrawl_file_count:,} files."
            )
        else:
            total_precrawl_file_count = sum(file_counts_in_folders)
            total_precrawl_file_count_is_accurate = True
            logger.info(
                "Finished pre-counting the total number of files: "
                f"{total_precrawl_file_count:,} files."
            )

    # Create a generator to go through all files in all subdirectories
    all_files_iter = itertools.chain.from_iterable(
        ((Path(folder_path) / file_name) for file_name in files)
        for folder_path, dirs, files in os.walk(input_folder)
    )

    logger.info("Starting main crawler loop...")

    # Walk through the directory
    tqdm_desc = "Crawling and indexing"
    if not total_precrawl_file_count_is_accurate:
        tqdm_desc += " [note: will take longer than ETA]"
    tqdm_average_over_files = 1000  # average over this many files

    for file_path in tqdm(
        all_files_iter,
        desc=tqdm_desc,
        unit=" files",
        total=total_precrawl_file_count,
        smoothing=(1 / tqdm_average_over_files),
    ):
        progress.total_file_count += 1

        # if it's a link, skip it
        if os.path.islink(file_path):
            progress.link_file_count += 1
            continue

        # if it's a thing like a named pipe, skip it
        if not os.path.isfile(file_path):
            progress.notfile_file_count += 1
            continue

        try:
            file_data: dict = get_file_info(
                file_path=file_path, time_taken_log=time_taken_log
            )
            unwritten_file_data.append(file_data)
        except KeyboardInterrupt:
            logger.error("Keyboard interrupt. Exiting loop.")
            logger.info(
                f"Before Keyboard interrupt, was working on {file_path=}"
            )
            break
        except PermissionError:
            logger.warning(
                "Permission error. This should never happen! Skipping "
                f"{file_path=}"
            )
            progress.failed_file_count += 1
            continue
        except Exception as e:
            progress.failed_file_count += 1
            # if fail_count % 100 == 0:
            logger.debug(
                f"Failed {progress.failed_file_count:,}/{progress.total_file_count:,} to get file properties (error: {e}). Example: {file_path}"  # noqa
            )
            continue

        with add_time_taken(time_taken_log, "progress_log"):
            if (datetime.utcnow() - last_progress_log) > timedelta(minutes=1):
                logger.debug(
                    "PROGRESS REPORT:"
                )  # get on a new line from the tqdm bar
                real_total_time_taken = (
                    datetime.utcnow() - indexing_start_timestamp
                )

                logger.info(f"PROGRESS: {progress.make_progress_string()}")

                df_time_taken = pl.DataFrame(
                    [
                        {
                            "action": k,
                            "time_taken_sec": v.total_seconds(),
                            "time_taken_str": str(v),
                        }
                        for k, v in time_taken_log.items()
                    ]
                ).sort("time_taken_sec", descending=True)
                total_accounted_time_sec = df_time_taken[
                    "time_taken_sec"
                ].sum()
                df_time_taken = df_time_taken.with_columns(
                    percent_of_accounted=pl.col("time_taken_sec")
                    / pl.lit(total_accounted_time_sec)
                    * pl.lit(100),
                    percent_of_real=pl.col("time_taken_sec")
                    / pl.lit(real_total_time_taken.total_seconds())
                    * pl.lit(100),
                    milliseconds_per_file=pl.col("time_taken_sec")
                    / pl.lit(progress.total_file_count)
                    * pl.lit(1000),
                )
                total_accounted_time = timedelta(
                    seconds=total_accounted_time_sec
                )
                unaccounted_time = real_total_time_taken - total_accounted_time
                logger.info(
                    f"TIME TAKEN: {df_time_taken}\n"
                    f"Note: Total accounted time: {total_accounted_time}. "
                    f"Total real time: {real_total_time_taken}. "
                    f"Unaccounted time: {unaccounted_time} "
                    f"({unaccounted_time/real_total_time_taken:.2%})."
                )

                last_progress_log = datetime.utcnow()

        # Save the file data to a Parquet file
        with add_time_taken(time_taken_log, "save_to_parquet"):
            if len(unwritten_file_data) % 10000 == 0:
                progress.parquet_saved_count += 1
                save_to_parquet(
                    unwritten_file_data,
                    output_folder,
                    input_folder,
                    strip_prefix,
                )
                unwritten_file_data = []

        progress.success_file_count += 1

    logger.info("Reached end of looping through all files!")

    if len(unwritten_file_data) > 0:
        save_to_parquet(
            unwritten_file_data, output_folder, input_folder, strip_prefix
        )
    else:
        logger.info(f"No files found in {input_folder}.")

    logger.info("Done.")


def get_file_info(
    file_path: Path, time_taken_log: dict[str, timedelta]
) -> dict:

    with add_time_taken(time_taken_log, "stat_file"):
        # Getting file properties
        stat_info = os.stat(file_path)

    with add_time_taken(time_taken_log, "extract_file_info"):
        file_size = stat_info.st_size
        date_created = datetime.fromtimestamp(stat_info.st_ctime)
        date_modified = datetime.fromtimestamp(stat_info.st_mtime)
        # date_accessed = datetime.fromtimestamp(stat_info.st_atime)

    # Read the file's first and last 100 bytes
    with add_time_taken(time_taken_log, "read_first_last_100_bytes"):
        first_100_bytes = last_100_bytes = None
        magic_file_type_1 = None
        try:
            with open(file_path, "rb") as f:
                first_100_bytes = f.read(100)

                if ENABLE_STORING_LAST_100_BYTES:
                    if (file_size > 100) and (
                        file_size < BIG_FILE_SIZE_THRESHOLD_BYTES
                    ):
                        f.seek(-100, os.SEEK_END)
                    last_100_bytes = f.read(100)
        except Exception:
            # If there's an error reading the file, just ignore
            pass

    with add_time_taken(time_taken_log, "construct_magic_worker"):
        magic_worker = magic.Magic()

    if first_100_bytes:
        with add_time_taken(
            time_taken_log, "magic_file_type_1_from_100_bytes"
        ):
            magic_file_type_1 = magic_worker.from_buffer(first_100_bytes)
    if not magic_file_type_1:
        with add_time_taken(time_taken_log, "magic_file_type_1_from_file"):
            try:
                magic_file_type_1 = magic_worker.from_file(file_path)
            except Exception:
                # If there's an error loading the magic file type, just ignore
                pass

    # SHA256 hash, if file size < 100 KiB
    with add_time_taken(time_taken_log, "sha256_hash_1"):
        sha256_base64 = None
        if file_size < BIG_FILE_SIZE_THRESHOLD_BYTES:
            with open(file_path, "rb") as f:
                sha256_hash = hashlib.sha256(f.read()).digest()
                sha256_base64 = base64.b64encode(sha256_hash).decode("utf-8")

    with add_time_taken(time_taken_log, "md5_hash_hex_1"):
        md5_hash_hex = None
        if file_size < BIG_FILE_SIZE_THRESHOLD_BYTES:
            with open(file_path, "rb") as f:
                md5_hash = hashlib.md5(f.read()).digest()
                md5_hash_hex = binascii.hexlify(md5_hash).decode("utf-8")

    # Append file information to the list
    with add_time_taken(time_taken_log, "append_to_list"):
        file_info = {
            "file_path": str(file_path),
            "folder_path": str(file_path.parent),
            "file_name": str(file_path.name),
            "file_size_bytes": file_size,
            "md5_hex": md5_hash_hex,
            "sha256_base64": sha256_base64,
            "date_created": date_created,
            "date_modified": date_modified,
            # "date_accessed": date_accessed,
            "magic_file_type_1": magic_file_type_1,
            "first_100_bytes": first_100_bytes,
            "last_100_bytes": last_100_bytes,
            "timestamp_crawled": datetime.utcnow(),
            "indexing_start_timestamp": indexing_start_timestamp,
        }
    return file_info


def save_to_parquet(
    file_data: list[dict],
    output_folder: Path,
    input_folder: Path,
    strip_prefix: bool = False,
):
    # Create a DataFrame from the file data
    df = pl.DataFrame(
        file_data,
        schema={
            "file_path": pl.String,
            "folder_path": pl.String,
            "file_name": pl.String,
            "file_size_bytes": pl.UInt64,
            "sha256_base64": pl.String,
            "date_created": pl.Datetime,
            "date_modified": pl.Datetime,
            "date_accessed": pl.Datetime,
            "magic_file_type_1": pl.String,
            "first_100_bytes": pl.Binary,
            "last_100_bytes": pl.Binary,
            "timestamp_crawled": pl.Datetime,
            "indexing_start_timestamp": pl.Datetime,
        },
    )

    input_folder_str = str(input_folder).rstrip("/").rstrip("\\")

    if strip_prefix:
        df = df.with_columns(
            [
                pl.when(pl.col(col).str.starts_with(input_folder_str))
                .then(pl.col(col).str.slice(len(input_folder_str) + 1))
                .otherwise(pl.col(col))
                for col in ["file_path", "folder_path"]
            ]
        )

    output_parquet_file = output_folder / (
        "partial_file_index_"
        f"{datetime.utcnow().strftime(DATETIME_FORMAT_FILES)}.parquet"
    )
    logger.info(f"Saving {len(file_data):,} rows to {output_parquet_file}")

    # Save the DataFrame to a Parquet file
    df.write_parquet(
        output_parquet_file,
        compression="zstd",  # "good compression performance"
        compression_level=22,  # 22 is the smallest files for zstd
    )


def merge_parquets(input_folder: Path, output_parquet_file: Path):
    file_list = list(input_folder.glob("partial_file_index_*.parquet"))
    logger.info(
        f"Union-ing {len(file_list):,} parquet files in {input_folder} into "
        f"{output_parquet_file}."
    )

    scanned_dfs = []
    for file in file_list:
        scanned_dfs.append(pl.scan_parquet(file))

    df = pl.concat(scanned_dfs)
    df.sink_parquet(
        output_parquet_file, compression="zstd", compression_level=22
    )
    logger.info("Union-ed all files into a single Parquet file.")

    parquet_file_size_bytes = output_parquet_file.stat().st_size
    total_file_count_in_parquet = (
        pl.scan_parquet(output_parquet_file).select(pl.len()).collect().item()
    )
    logger.info(
        f"Total file count after union: {total_file_count_in_parquet:,} files."
        f"Parquet file size: {parquet_file_size_bytes:,} bytes = "
        f"{parquet_file_size_bytes / 1024 / 1024:.2f} MiB."
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="List the files in a directory and store the data as "
        "an index into a Parquet file."
    )

    parser.add_argument(
        "-i",
        "--input-folder",
        required=True,
        type=str,
        help="Path to the folder to read files from",
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        required=True,
        type=str,
        help="Path to the output folder where the Parquet file(s) will be stored",  # noqa
    )
    parser.add_argument(
        "-s",
        "--strip-prefix",
        action="store_true",
        help="If set, removes the input folder prefix from the file paths, as "
        "they get saved to the Parquet file (thus making them relative paths,"
        " relative to the input folder). Otherwise, absolute paths are used.",
    )

    args = parser.parse_args()
    return args


def main_cli():
    logger.info("Starting file crawler...")

    args = parse_arguments()

    input_folder = Path(args.input_folder)
    output_folder = Path(args.output_folder)

    log_file_path = output_folder / (
        "file_crawler_"
        f"{indexing_start_timestamp.strftime(DATETIME_FORMAT_FILES)}.log"
    )
    logger.add(log_file_path)

    logger.info(f"Started logging to log file: {log_file_path}")
    logger.info(f"Execution start timestamp: {indexing_start_timestamp=}")
    logger.info(f"Input folder: {args.input_folder}")
    logger.info(f"Output folder: {args.output_folder}")
    logger.info(f"Strip prefix?: {args.strip_prefix}")

    if not output_folder.exists():
        output_folder.mkdir(parents=True)
        logger.info(f"Created output folder: {output_folder}")

    if not input_folder.exists():
        raise ValueError(f"Input folder does not exist: {input_folder}")

    (
        partial_storage_folder := (
            output_folder / f"file_indexer_partial_storage_{uuid.uuid4()}"
        )
    ).mkdir()
    logger.info(f"Created partial storage folder: {partial_storage_folder}")

    run_file_indexer(
        input_folder=input_folder,
        output_folder=partial_storage_folder,
        strip_prefix=args.strip_prefix,
    )

    merge_parquets(
        input_folder=partial_storage_folder,
        output_parquet_file=output_folder / "00_complete_file_index.parquet",
    )

    shutil.rmtree(partial_storage_folder)

    logger.info("Done.")


if __name__ == "__main__":
    main_cli()
