# coding:utf-8
import allure
import pytest


@allure.story("创建团队接口")
@pytest.mark.dependency(name="create_team", depends=["login"], scope="session")
def test_creat_team(rq, value):
    rq(value)


@allure.story("删除团队接口")
@pytest.mark.dependency(depends=["create_team"])
def test_del_team(rq, value):
    rq(value)


@allure.story("获取团队信息")
@pytest.mark.dependency(depends=["create_team"])
def test_get_team(rq, value):
    rq(value)


@allure.story("修改团队名称")
@pytest.mark.dependency(depends=["create_team"])
def test_put_team(rq, value):
    rq(value)


@allure.story("生成邀请")
@pytest.mark.dependency(name="serializer", depends=["create_team"])
def test_serializer(rq, value):
    rq(value)


@allure.story("生成短链")
@pytest.mark.dependency(depends=["serializer"])
def test_short_url(rq, value):
    rq(value)


# 会导致登录失效
@allure.story("邮箱邀请")
@pytest.mark.dependency(depends=["serializer"])
def test_put_invite_member(rq, value):
    rq(value)


# 会导致登录失效
@allure.story("链接邀请")
@pytest.mark.dependency(name="invite_no_trace", depends=["serializer"])
def test_put_invite_no_trace(rq, value):
    rq(value)


@allure.story("移除团队成员")
@pytest.mark.dependency(depends=["create_team"])
def test_remove_member(login, rq, value):
    rq(value)


@allure.story("退出团队")
@pytest.mark.dependency(depends=["create_team"])
def test_quit_team(login, rq, value):
    rq(value)


@allure.story("搜索团队成员")
@pytest.mark.dependency(depends=["create_team"])
def test_search_member(rq, value):
    rq(value)


@allure.story("创建分组")
@pytest.mark.dependency(name="create_department", depends=["create_team"])
def test_create_department(rq, value):
    rq(value)


@allure.story("删除分组")
@pytest.mark.dependency(depends=["create_department"])
def test_del_department(rq, value):
    rq(value)


@allure.story("分组下权限低于当前用户的信息")
@pytest.mark.dependency(depends=["create_department"])
def test_users_in_department(rq, value):
    rq(value)


@allure.story("修改团队成员权限")
@pytest.mark.dependency(name="update_member", depends=["create_team"])
def test_update_member(rq, value):
    rq(value)


@allure.story("修改团队成员项目")
@pytest.mark.dependency(
    name="update_member", depends=["create_project"], scope="session"
)
def test_update_projects(rq, value):
    rq(value)


@allure.story("查询团队成员项目")
@pytest.mark.dependency(depends=["create_team"])
def test_users_to_projects(rq, value):
    rq(value)


@allure.story("获取团队下所有项目最近一个月最后使用时间")
@pytest.mark.dependency(depends=["create_team"])
def test_recently_used_project(rq, value):
    rq(value)


@allure.story("用户所在某团队的项目数")
@pytest.mark.dependency(depends=["create_team"])
def test_user_folder_project(rq, value):
    rq(value)


@allure.story("用户所在某团队的项目数")
@pytest.mark.dependency(depends=["create_team"])
def test_user_projects_cnt(rq, value):
    rq(value)


@allure.story("移交团队")
@pytest.mark.dependency(depends=["create_team"])
def test_transfer_team(rq, value):
    rq(value)


@allure.story("获取团队详细信息")
@pytest.mark.dependency(depends=["create_team"])
def test_team_detail(rq, value):
    rq(value)


@allure.story("获取团队名额信息")
@pytest.mark.dependency(depends=["create_team"])
def test_quota(rq, value):
    rq(value)


@allure.story("获取dsm项目")
@pytest.mark.dependency(depends=["create_team"])
def test_dsm_project(rq, value):
    rq(value)
