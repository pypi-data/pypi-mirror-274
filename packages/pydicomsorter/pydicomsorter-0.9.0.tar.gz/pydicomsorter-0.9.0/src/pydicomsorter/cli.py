"""Main module of the package."""

import pathlib

import rich_click as click
from rich import print

from pydicomsorter.dicomsort import DICOMSorter
from pydicomsorter.io import find_dicom_files

click.rich_click.OPTION_GROUPS = {
    "dicomsort": [
        {
            "name": "Advanced options",
            "options": ["--delete_source", "--keep_going", "--symlink", "--dry_run"],
        },
        {
            "name": "Basic options",
            "options": ["--verbose", "--debug", "--help"],
        },
    ]
}


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument(
    "sourcedir",
    type=click.Path(
        exists=True,
        path_type=pathlib.Path,
        resolve_path=True,
        file_okay=False,
    ),
)
@click.argument(
    "destination_dir",
    type=str,
)
@click.option(
    "-d",
    "--delete_source",
    is_flag=True,
    help="Delete the source files after sorting.",
)
@click.option(
    "-k",
    "--keep_going",
    is_flag=True,
    help="Keep going when an error occurs.",
)
@click.option(
    "-s",
    "--symlink",
    is_flag=True,
    help="Create symbolic links instead of moving files.",
)
@click.option(
    "-n",
    "--dry_run",
    is_flag=True,
    help="Do not move or copy files, just print what would be done.",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Print verbose output.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Print debug output.",
)
def main(
    sourcedir: pathlib.Path,
    destination_dir: str,
    delete_source: bool,
    keep_going: bool,
    symlink: bool,
    dry_run: bool,
    verbose: bool,
    debug: bool,
) -> None:
    """Main function of the package.

    pixi run dicomsort data data/test/%PatientID/%StudyInstanceUID-%Modality/%InstanceNumber.dcm
    """
    import asyncio

    asyncio.run(
        _main(
            sourcedir,
            destination_dir,
            delete_source,
            keep_going,
            symlink,
            dry_run,
            verbose,
            debug,
        )
    )


async def _main(
    sourcedir: pathlib.Path,
    destination_dir: str,
    delete_source: bool,
    keep_going: bool,
    symlink: bool,
    dry_run: bool,
    verbose: bool,
    debug: bool,
) -> None:
    """Main function of the package.

    pixi run dicomsort data data/test/%PatientID/%StudyInstanceUID-%Modality/%InstanceNumber.dcm
    """
    # run find_dicom_files asynchronously
    files = await find_dicom_files(sourcedir)
    print(f"Found {len(files)} DICOM files.")
    # other code here
    sorter = DICOMSorter(destination_dir=destination_dir).validate_keys()

    print(f"Keys to use: {sorter.keys}")
