# python-website-scraper

Scan a website's HTML for links to potentially interesting assets and paths.
Only scan websites you own or are authorized to assess.

## Usage

Install the required packages:

```bash
python -m pip install requests beautifulsoup4
```

Run a scan:

```bash
python app.py https://example.com
```

The scanner checks links for these built-in terms: `assets`, `uploads`, `js`,
`images`, `backup`, `s3`, `sitemap`, `zip`, `sql`, `login`, `admin`, `bug`,
`temp`, `ftp`, and `php`.

Add one or more custom terms with `--assets`:

```bash
python app.py https://example.com --assets staging internal-api
```

Custom terms are added to the built-in list. If a term is already in the list,
it is skipped.

To also export matches to a CSV file in the current directory:

```bash
python app.py https://example.com --export-to-csv
```

Use both options to export matches for a scan with custom terms:

```bash
python app.py https://example.com --assets staging internal-api --export-to-csv
```

The scanner checks link `href` and `src` values for the terms. Matching results
are saved to a CSV named for the site's hostname when `--export-to-csv` is
enabled and matches are found. The CSV includes the matching term, HTML tag,
and absolute URL.
