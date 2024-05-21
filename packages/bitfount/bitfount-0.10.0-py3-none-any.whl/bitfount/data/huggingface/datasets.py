"""Hugging Face Datasets."""

from __future__ import annotations

from typing import Any, Iterator, List, Mapping, Optional, Sequence, Tuple, Union, cast

import numpy as np
import pandas as pd

from bitfount.config import _PYTORCH_ENGINE, BITFOUNT_ENGINE
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN

if BITFOUNT_ENGINE == _PYTORCH_ENGINE:
    import torch

from bitfount.data.datasets import (
    _BaseBitfountDataset,
    _BitfountDataset,
    _FileSystemBitfountDataset,
    _FileSystemIterableBitfountDataset,
    _IterableBitfountDataset,
)
from bitfount.data.datasources.base_source import (
    FileSystemIterableSource,
    IterableSource,
)
from bitfount.data.types import (
    _Y_VAR,
    _DataEntryAllowingText,
    _HFSegmentation_ImageTextEntry,
    _ImageAndTabularEntry,
    _ImageEntry,
    _ImagesData,
    _SupportData,
    _TabularData,
    _TabularEntry,
    _TextData,
    _TextEntry,
)


class _BaseHuggingFaceDataset(_BaseBitfountDataset):
    """Hugging Face Dataset."""

    def __init__(
        self, labels2id: Optional[Mapping[str, int]] = None, **kwargs: Any
    ) -> None:
        self.labels2id = labels2id
        super().__init__(**kwargs)

    def _set_text_values(self, data: pd.DataFrame) -> None:
        """Sets `self.text`."""
        self.text = data.loc[
            :, self.selected_cols_semantic_types.get("text", [])
        ].values.tolist()

    def __len__(self) -> int:
        """Returns the length of the dataset."""
        data = self.get_dataset_split(
            split=self.data_split, data_splitter=self.data_splitter
        )
        self._reformat_data(data)
        return len(self.x_var[0])

    def _reformat_data(self, data: pd.DataFrame) -> None:
        """Reformats the data to be compatible with the Dataset class."""
        self.data = data.reset_index(drop=True)
        if self.labels2id is not None:
            # Encode categorical labels to integers in the data
            self.data = self.data.replace(self.labels2id)

        X, Y = self._get_xy(self.data)

        if self.image_columns:
            self._set_image_values(X)

        self._set_tabular_values(X)
        self._set_text_values(X)

        # Package tabular, image and text columns together under the x_var attribute
        self.x_var = (self.tabular, self.image, self.text)

        self._set_target_values(Y)

    def __getitem__(
        self, idx: Union[int, Sequence[int], torch.Tensor]
    ) -> _DataEntryAllowingText:
        if torch.is_tensor(idx):
            idx = cast(torch.Tensor, idx)
            list_idx: list = idx.tolist()
            return self._getitem(list_idx)
        else:
            idx = cast(Union[int, Sequence[int]], idx)
            return self._getitem(idx)

    def _getitem(self, idx: Union[int, Sequence[int]]) -> _DataEntryAllowingText:
        """Returns the item referenced by index `idx` in the data."""
        image: _ImagesData
        tab: _TabularData
        text: _TextData
        target: Union[np.ndarray, Tuple[np.ndarray, ...]]

        # Get target
        if len(self.y_var) == 0:
            # Set the target, if the dataset has no supervision,
            # choose set the default value to be 0.
            target = np.array(0)
        elif (
            "image" in self.selected_cols_semantic_types
            and self.target in self.selected_cols_semantic_types["image"]
        ):
            # Check if the target is an image and load it.
            target = self._load_images(idx, what_to_load="target")
        else:
            target = self.y_var[idx]

        # If the Dataset contains both tabular and image data
        if self.image.size and self.tabular.size:
            tab = self.tabular[idx]
            image = self._load_images(idx)
            return (tab, image), target  # _ImageAndTabularEntry

        # If the Dataset contains only tabular data
        elif self.tabular.size:
            tab = self.tabular[idx]
            return tab, target  # _TabularEntry

        # If the Dataset contains image and text data
        # Used for Hugging Face image segmentation algorithm
        elif self.image.size and np.array(self.text).size:
            image = self._load_images(idx)
            text = self.text[idx]
            return cast(
                _HFSegmentation_ImageTextEntry, (image, text, target)
            )  # _HFSegmentation_ImageTextEntry

        # If the Dataset contains only image data
        elif self.image.size:
            image = self._load_images(idx)
            return image, target  # _ImageEntry

        # All cases remaining cases require text data only need the text (for now)
        else:
            text = self.text[idx]
            return text, target  # _TextEntry


class _HuggingFaceDataset(_BaseHuggingFaceDataset, _BitfountDataset):
    """Hugging Face Dataset."""

    datasource: IterableSource
    pass


class _IterableHuggingFaceDataset(_BaseHuggingFaceDataset, _IterableBitfountDataset):
    """Iterable HuggingFace Dataset.

    The main difference between this and other datasets
    is that it does not require a schema and does not
    include the support columns.
    """

    datasource: IterableSource

    def __iter__(self) -> Iterator[_DataEntryAllowingText]:
        """Iterates over the dataset."""
        for data_partition in self.yield_dataset_split(
            split=self.data_split, data_splitter=self.data_splitter
        ):
            self._reformat_data(data_partition)

            for idx in range(len(self.data)):
                yield self._getitem(idx)

    def __len__(self) -> int:
        # _BaseHuggingFaceDataset should take priority in MRO _except_ for __len__ as
        # the method implemented in _IterableBitfountDataset is better suited for the
        # iterable use-case (i.e. doesn't rely on a data split finder that requires
        # data to be loaded)
        return _IterableBitfountDataset.__len__(self)


_TabularEntryWithKey = Union[
    Tuple[Tuple[_TabularData, _SupportData], _Y_VAR, str],
    Tuple[_TabularData, _Y_VAR, str],
]
_TextEntryWithKey = Tuple[_TextData, _Y_VAR, str]
_ImageEntryWithKey = Union[
    Tuple[Tuple[_ImagesData, _SupportData], _Y_VAR, str],
    Tuple[_ImagesData, _Y_VAR, str],
]
_ImageAndTabularEntryWithKey = Union[
    Tuple[Tuple[_TabularData, _ImagesData, _SupportData], _Y_VAR, str],
    Tuple[Tuple[_TabularData, _ImagesData], _Y_VAR, str],
]
_HFSegmentation_ImageTextEntryWithKey = Tuple[_ImagesData, _TextData, _Y_VAR, str]
_HFDataEntryWithKey = Union[
    _TabularEntryWithKey,
    _TextEntryWithKey,
    _ImageEntryWithKey,
    _ImageAndTabularEntryWithKey,
    _HFSegmentation_ImageTextEntryWithKey,
]
_HFDataEntryNoKey = Union[
    _TabularEntry,
    _TextEntry,
    _ImageEntry,
    _ImageAndTabularEntry,
    _HFSegmentation_ImageTextEntry,
]


class _FileSystemHuggingFaceDataset(_HuggingFaceDataset, _FileSystemBitfountDataset):
    """File System HuggingFace Dataset."""

    data_keys: List[str]

    datasource: FileSystemIterableSource

    def _reformat_data(self, data: pd.DataFrame) -> None:
        super()._reformat_data(data)
        self.data_keys = cast(
            np.ndarray, data.loc[:, ORIGINAL_FILENAME_METADATA_COLUMN].values
        ).tolist()

    def __getitem__(  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        self, idx: Union[int, Sequence[int], torch.Tensor]
    ) -> _HFDataEntryWithKey:
        # Super method relies on calls to _getitem(), etc, which we have changed in
        # this class; this means we can constrain the return type even though we are
        # calling the super method
        return cast(_HFDataEntryWithKey, super().__getitem__(idx))

    def _getitem(self, idx: Union[int, Sequence[int]]) -> _HFDataEntryWithKey:  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        # Super method actually only returns a subset of DataEntryAllowingText types;
        # the wider typing is due to the base class's. We can constrain it to the
        # actual types as returned by that method.
        d: _HFDataEntryNoKey = cast(_HFDataEntryNoKey, super()._getitem(idx))
        if isinstance(idx, int):
            data_key = self.data_keys[idx]
        else:
            # TODO: [BIT-3851] support multi-index
            raise TypeError(f"idx of type ({type(idx)}) is not supported")

        # mypy: lack of support for tuple unpacking means we need to manually cast this
        new_d: _HFDataEntryWithKey = cast(_HFDataEntryWithKey, (*d, data_key))
        return new_d


class _FileIterableHuggingFaceDataset(
    _IterableHuggingFaceDataset, _FileSystemIterableBitfountDataset
):
    """File Iterable HuggingFace Dataset."""

    data_keys: List[str]

    datasource: FileSystemIterableSource

    def __iter__(self) -> Iterator[_HFDataEntryWithKey]:  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        # Super method relies on calls to _getitem(), etc, which we have changed in
        # this class; this means we can constrain the return type even though we are
        # calling the super method
        return cast(Iterator[_HFDataEntryWithKey], super().__iter__())

    def _reformat_data(self, data: pd.DataFrame) -> None:
        super()._reformat_data(data)
        self.data_keys = cast(
            np.ndarray, data.loc[:, ORIGINAL_FILENAME_METADATA_COLUMN].values
        ).tolist()

    def __getitem__(  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        self, idx: Union[int, Sequence[int], torch.Tensor]
    ) -> _HFDataEntryWithKey:
        # Super method relies on calls to _getitem(), etc, which we have changed in
        # this class; this means we can constrain the return type even though we are
        # calling the super method
        return cast(_HFDataEntryWithKey, super().__getitem__(idx))

    def _getitem(self, idx: Union[int, Sequence[int]]) -> _HFDataEntryWithKey:  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        # Super method actually only returns a subset of DataEntryAllowingText types;
        # the wider typing is due to the base class's. We can constrain it to the
        # actual types as returned by that method.
        d: _HFDataEntryNoKey = cast(_HFDataEntryNoKey, super()._getitem(idx))
        if isinstance(idx, int):
            data_key = self.data_keys[idx]
        else:
            # TODO: [BIT-3851] support multi-index
            raise TypeError(f"idx of type ({type(idx)}) is not supported")

        # mypy: lack of support for tuple unpacking means we need to manually cast this
        new_d: _HFDataEntryWithKey = cast(_HFDataEntryWithKey, (*d, data_key))
        return new_d
