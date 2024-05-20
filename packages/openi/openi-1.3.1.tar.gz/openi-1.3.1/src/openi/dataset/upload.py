from ..services import *

log = logger.setup_logger()


def upload_file(
    file: str,
    repo_id: str,
    # cluster: str = "npu",
):
    """
    upload a dataset file to OpenI

    :param file: lcoal file name
    :param repo_id: repo id in form of `owner/repo_name`
    :param cluster: cluster type in [gpu,npu], default is `npu`
    :return:

    e.g.
    >>> from openi.dataset import upload_file
    >>> upload_file("cifar10.zip", "openi/official", cluster="gpu")

    Calculating file md5, this might take a while for large file…
    Complete( cifar10.zip)(gpu): 100%|████████████████████████| 163MB/163MB [00:00<00:00, 54.0MB/s]

    """

    log.info(f"{'-' * 200}")
    log.info(f"params - {locals()}")

    cluster = "npu"
    upload_type = get_upload_type(cluster)

    # OpeniFileUpload
    local_file = os.path.expanduser(file)
    if not os.path.exists(local_file):
        msg = f"❌ {local_file} 未找到本地文件"
        log.error(msg)
        raise ValueError(msg)

    openi_repo = OpeniRepo(repo_id=repo_id)
    if openi_repo.access != "write":
        msg = f"❌ `{openi_repo.current_user}` 无权限操作此仓库数据集 `{openi_repo.full_display_name}`"
        log.error(msg)
        raise ValueError(msg)

    openi_dataset = OpeniDataset(repo_id=openi_repo.repo_id)

    tqdm.write(
        "Calculating file md5, this might take a while for large file… "
    )
    openi_file = OpeniFileUpload(
        local_file=local_file,
        repo_id=openi_repo.repo_id,
        upload_type=upload_type,
        dataset_or_model_id=openi_dataset.dataset_id,
        dataset_or_model_name=openi_dataset.dataset_name,
        target_type="dataset",
    )

    display_progress_bar([openi_file])
    openi_file.upload_with_tqdm()
    log.info(f"{'-' * 200}")
