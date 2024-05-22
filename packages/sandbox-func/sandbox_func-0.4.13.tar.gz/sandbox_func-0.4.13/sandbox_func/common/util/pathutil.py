import os
from sandbox_func.common.config.LogConfig import DEFAULT_LOG_FILE


def get_project_path() -> str:
    common_path = os.path.dirname(os.path.dirname(__file__))
    sandbox_func_path = os.path.dirname(common_path)  # noqa
    return os.path.dirname(sandbox_func_path)


def get_test_path():
    project_path = get_project_path()
    test_path = os.path.join(project_path, "tests")
    return test_path


def get_log_file_path():
    project_path = get_project_path()
    log_file_path = os.path.join(project_path, DEFAULT_LOG_FILE)
    return log_file_path


def get_tmp_path():
    if os.getenv("env") in ["dev", "test", "prod"]:
        return "/tmp"  # 云函数环境
    return os.path.join(get_project_path(), "tmp")
