import hashlib
import math
from pathlib import Path
from typing import Iterator, List, Optional, Tuple, Union

from .constants import CHUNK_SIZE, FILE_CACHE_PREFIX


class UploadFile:
    """
    file object for upload
    """

    def __init__(self, path: Union[str, Path], name: Optional[str] = None):
        if isinstance(path, str):
            path = Path(path).absolute()

        self.path = path
        self.name: str = name if name else path.name
        self.chunk_size = CHUNK_SIZE

    def __repr__(self):
        return (
            f"UploadFile(path={self.path}, name={self.name}, "
            f"size={self.size}, md5={self.md5}, "
            f"total_chunks_count={self.total_chunks_count})"
        )

    def exists(self) -> bool:
        if self.path.exists() and self.path.is_file():
            return True
        else:
            return False

    def is_zip(self) -> bool:
        suffixes = "".join(self.path.suffixes)
        return ".zip" in suffixes or ".tar.gz" in suffixes

    @property
    def size(self) -> int:
        return self.path.stat().st_size

    @property
    def md5(self) -> str:
        return get_file_md5(self.path, chunk_size=self.chunk_size)

    @property
    def total_chunks_count(self) -> int:
        return get_file_total_chunks_count(
            self.path, chunk_size=self.chunk_size
        )


class CacheFile:
    """
    file object for download
    """

    def __init__(
        self,
        name: str,
        size: int,
        save_path: Union[Path, str],
        force: bool = False,
    ):
        self.name: str = name
        self.size: int = size

        if isinstance(save_path, str):
            save_path = Path(save_path).absolute()
        self.save_path: Path = save_path

        self.file_path = self.save_path / self.name
        self.cache_path = self.save_path / f"{FILE_CACHE_PREFIX}{self.name}"

        if force:
            self.force_download()

        if not self.cache_path.exists():
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.touch(exist_ok=True)

    def __repr__(self):
        return (
            f"CacheFile(name={self.name}, size={self.size}, "
            f"save_path={self.save_path},"
            f"file_path={self.file_path}, cache_path={self.cache_path})"
        )

    @property
    def cache_size(self) -> int:
        return self.cache_path.stat().st_size

    def as_completed(self, rename_existing: bool = True) -> bool:
        if self.cache_size != self.size:
            return False

        if rename_existing and self.file_path.exists():
            self.file_path = rename_existing_file(self.file_path)

        self.cache_path.rename(self.file_path)
        return True

    def force_download(self) -> None:
        self.file_path.unlink(missing_ok=True)
        self.cache_path.unlink(missing_ok=True)


def rename_existing_file(filepath: Union[str, Path]) -> Path:
    """Renames a file by adding a digital suffix in case of conflicts.

    Args:
        filepath (Path): The path to the file to rename.

    Returns:
        Path: The new path of the renamed file.
    """
    if isinstance(filepath, str):
        filepath = Path(filepath).absolute()

    filename = filepath.name.split(".")
    stem, suffix = filename[0], ".".join(filename[1:])
    new_filepath = filepath

    i = 1
    while new_filepath.exists():
        new_filepath = filepath.with_name(f"{stem}({i}).{suffix}")
        i += 1

    return new_filepath


def is_file(filepath: Path) -> bool:
    return filepath.is_file()


def is_dir(filepath: Path) -> bool:
    return filepath.is_dir()


def is_zip(filepath: Path) -> bool:
    suffixes = "".join(filepath.suffixes)
    return ".zip" in suffixes or ".tar.gz" in suffixes


def get_file_size(filepath: Path) -> int:
    return filepath.stat().st_size


def get_file_md5(filepath: Path, chunk_size: int = CHUNK_SIZE) -> str:
    # upload_mode: Literal["model", "dataset"],
    m = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            md5_data = data[
                : 1024 * 1024
            ]  # if upload_mode == "dataset" else data
            m.update(md5_data)
    return m.hexdigest()


def get_file_total_chunks_count(
    filepath: Path, chunk_size: int = CHUNK_SIZE
) -> int:
    file_size = get_file_size(filepath)
    return math.ceil(file_size / chunk_size)


def file_chunk_iterator(
    filepath: Path,
    chunk_size: int = CHUNK_SIZE,
    start_from_chunk: int = 1,
) -> Iterator[Tuple[int, bytes]]:
    """
    Iterate over file chunks data.

    Args:
        filepath (Union[str, Path]): local file path
        chunk_size (int, optional): chunk size.
        start_from_chunk (int, optional): start from chunk. Defaults to 1.

    Yields:
        Tuple[int, bytes]: chunk number and chunk data
    """
    chunk_number = start_from_chunk

    with open(filepath, "rb") as f_reader:
        f_reader.seek((start_from_chunk - 1) * chunk_size)
        while True:
            chunk_data = f_reader.read(chunk_size)
            if not chunk_data:
                break

            yield chunk_number, chunk_data

            chunk_number += 1


def split_subdir_name(filename: str) -> Tuple[str, str]:
    """
    Split the filename into subdirectory and name.

    Args:
        filename (str): The name of the file.

    Returns:
        Tuple[str, str]: The subdirectory and the name of the file.
    """
    as_path = Path(filename.lstrip("/"))
    return as_path.parent.as_posix(), as_path.name


def get_local_dir_files(local_dir: Path) -> List[Path]:
    """
    Returns a list of filepath in given directory.
    """
    return [file for file in local_dir.rglob("*") if file.is_file()]


# def get_local_dir_zipfiles(local_dir: Union[Path, str]) -> List[UploadFile]:
#     """
#     Returns a list of dictionaries containing file information.
#
#     Args:
#         folder_path (Path): Path to the folder to process.
#
#     Returns:
#         list: A list of dictionaries with the following structure:
#             {
#                 "path": Path object representing the file path,
#                 "name": Relative path of the file from the given folder
#             }
#     """
#     if isinstance(local_dir, str):
#         local_dir = Path(local_dir).absolute()
#
#     if not local_dir.is_dir():
#         raise LocalDirNotFound(f"{local_dir} is not a directory")
#
#     file_list = list()
#     for file in local_dir.rglob("*"):
#         if file.is_file() and is_zip(file):
#             path = file
#             name = file.name
#             size = get_file_size(file)
#
#             file_obj = UploadFile(path=path, name=name, size=size)
#
#             file_list.append(file_obj)
#
#     return file_list
