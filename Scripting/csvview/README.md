
# csvview

**csvview** is a lightweight Python CLI tool that displays CSV data in a neatly formatted table. It supports automatic delimiter detection, column filtering, row slicing, and more — all without relying on Python’s built-in `csv` module.

---

## Features

- **Auto-detects CSV delimiter** (`comma`, `semicolon`, or `tab`)
- Display specific columns using column indices (1-based)
- Skip initial rows (`--skip-row`)
- Display only first or last `N` rows using `--head` or `--tail`
- Clean and aligned **tabular output**

---

## Usage

```bash
python csvview.py path/to/file.csv [OPTIONS]
```

### Required Argument

| Argument    | Description                 |
| ----------- | --------------------------- |
| `file`      | Path to the input CSV file. |

### Optional Arguments

| Option           | Description                                                                 |
| ---------------- | --------------------------------------------------------------------------- |
| `-d`, `--delimiter` | Manually specify the delimiter (default: auto-detect)                      |
| `--skip-row N`    | Skip the first `N` data rows (excluding the header)                         |
| `--head N`        | Display only the first `N` data rows                                        |
| `--tail N`        | Display only the last `N` data rows                                         |
| `-f`, `--columns` | Comma-separated **1-based** column indices to include in the output (e.g. `-f 1,3,5`) |

> Note: If both `--head` and `--tail` are used, only `--head` is applied.

---

## Examples

#### Display full CSV with auto-detected delimiter:

```bash
python csvview.py data.csv
```

#### Display only selected columns (e.g. 1st, 3rd, 5th):

```bash
python csvview.py data.csv -f 1,3,5
```

#### Skip first 2 rows and show top 5:

```bash
python csvview.py data.csv --skip-row 2 --head 5
```

#### Use semicolon as delimiter:

```bash
python csvview.py data.csv -d ';'
```

---

## Notes

- This script does **not** use Python’s `csv` module — parsing is done manually.
- Assumes the data can fit into memory (not ideal for massive files).
- Output is optimized for CLI readability.

---
