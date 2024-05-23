# pydicomsorter

[![codecov](https://codecov.io/gh/jjjermiah/PyDicomSorter/graph/badge.svg?token=tCcajRIGz9)](https://codecov.io/gh/jjjermiah/PyDicomSorter)
[![CI-CD](https://github.com/jjjermiah/PyDicomSorter/actions/workflows/main.yaml/badge.svg)](https://github.com/jjjermiah/PyDicomSorter/actions/workflows/main.yaml)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Built with Material for MkDocs](https://img.shields.io/badge/mkdocs--material-gray?logo=materialformkdocs)](https://github.com/squidfunk/mkdocs-material)

[![PyPI - Version](https://img.shields.io/pypi/v/PyDicomSorter)](https://pypi.org/project/pydicomsorter/)
[![PyPI - Format](https://img.shields.io/pypi/format/PyDicomSorter)](https://pypi.org/project/pydicomsorter/)
[![pixi-badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json&style=flat-square)](https://github.com/prefix-dev/pixi)

Testing the pydicom library to sort dicom files by patient name and study date.

Designing:

``` bash
Usage: dicomsort [OPTIONS] SOURCEDIR DESTINATION_DIR

╭─ Advanced options ───────────────────────────────────────────────────────────────╮
│ --delete_source  -d    Delete the source files after sorting.                    │
│ --keep_going     -k    Keep going when an error occurs.                          │
│ --symlink        -s    Create symbolic links instead of moving files.            │
│ --dry_run        -n    Do not move or copy files, just print what would be done. │
╰──────────────────────────────────────────────────────────────────────────────────╯
╭─ Basic options ──────────────────────────────────────────────────────────────────╮
│ --verbose        Print verbose output.                                           │
│ --debug          Print debug output.                                             │
│ --help     -h    Show this message and exit.                                     │
╰──────────────────────────────────────────────────────────────────────────────────╯
```

<!-- [![Anurag's GitHub stats](https://github-readme-stats.vercel.app/api?username=anuraghazra)](https://github.com/anuraghazra/github-readme-stats)

[![Anurag's GitHub stats](https://github-readme-stats.vercel.app/api?username=jjjermiah)](https://github.com/jjjermiah/github-readme-stats) -->

<!-- [![GitHub Trends SVG](https://api.githubtrends.io/user/svg/jjjermiah/langs)](https://githubtrends.io) -->
