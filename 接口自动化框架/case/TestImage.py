import allure
import pytest


@allure.story("上传文件")
@pytest.mark.dependency(
    name="upload_files", depends=["create_project"], scope="session"
)
def test_upload_files(rq, value):
    rq(value)


@allure.story("上传设计图")
@pytest.mark.dependency(
    name="upload_image", depends=["create_project"], scope="session"
)
def test_upload_image(rq, value):
    rq(value)


@allure.story("获取图片信息")
@pytest.mark.dependency(depends=["upload_image"])
def test_get_image(rq, value):
    rq(value)


@allure.story("图片状态")
@pytest.mark.dependency(depends=["upload_image"])
def test_image_type(rq, value):
    rq(value)


@allure.story("获取>20M图片")
@pytest.mark.dependency(depends=["upload_image"])
def test_get_compressed(rq, value):
    rq(value)


@allure.story("设置原型主页")
@pytest.mark.dependency(depends=["upload_image"])
def test_image_home(rq, value):
    rq(value)


@allure.story("获取原型主页")
@pytest.mark.dependency(depends=["upload_image"])
def test_get_image_home(rq, value):
    rq(value)


@allure.story("添加原型链接")
@pytest.mark.dependency(depends=["upload_image"])
def test_prototype(rq, value):
    rq(value)


@allure.story("获取原型链接")
@pytest.mark.dependency(depends=["upload_image"])
def test_get_prototype(rq, value):
    rq(value)


@allure.story("创建设计图分组")
@pytest.mark.dependency(name="create_sector", depends=["upload_image"])
def test_sector(rq, value):
    rq(value)


@allure.story("重命名设计图分组")
@pytest.mark.dependency(depends=["create_sector"])
def test_rename_sector(rq, value):
    rq(value)


@allure.story("分组排序")
@pytest.mark.dependency(depends=["create_sector"])
def test_sector_sort(rq, value):
    rq(value)


@allure.story("获取项目分组")
@pytest.mark.dependency(depends=["create_sector"])
def test_get_project_sectors(rq, value):
    rq(value)


@allure.story("增删分组设计图")
@pytest.mark.dependency(depends=["create_sector"])
def test_change_sector(rq, value):
    rq(value)


@allure.story("删除设计图分组")
@pytest.mark.dependency(depends=["create_sector"])
def test_del_sector(rq, value):
    rq(value)


@allure.story("分组图片排序")
@pytest.mark.dependency(depends=["create_sector"])
def test_sector_image_sort(rq, value):
    rq(value)


@allure.story("创建文字卡片")
@pytest.mark.dependency(depends=["upload_image"])
def test_card(rq, value):
    rq(value)


@allure.story("删除设计图")
@pytest.mark.dependency(depends=["upload_image"])
def test_del_image(rq, value):
    rq(value)


@allure.story("上传文件")
@pytest.mark.dependency(name="upload_file", depends=["create_project"], scope="session")
def test_upload_file(rq, value):
    rq(value)


@allure.story("删除文件")
@pytest.mark.dependency(depends=["upload_file"])
def test_del_file(rq, value):
    rq(value)


@allure.story("搜索image")
@pytest.mark.dependency(depends=["upload_image"])
def test_search_image(rq, value):
    rq(value)


@allure.story("修改图片版本名称")
def test_update_version(rq, value):
    rq(value)


@allure.story("图片对比")
def test_image_contrast(rq, value):
    rq(value)


@allure.story("复制粘贴图片")
@pytest.mark.dependency(depends=["upload_image"])
def test_copyimage(rq, value):
    rq(value)


@allure.story("创建连线")
@pytest.mark.dependency(name="link", depends=["upload_image"])
def test_link(rq, value):
    rq(value)


@allure.story("删除连线")
@pytest.mark.dependency(depends=["link"])
def test_del_link(rq, value):
    rq(value)


@allure.story("连线说明")
@pytest.mark.dependency(depends=["link"])
def test_connection_explain(rq, value):
    rq(value)


@allure.story("创建评论")
@pytest.mark.dependency(name="comment", depends=["upload_file"])
def test_comment(rq, value):
    rq(value)


@allure.story("修改评论状态")
@pytest.mark.dependency(depends=["comment"])
def test_change_comment_status(rq, value):
    rq(value)


@allure.story("删除评论")
@pytest.mark.dependency(depends=["comment"])
def test_del_comment(rq, value):
    rq(value)


@allure.story("创建资源")
@pytest.mark.dependency(name="bookmark", depends=["create_project"], scope="session")
def test_bookmark(rq, value):
    rq(value)


@allure.story("获取资源")
@pytest.mark.dependency(depends=["bookmark"])
def test_get_bookmark(rq, value):
    rq(value)


@allure.story("修改资源")
@pytest.mark.dependency(depends=["bookmark"])
def test_put_bookmark(rq, value):
    rq(value)


@allure.story("删除资源")
@pytest.mark.dependency(depends=["bookmark"])
def test_del_bookmark(rq, value):
    rq(value)
