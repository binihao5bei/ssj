import allure
import pytest


@allure.story("创建文件夹")
@pytest.mark.dependency(name="create_folder", depends=["create_team"], scope="session")
def test_create_folder(login, rq, value):
    rq(value)


@allure.story("删除文件夹接口")
@pytest.mark.dependency(depends=["create_folder"])
def test_del_folder(rq, value):
    rq(value)


@allure.story("重命名文件夹接口")
@pytest.mark.dependency(depends=["create_folder"])
def test_rename_folder(rq, value):
    rq(value)


@allure.story("获取文件夹接口")
@pytest.mark.dependency(depends=["create_folder"])
def test_get_folder(rq, value):
    rq(value)


@allure.story("获取文件夹下项目")
@pytest.mark.dependency(depends=["create_project", "create_folder"], scope="session")
def test_folder_projects(rq, value):
    rq(value)


@allure.story("获取文件夹下所有项目")
@pytest.mark.dependency(depends=["create_folder"], scope="session")
def test_one_folder_projects(rq, value):
    rq(value)
