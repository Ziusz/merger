# Ziusz/merger

A command-line tool to merge multiple source files from a directory into a single file, with a primary focus on Solidity contracts.

## Installation

1.  Clone the repository or download the `merger.py` script.
2.  No external libraries are needed, so you only need Python 3.

## Usage

The script is run from the command line and accepts several arguments to customize its behavior.

```bash
python merger.py <src_dir> <output_file> [options]
```

### Arguments

-   `src_dir`: The source directory to scan for files.
-   `output_file`: The path to the single output file that will be created.

### Options

-   `-e, --extensions`: A list of file extensions to include. Defaults to `sol`.
-   `--exclude`: A list of additional directory names to exclude from the scan.

### Examples

**1. Merge Solidity Contracts**

This is the default and most common use case. It will scan the `src/` directory for all `.sol` files and merge them into `merged.sol`.

```bash
python merger.py src/ merged.sol
```

**2. Merge TypeScript Files**

Merge all `.ts` and `.tsx` files from the `src/` directory into a single `merged.ts` file.

```bash
python merger.py src/ merged.ts -e ts tsx
```

**3. Merge Multiple File Types**

Scan the current directory (`.`) for Python (`.py`), JavaScript (`.js`), TypeScript (`.ts`), and Solidity (`.sol`) files, and output them to `all_code.txt`.

```bash
python merger.py . all_code.txt -e py js ts sol
```

**4. Exclude Additional Directories**

Merge Solidity contracts from the `src/` directory, but exclude the `test` and `mocks` subdirectories from the process.

```bash
python merger.py src/ output.sol --exclude test mocks
```