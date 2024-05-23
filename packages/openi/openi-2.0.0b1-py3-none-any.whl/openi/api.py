#!/usr/bin/env python

from pathlib import Path
from typing import Iterator, List, Literal, Optional, Union

import requests
from deprecated import deprecated

from ._dataclass import (
    BasicResp,
    DatasetFile,
    DatasetInfo,
    FileChunkInfo,
    ModelCreate,
    ModelFile,
    ModelInfo,
    MultipartUrl,
    NewMultipart,
    RepoInfo,
    UserInfo,
)
from ._exceptions import (
    DatasetNotFound,
    ModelNotFoundError,
    RepoNotFoundError,
    ServerFileExistsError,
    UploadError,
)
from ._file import (
    file_chunk_iterator,
    get_file_size,
)
from ._session import OpenISession
from .constants import (
    AI_MODEL_VERSION_FILE,
    DOWNLOAD_RATES,
    UPLOAD_ENDPOINT,
    UPLOAD_ID_PARAM,
)
from .log import setup_logger

logger = setup_logger("info")


def filter_model_version_file(
    model_files: List[ModelFile],
) -> Optional[List[ModelFile]]:
    """
    Filter model version files from a list of model files.

    Args:
        model_files (List[ModelFile]): List of model files

    Returns:
        List[ModelFile]: List of model version files
    """
    filtered = [f for f in model_files if f.FileName != AI_MODEL_VERSION_FILE]
    if not filtered:
        return None
    return filtered


class OpenIApi:
    R"""
    OpenI API Wrapper Class

    This class provides a client session to the REST API of OpenI AiForge
    Project.

    All API endpoints are implemented as methods of this class. The class
    methods wrap the original API json response in Python dataclass format,
    with tiny changes on some variables names.

    For more information, refer to the official git repo source code:
        - https://openi.pcl.ac.cn/OpenI/aiforge

    Args:
        endpoint (str, optional):
            URL for the OpenI website.
            When not specified, will load from local machine at
            `/home/{usr}/.openi/token.json`

        token (str, optional):
            login user access token obtained by following url:
                - https://openi.pcl.ac.cn/user/settings/applications
            When not specified, will load from local machine at
            `/home/{usr}/.openi/token.json`
    """

    def __init__(
        self,
        token: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        self.session = OpenISession()
        self.session.set_basic_auth(token=token, endpoint=endpoint)

        logger.info(f"New OpenIApi Session @{self.session.endpoint}")

    def dev(self, mode: bool = False):
        self.session.dev_mode = mode

    """
    Base API Endpoints
    """

    def get_user_info(self) -> UserInfo:
        """Retrieve user info for currently authenticated user

        Returns:
            UserInfo: UserInfo object containing metadata about current
            login user
        """
        resp = self.session.get(
            "/user",
        )
        data = resp.json()
        return UserInfo(**data)

    def get_repo_info(self, repo_id: str) -> RepoInfo:
        """Retrieve repository info for given repo id

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format

        Returns:
            RepoInfo: RepoInfo object containing metadata about given repo id
        """
        resp = self.session.get(
            f"/repos/{repo_id}",
        )
        data = resp.json()
        return RepoInfo(**data)

    def get_repo_access_right(self, repo_id: str) -> str:
        """Retrieve current login user's operation right for a specific
        repository

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format

        Returns:
            RepoPermission:
                access right information wrapped in RepoPermission object,
                containing three attributes: [`write` `read` or `none`]
        """
        r = self.session.get(
            f"/repos/{repo_id}/right",
        )
        resp = r.json()["right"]
        return resp

    """
    Dataset API Endpoints
    """

    def get_dataset_url(self, repo_id: str) -> str:
        """Get dataset url"""
        return f"{self.session.endpoint}/{repo_id}/datasets"

    def get_dataset_info(
        self,
        repo_id: str,
        upload_type: int = 1,
    ) -> Optional[DatasetInfo]:
        params: dict = {"type": upload_type}
        r = self.session.get(
            f"/{repo_id}/sdk/get_dataset",
            params=params,
        )
        resp = BasicResp(**r.json())
        if resp.code == -1:
            raise DatasetNotFound(repo_id, self.get_dataset_url(repo_id))

        resp.data["repo_id"] = repo_id
        return DatasetInfo(**resp.data) or None

    def list_dataset_files(
        self,
        repo_id: str,
        upload_type: int = 1,
    ) -> Optional[List[DatasetFile]]:
        dataset_info = self.get_dataset_info(
            repo_id=repo_id, upload_type=upload_type
        )

        if dataset_info is None:
            raise DatasetNotFound(repo_id, self.get_dataset_url(repo_id))

        return dataset_info.attachments

    def query_dataset_file(
        self,
        repo_id: str,
        filename: str,
        upload_type: int = 1,
    ) -> Optional[DatasetFile]:
        dataset_files = self.list_dataset_files(
            repo_id=repo_id,
            upload_type=upload_type,
        )

        if dataset_files is None:
            return None

        try:
            return next(f for f in dataset_files if f.name == filename)
        except StopIteration:
            return None

    """
    Model API Endpoints
    """

    def get_repo_models_url(self, repo_id: str) -> str:
        """Get model list url"""
        return f"{self.session.endpoint}/{repo_id}/modelmanage/show_model"

    def get_model_url(self, repo_id: str, model_name: str) -> str:
        """Get model url"""
        return f"{self.session.endpoint}/{repo_id}/modelmanage/model_filelist_tmpl?name={model_name}"

    def create_model(
        self,
        repo_id: str,
        model_name: str,
        upload_type: int = 1,
        engine: int = 0,
        is_private=True,
    ) -> ModelCreate:
        """Create a new model in a specific repo

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format
            model_name (str): model_name of the model to create
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            engine (int): engine of the model to create; 0 for PyTorch,
            1 for TensorFlow
            is_private (bool): whether the model is private or not

        Returns:
            dict: model info in json format of the response from OpenI
        """
        r = self.session.get(
            f"/repos/{repo_id}/modelmanage/create_local_model",
            params=dict(
                name=model_name,
                type=upload_type,
                engine=engine,
                isPrivate=is_private,
            ),
        )
        resp = r.json()
        return ModelCreate(**resp)

    def get_model_info(
        self, repo_id: str, model_name: str
    ) -> Optional[ModelInfo]:
        params: dict = {"name": model_name}
        r = self.session.get(
            f"/{repo_id}/sdk/get_model",
            params=params,
        )
        resp = BasicResp(**r.json())
        if resp.code == -1:
            raise ModelNotFoundError(
                model_name, self.get_repo_models_url(repo_id)
            )

        resp.data["repo_id"] = repo_id
        return ModelInfo(**resp.data) or None

    def list_model_files(
        self,
        repo_id: str,
        model_name: str,
    ) -> Optional[List[ModelFile]]:
        model_info = self.get_model_info(
            repo_id=repo_id, model_name=model_name
        )

        if model_info is None:
            raise ModelNotFoundError(
                repo_id, self.get_repo_models_url(repo_id)
            )

        return filter_model_version_file(model_info.modelFileList)

    def query_model_file(
        self,
        repo_id: str,
        model_name: str,
        filename: str,
    ) -> Optional[ModelFile]:
        model_files = self.list_model_files(
            repo_id=repo_id, model_name=model_name
        )

        if model_files is None:
            return None

        try:
            return next(f for f in model_files if f.FileName == filename)
        except StopIteration:
            return None

    """
    Download API Endpoint
    """

    def download_file_iterator(
        self,
        src_file: Union[DatasetFile, ModelFile],
        filepath: Union[Path, str],
        chunk_size: int = DOWNLOAD_RATES,
    ) -> Iterator[int]:
        """Download a specific file by filename

        Args:
            src_file (Union[DatasetFile, ModelFile]):
                file object containing metadata of the file
            filepath (Union[Path, str]):
                local file path to be downloaded
            chunk_size (int, optional):
                size of the chunk to download
        """
        if not isinstance(filepath, Path):
            filepath = Path(filepath).absolute()

        if not isinstance(src_file, (DatasetFile, ModelFile)):
            raise ValueError(f"Invalid file type: {type(src_file)}")

        if isinstance(src_file, DatasetFile):
            return self.download_dataset_file_iterator(
                dataset_file=src_file,
                filepath=filepath,
                chunk_size=chunk_size,
            )

        if isinstance(src_file, ModelFile):
            return self.download_model_file_iterator(
                model_file=src_file,
                filepath=filepath,
                chunk_size=chunk_size,
            )

    def download_dataset_file_iterator(
        self,
        dataset_file: DatasetFile,
        filepath: Path,
        chunk_size: int = DOWNLOAD_RATES,
    ) -> Iterator[int]:
        """Download a specific attachment file by uuid

        Args:
            dataset_file (DatasetFile): dataset_file object containing
            metadata of the file
            filepath (Path): local file path to be downloaded
            chunk_size (int, optional): size of the chunk to download,
            defaults to DOWNLOAD_RATES
        """
        if not filepath.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.touch()

        cache_size = get_file_size(filepath)
        yield cache_size

        if cache_size == dataset_file.size:
            return

        repo_id: str = dataset_file.repo_id
        uuid: str = dataset_file.uuid
        upload_type: int = dataset_file.type
        params: dict = {"type": upload_type}
        headers: dict = {"Range": "bytes=%d-" % cache_size}

        try:
            with self.session.get(
                f"/{repo_id}/sdk/download_dataset_file/{uuid}",
                params=params,
                headers=headers,
                allow_redirects=True,
                stream=True,
            ) as resp:
                with open(filepath, "ab") as f:
                    for chunk_data in resp.iter_content(chunk_size=chunk_size):
                        f.write(chunk_data)
                        yield len(chunk_data)

        except Exception as e:
            raise e

    def download_model_file_iterator(
        self,
        model_file: ModelFile,
        filepath: Path,
        chunk_size: int = DOWNLOAD_RATES,
    ) -> Iterator[int]:
        """Download a specific model file by filename

        Args:
            model_file (ModelFile): model_file object containing metadata
            of the file
            filepath (Path): local file path to be downloaded
            chunk_size (int, optional): size of the chunk to download
        """
        if not filepath.parent.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)

        cache_size = get_file_size(filepath) if filepath.exists() else 0
        yield cache_size

        if cache_size == model_file.Size:
            return

        repo_id: str = model_file.repo_id
        model_id: str = model_file.model_id
        filename: str = model_file.FileName
        params: dict = {"fileName": filename}
        headers: dict = {"Range": "bytes=%d-" % cache_size}

        try:
            with self.session.get(
                f"/{repo_id}/sdk/download_model_file/{model_id}",
                params=params,
                headers=headers,
                allow_redirects=True,
                stream=True,
            ) as resp:
                with open(filepath, "ab") as f:
                    for chunk_data in resp.iter_content(chunk_size=chunk_size):
                        f.write(chunk_data)
                        yield len(chunk_data)

        except Exception as e:
            raise e

    """
    File Upload API Endpoints
    """

    def upload_get_chunks(
        self,
        dataset_or_model_id: str,
        md5: str,
        filename: str,
        upload_type: int,
        upload_mode: Literal["dataset", "model"],
    ) -> FileChunkInfo:
        """Get chunks info for a specific file upload

        Args:
            dataset_or_model_id (str): dataset or model id
            md5 (str): md5 hash of the file
            filename (str): name of the file
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            upload_mode (str): upload mode; "dataset" or "model"

        Returns:
            FileChunkInfo: FileChunkInfo object containing metadata of the file
        """
        route = UPLOAD_ENDPOINT.get(upload_mode, "") + "/get_chunks"
        id_param = UPLOAD_ID_PARAM.get(upload_mode, None)
        if not route or not id_param:
            raise ValueError(f"Invalid upload_mode: {upload_mode}")

        params = dict(file_name=filename, md5=md5, type=upload_type)
        params.update({id_param: dataset_or_model_id})

        resp = self.session.get(
            route,
            params=params,
        )
        data = resp.json()
        #
        # if "result_code" in data and data["result_code"] == "-1":
        #     raise ValueError(f"Failed to get chunks info: {data['msg']}")

        data.update({"upload_mode": upload_mode})
        data.update({"md5": md5})
        return FileChunkInfo(**data)

    def upload_new_multipart(
        self,
        dataset_or_model_id: str,
        md5: str,
        filename: str,
        filesize: int,
        total_chunks_counts: int,
        upload_type: int,
        upload_mode: Literal["dataset", "model"],
    ) -> NewMultipart:
        """Create a new multipart upload of a specific file

        Args:
            dataset_or_model_id (str): dataset or model id
            md5 (str): md5 hash of the file
            filename (str): name of the file
            filesize (int): size of the file
            total_chunks_counts (int): total chunks count of the file
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            upload_mode (str): upload mode; "dataset" or "model"

        Returns:
            NewMultipart: NewMultipart object containing metadata of the file
        """
        route = UPLOAD_ENDPOINT.get(upload_mode, "") + "/new_multipart"
        id_param = UPLOAD_ID_PARAM.get(upload_mode, None)
        if not route or not id_param:
            raise ValueError(f"Invalid upload_mode: {upload_mode}")

        params = dict(
            md5=md5,
            file_name=filename,
            size=filesize,
            totalChunkCounts=total_chunks_counts,
            type=upload_type,
        )
        params.update({id_param: dataset_or_model_id})

        resp = self.session.get(
            route,
            params=params,
        )
        data = resp.json()
        return NewMultipart(**data)

    def upload_get_multipart_url(
        self,
        dataset_or_model_id: str,
        uuid: str,
        upload_id: str,
        upload_type: int,
        upload_mode: Literal["dataset", "model"],
        chunk_number: int,
        chunk_size: int,
        filename: Optional[str] = None,
    ) -> MultipartUrl:
        """Get upload url for a specific file_chunk

        Args:
            dataset_or_model_id (str): dataset or model id
            uuid (str): uuid of the file
            upload_id (str): upload id of the file
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            chunk_number (int): chunk number of the file
            chunk_size (int): size of the chunk
            filename (str): name of the file
            upload_mode (str): upload mode; "dataset" or "model"

        Returns:
            MultipartUrl: MultipartUrl object containing metadata of the file
        """
        route = UPLOAD_ENDPOINT.get(upload_mode, "") + "/get_multipart_url"
        id_param = UPLOAD_ID_PARAM.get(upload_mode, None)
        if not route or not id_param:
            raise ValueError(f"Invalid upload_mode: {upload_mode}")

        params = dict(
            uuid=uuid,
            uploadID=upload_id,
            type=upload_type,
            chunkNumber=chunk_number,
            size=chunk_size,
        )
        if upload_mode == "dataset":
            params.update(
                {f"{id_param}": dataset_or_model_id, "file_name": filename}
            )

        resp = self.session.get(
            route,
            params=params,
        )
        data = dict()
        if resp.status_code == 200:
            data.update({"url": resp.json()["url"]})
        if resp.status_code in [400, 500]:
            data.update({"msg": resp.text})

        return MultipartUrl(**data)

    def upload_complete_multipart(
        self,
        dataset_or_model_id: str,
        upload_mode: Literal["dataset", "model"],
        upload_type: int,
        upload_id: str,
        uuid: str,
        filename: Optional[str] = None,
        filesize: Optional[int] = None,
    ) -> Union[bool, dict]:
        """Complete a multipart upload of a specific file

        Args:
            dataset_or_model_id (str): dataset or model id
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            upload_id (str): upload id of the file
            uuid (str): uuid of the file
            filename (str): name of the file
            filesize (int): size of the file
            upload_mode (str): upload mode; "dataset" or "model"

        Returns:
            Union[bool, dict]: returns True if upload is successful,
            otherwise False
        """

        route = UPLOAD_ENDPOINT.get(upload_mode, "") + "/complete_multipart"
        id_param = UPLOAD_ID_PARAM.get(upload_mode)
        if not route or not id_param:
            raise ValueError(f"Invalid upload_mode: {upload_mode}")

        params = dict(
            uuid=uuid,
            uploadID=upload_id,
            type=upload_type,
        )
        params.update({id_param: dataset_or_model_id})
        if upload_mode == "dataset":
            params.update(dict(file_name=filename, size=filesize))

        resp = self.session.post(
            route,
            params=params,
        )
        try:
            data = resp.json()
            if "result_code" in data.keys():
                return data["result_code"] == "0"
        except:
            return False

        return False

    def upload_file_iterator(
        self,
        filepath: Union[Path, str],
        dataset_or_model_id: str,
        file_md5: str,
        file_size: int,
        total_chunks_count: int,
        upload_mode: Literal["model", "dataset"],
        upload_name: str,
        upload_type: int,
        chunk_size: int,
    ) -> Iterator[int]:
        """Upload single model file from local to OpenI

        Args:

        Returns:
            Iterator[int]:
                iterator of len(bytes) uploaded, for upload progress
                notification; generally should yield CHUNK_SIZE
                except the last chunk, whose len(bytes) might be <= CHUNK_SIZE.
        """

        # get chunk
        get_chunks = self.upload_get_chunks(
            dataset_or_model_id=dataset_or_model_id,
            md5=file_md5,
            filename=upload_name,
            upload_type=upload_type,
            upload_mode=upload_mode,
        )
        if not get_chunks or get_chunks.result_code == -1:
            if get_chunks.msg:
                msg = f"get chunks failed with error {get_chunks.msg}"
            else:
                msg = f"get chunks create failed with unknown error."
            logger.error(msg)
            raise UploadError(msg)
        logger.info(f"`{upload_name}` {get_chunks}")

        if get_chunks.uploaded:
            if get_chunks.fileName and get_chunks.fileName != upload_name:
                existing_filename = get_chunks.fileName
            else:
                existing_filename = None
            logger.warning(
                f"{upload_name} already uploaded as {existing_filename}"
            )
            raise ServerFileExistsError(
                filename=upload_name,
                existing_filename=existing_filename,
            )

        # new multipart
        if not get_chunks.uuid or not get_chunks.uploadID:
            new_multipart = self.upload_new_multipart(
                dataset_or_model_id=dataset_or_model_id,
                filename=upload_name,
                upload_type=upload_type,
                md5=file_md5,
                filesize=file_size,
                total_chunks_counts=total_chunks_count,
                upload_mode=upload_mode,
            )
            if not new_multipart or new_multipart.result_code == -1:
                if new_multipart.msg:
                    msg = (
                        f"new multipart failed with error: {new_multipart.msg}"
                    )
                else:
                    msg = f"new multipart failed with unknown error."
                logger.error(msg)
                raise UploadError(msg)

            get_chunks.uploadID = new_multipart.uploadID
            get_chunks.uuid = new_multipart.uuid

            logger.info(f"`{upload_name}` {new_multipart}")

        etags: List = list()
        start_from_chunk = len(get_chunks.uploaded_chunks) or 1
        yield chunk_size * (start_from_chunk - 1)

        # get multipart url
        # put upload
        for chunk_number, chunk_data in file_chunk_iterator(
            filepath=filepath,
            chunk_size=chunk_size,
            start_from_chunk=start_from_chunk,
        ):
            multipart_url = self.upload_get_multipart_url(
                dataset_or_model_id=dataset_or_model_id,
                chunk_number=chunk_number,
                uuid=get_chunks.uuid,
                upload_id=get_chunks.uploadID,
                upload_mode=upload_mode,
                upload_type=upload_type,
                chunk_size=len(chunk_data),
                filename=upload_name,
            )
            if not multipart_url.url:
                msg = (
                    f"get multipart url failed with"
                    f" error {multipart_url.msg}."
                )
                logger.error(msg)
                raise UploadError(msg)
            logger.info(f"`{upload_name}` {multipart_url}")

            etag = self.session.put_upload(
                url=multipart_url.url,
                filedata=chunk_data,
                upload_type=upload_type,
            )
            if not etag:
                raise UploadError("put upload failed")

            yield len(chunk_data)
            etags.append(etag)

        if len(etags) != total_chunks_count - start_from_chunk + 1:
            msg = (
                f"some chunk failed to upload, can not complete upload "
                f"process."
            )
            logger.error(msg)
            raise UploadError(msg)

        # complete multipart
        complete = self.upload_complete_multipart(
            dataset_or_model_id=dataset_or_model_id,
            upload_mode=upload_mode,
            uuid=get_chunks.uuid,
            upload_id=get_chunks.uploadID,
            filename=upload_name,
            filesize=file_size,
            upload_type=upload_type,
        )
        if not complete:
            msg = f"complete multipart failed with unknown error."
            logger.error(msg)
            raise UploadError(msg)
        logger.info(f"`{upload_name}` complete_multipart: {complete}")

        logger.info("uploading success.")

    """
    deprecated method, to be removed
    """

    @deprecated
    def get_repo_dataset_info(self, repo_id: str) -> Optional[DatasetInfo]:
        """Mainly used for query the dataset_id with given repo_id.

        This api only retrieve the MAIN dataset of current repo,
        does not return any other related datasets' information.


        Args:
            repo_id (str): Repository ID in `Username/Reponame` format

        Returns:
            DatasetInfo (optional):
                DatasetInfo containing metadata of current repo's dataset
                without any attachment(dataset file) information.
                Returns None if dataset is yet to be created.
        """
        resp = self.session.get(
            f"/datasets/{repo_id}",
        )

        if resp.status_code == 404:
            raise RepoNotFoundError(repo_id)

        data = resp.json().get("data", None)
        if not data:
            dataset_url = self.get_dataset_url(repo_id)
            raise DatasetNotFound(repo_id=repo_id, dataset_url=dataset_url)

        data[0].update({"repo_id": repo_id})
        return DatasetInfo(**data[0])

    @deprecated
    def get_all_datasets_with_files(
        self, repo_id: str, upload_type: int = 0
    ) -> Optional[List[DatasetInfo]]:
        """Retrieve all datasets with attachments info for a specific repo

        This api will return all RELATED and MAIN dataset of current repo,
        as well as the attachment info(dataset files) with designated
        upload_type.
        Note that only `.zip` and `.tar.gz` files will be returned.

        Args:
            repo_id (str):
                Repository ID in `Username/Reponame` format
            upload_type (int):
                storage of files; 0 for GPU(minio), 1 for NPU(obs)

        Returns:
            list of DatasetInfo (optional):
                returns all datasets' metadata and their attachments
                with given upload_type.
                returns None if there is no datasets found in given
                upload_type.
        """
        resp = self.session.get(
            f"/datasets/{repo_id}/current_repo",
            params=dict(type=upload_type),
        )

        try:
            data = resp.json()["data"]
            for d in data:
                d["repo_id"] = repo_id
        except Exception as e:
            logger.error(f"Failed api._get_all_datasets_with_files: {e}")
            return None
        else:
            return [DatasetInfo(**d) for d in data]

    @deprecated
    def get_repo_dataset_with_files(
        self, repo_id: str, upload_type: int = 0
    ) -> Optional[DatasetInfo]:
        """Mainly used for retrieve dataset files for current repo dataset

        This method combines `get_repo_dataset()` and
        `_get_dataset_with_files()`
        API endpoints to retrieve MAIN dataset's metadata and attachment data
        with given upload_type.

        Args:
            repo_id (str):
                Repository ID in `Username/Reponame` format
            upload_type (int):
                storage of files; 0 for GPU(minio), 1 for NPU(obs)

        Returns:
            DatasetInfo (optional):
                returns DatasetInfo with attachments' information for current
                repository MAIN dataset.
                returns None if no corresponding files found for given
                upload_type.
        """
        repo_dataset = self.get_repo_dataset_info(repo_id)
        all_datasets = self.get_all_datasets_with_files(repo_id, upload_type)

        if not all_datasets or not repo_dataset:
            return None

        try:
            return next(d for d in all_datasets if d.id == repo_dataset.id)
        except StopIteration:
            logger.error(f"Could not found repo_dataset in: {repo_id}")
            return None
        except Exception as e:
            logger.error(f"Failed api.get_dataset_with_files: {e}")
            return None

    @deprecated
    def list_repo_dataset_files_with_info(
        self, repo_id: str, upload_type: int = 0
    ) -> Optional[List[DatasetFile]]:
        """Retrieve all dataset files for a specific repo

        Args:
            repo_id (str):
                Repository ID in `Username/Reponame` format
            upload_type (int):
                storage of files; 0 for GPU(minio), 1 for NPU(obs)

        Returns:
            list of DatasetFile (optional):
                returns all dataset files for current repository MAIN dataset.
                returns None if no corresponding files found for given
                upload_type.
        """
        dataset = self.get_repo_dataset_with_files(repo_id, upload_type)
        return dataset.attachments if dataset else None

    @deprecated
    def list_repo_dataset_files(
        self, repo_id: str, upload_type: int = 0
    ) -> Optional[List[str]]:
        """Retrieve all dataset files for a specific repo

        Args:
            repo_id (str):
                Repository ID in `Username/Reponame` format
            upload_type (int):
                storage of files; 0 for GPU(minio), 1 for NPU(obs)

        Returns:
            list of str (optional):
                returns all dataset files for current repository MAIN dataset.
                returns None if no corresponding files found for given
                upload_type.
        """
        dataset = self.get_repo_dataset_with_files(repo_id, upload_type)
        return [f.name for f in dataset.attachments] if dataset else None

    @deprecated
    def get_repo_dataset_file(
        self, repo_id: str, filename: str, upload_type: int = 0
    ) -> Optional[DatasetFile]:
        """Get dataset file info for a specific file

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format
            filename (str): filename of the file to be downloaded
            upload_type (int): storage of file; 0 for (GPU/minio), 1 for (
            NPU/obs)

        Returns:
            DatasetFile (optional): DatasetFile object containing metadata
            of the file
        """
        files = self.list_repo_dataset_files_with_info(repo_id, upload_type)
        try:
            target_file = next(f for f in files if f.name == filename)
        except StopIteration:
            logger.error(
                f"Could not found file `{filename}` in repo_dataset `{repo_id}`"
            )
            return None

        return target_file if target_file else None

    @deprecated
    def download_dataset_file(
        self, dataset_file: DatasetFile, from_bytes: int = 0
    ) -> requests.Response:
        """Download a specific attachment file by uuid

        Args:
            upload_type (`int`): storage of file; 0 for (GPU/minio), 1 for (
            NPU/obs)
            uuid (`str`): uuid of the file to be uploaded

        Returns:
            redirect response to download url
        """
        uuid: str = dataset_file.uuid
        upload_type: int = dataset_file.type
        params: dict = {"type": upload_type}
        headers: dict = {"Range": "bytes=%d-" % from_bytes}

        return self.session.get(
            f"/attachments/{uuid}",
            params=params,
            headers=headers,
            allow_redirects=True,
            stream=True,
        )

    @deprecated
    def query_model_by_name(self, repo_id: str, model_name: str) -> ModelInfo:
        """Retrieve model info for a specific model

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format
            model_name (str): name of the model to retrieve

        Returns:
            dict: model info in json format of the response from OpenI
        """
        resp = self.session.get(
            f"/repos/{repo_id}/modelmanage/query_model_byName",
            params=dict(name=model_name),
        )
        if resp.status_code == 404:
            raise RepoNotFoundError(repo_id)

        data = resp.json()
        if not data:
            model_list_url = self.get_model_list_url(repo_id)
            raise ModelNotFoundError(
                model_name=model_name, model_list_url=model_list_url
            )
            # return None

        data[0].update({"repo_id": repo_id})
        return ModelInfo(**data[0])

    @deprecated
    def list_model_files_info(
        self, repo_id: str, model_name: str
    ) -> Optional[List[ModelFile]]:
        """Retrieve list of model files ONLY for a specific model

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format
            model_id (str): model_id of the model to retrieve

        Returns:
            dict: model files info in json format of the response from OpenI
        """
        model_info = self.get_model_info(
            repo_id=repo_id, model_name=model_name
        )
        if not model_info:
            return None

        print(model_info)
        model_id: str = model_info.id

        resp = self.session.get(
            f"/repos/{repo_id}/modelmanage/query_modelfile_for_predict",
            params=dict(id=model_id),
        )

        data = resp.json()

        if not data:
            return None

        for model_file in data:
            model_file.update({"repo_id": repo_id, "model_id": model_id})

        return [ModelFile(**model_file) for model_file in data]

    @deprecated
    def get_model_file(
        self, repo_id: str, model_name: str, filename: str
    ) -> Optional[ModelFile]:
        """Retrieve size of a specific model file by filename

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format
            model_id (str): model_id of the model to retrieve
            filename (str): filename of the file to be downloaded

        Returns:
            int: size of the file
        """
        list_files = self.list_model_files_info(repo_id, model_name)

        if not list_files:
            return None

        try:
            target_file = next(f for f in list_files if f.FileName == filename)
        except StopIteration:
            return None

        return target_file

    @deprecated
    def download_model_file(
        self, model_file: ModelFile, from_bytes: Optional[int] = 0
    ) -> requests.Response:
        """Download a specific model file by filename

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format
            model_id (str): model_id of the model to retrieve
            filename (str): filename of the file to be downloaded

        Returns:
        """
        repo_id: str = model_file.repo_id
        model_id: str = model_file.model_id
        filename: str = model_file.FileName
        params: dict = {"filename": filename}
        headers: dict = {"Range": "bytes=%d-" % from_bytes}

        return self.session.get(
            f"/repos/{repo_id}/modelmanage/downloadsingle/{model_id}",
            params=params,
            headers=headers,
            allow_redirects=True,
            stream=True,
        )
