import allure
import pytest


@allure.story("创建项目接口")
@pytest.mark.dependency(name="create_project", depends=["create_team"], scope="session")
def test_create_project(login, rq, value):
    rq(value)


@allure.story("获取项目图片更新")
@pytest.mark.dependency(depends=["create_project"])
def test_user_pic_status(rq, value):
    rq(value)


@allure.story("删除项目接口")
@pytest.mark.dependency(depends=["create_project"])
def test_del_project(rq, value):
    rq(value)


@allure.story("退出项目")
@pytest.mark.dependency(depends=["create_project"])
def test_quit_project(rq, value):
    rq(value)


@allure.story("项目添加成员")
@pytest.mark.dependency(name="add_member", depends=["create_project"])
def test_project_add_member(rq, value):
    rq(value)


@allure.story("项目移除成员")
@pytest.mark.dependency(depends=["add_member"])
def test_project_rm_member(rq, value):
    rq(value)


@allure.story("修改项目类型")
@pytest.mark.dependency(depends=["create_project"])
def test_change_project_type(rq, value):
    rq(value)


@allure.story("修改项目名称")
@pytest.mark.dependency(depends=["create_project"])
def test_change_project_name(rq, value):
    rq(value)


@allure.story("获取项目信息")
@pytest.mark.dependency(depends=["create_project"])
def test_get_project_info(rq, value):
    rq(value)


@allure.story("获取项目简单信息")
@pytest.mark.dependency(depends=["create_project"])
def test_multiple_projects(rq, value):
    rq(value)


@allure.story("@获取项目成员")
@pytest.mark.dependency(depends=["create_project"])
def test_project_usernames(rq, value):
    rq(value)


@allure.story("分享项目")
@pytest.mark.dependency(depends=["create_project"])
def test_share_project(rq, value):
    rq(value)


@allure.story("移动项目到其他团队")
@pytest.mark.dependency(depends=["create_project"])
def test_move_project(rq, value):
    rq(value)


@allure.story("移动项目到文件夹")
@pytest.mark.dependency(depends=["create_project", "create_folder"], scope="session")
def test_move_project_folder(rq, value):
    rq(value)
