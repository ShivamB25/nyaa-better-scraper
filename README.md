# nyaa-page-scraper

An application to scrape and extract download links from Nyaa, a popular torrent site. This tool is useful for automating the extraction of download links for various files, including torrents.

This scraper will search for the provided URL, extract the download links, and display them or save them to a file as specified.

# Features

- Extracts download links from the provided URL.
- Automatically extracts the base URL from the provided link.
- Option to filter links by specific file types (e.g., `.torrent`).
- Option to save the extracted links to a file.
- Handles pagination to extract links from multiple pages.
- Customizable User-Agent header for HTTP requests.
- Retry mechanism for fetching pages in case of failure.

# Requirements

- Python 3.0+
- `requests` and `beautifulsoup4` libraries (install via `pip`)

# Installation

1. Download `nyaascraper.py`.
2. Run `pip install -r requirements.txt`.

# Usage

Run the script from the command line with the required URL and optional arguments for file type and output file.

```
python nyaascraper.py <url> [-f <file_type>] [-o <output_file>]
```

## Arguments

- `url` (required): The URL to scrape.
- `-f`, `--file-type` (optional): Filter links by file type (e.g., `.torrent`).
- `-o`, `--output-file` (optional): Save links to a specified file.

## Examples

### Basic Usage

Extract and display download links from the provided URL:

```bash
python nyaascraper.py "https://nyaaaa.antidrive.shop/?f=1&c=3_1&q=digital+-ana+-weekly&p=2"
```

### Filter by File Type

Extract and display only `.torrent` links:

```bash
python nyaascraper.py "https://nyaaaa.antidrive.shop/?f=1&c=3_1&q=digital+-ana+-weekly&p=2" -f .torrent
```

### Save Links to a File

Extract links and save them to `links.txt`:

```bash
python nyaascraper.py "https://nyaaaa.antidrive.shop/?f=1&c=3_1&q=digital+-ana+-weekly&p=2" -o links.txt
```

### Combined Usage

Filter by file type and save the links to a file:

```bash
python nyaascraper.py "https://nyaaaa.antidrive.shop/?f=1&c=3_1&q=digital+-ana+-weekly&p=2" -f .torrent -o links.txt
```

# Additional Information

If the specified URL does not return any links, ensure the URL is correct and the page is accessible. Use the verbose logging to debug any issues.

This tool is a modified and enhanced version of an older scraper, designed to be more flexible and feature-rich.

# License

This project is licensed under the MIT License.
