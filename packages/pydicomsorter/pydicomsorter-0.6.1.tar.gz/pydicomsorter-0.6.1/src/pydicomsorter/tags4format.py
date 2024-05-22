"""Some functions to get DICOM tags from keywords."""

import tkinter as tk
from tkinter import ttk

import pydicom
from pydicom._dicom_dict import DicomDictionary
from pydicom.datadict import (
    dictionary_has_tag,
    tag_for_keyword,
)

# dictionary_description,
#     dictionary_is_retired,
#     dictionary_keyword,
#     dictionary_VR,
#     private_dictionary_description,
#     private_dictionary_VR,
#     repeater_has_tag,


def lookup_tag(keyword: str) -> str:
    """Returns the tag of a keyword."""
    return str(tag_for_keyword(keyword))


def tag_exists(keyword: str) -> bool:
    """Check if a tag exists for a keyword."""
    return dictionary_has_tag(keyword)


all_dicom_tags: list[str] = [
    item for key, value in DicomDictionary.items() for item in (value[2], value[4])
]


def build_tree(tree: ttk.Treeview, ds: pydicom.Dataset, parent: str | None = None) -> None:
    """Build out the tree.

    Parameters
    ----------
    tree : ttk.Treeview
        The treeview object.
    ds : pydicom.dataset.Dataset
        The dataset object to add to the `tree`.
    parent : str | None
        The item ID of the parent item in the tree (if any), default ``None``.
    """
    # For each DataElement in the current Dataset
    for idx, elem in enumerate(ds):
        tree_item = tree.insert('', tk.END, text=str(elem))
        if parent:
            tree.move(tree_item, parent, idx)

        if elem.VR == 'SQ':
            # DataElement is a sequence, containing 0 or more Datasets
            for seq_idx, seq_item in enumerate(elem.value):
                tree_seq_item = tree.insert('', tk.END, text=f'{elem.name} Item {seq_idx + 1}')
                tree.move(tree_seq_item, tree_item, seq_idx)

                # Recurse into the sequence item(s)
                build_tree(tree, seq_item, tree_seq_item)
