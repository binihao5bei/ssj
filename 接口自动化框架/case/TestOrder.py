import allure
import pytest


@allure.story("获取team_service")
@pytest.mark.dependency(depends=["create_team"], scope="session")
def test_team_service(rq, value):
    rq(value)


@allure.story("修改团队服务信息")
@pytest.mark.dependency(depends=["create_team"], scope="session")
def test_put_team_service(rq, value):
    rq(value)


@allure.story("获取team_service")
@pytest.mark.dependency(depends=["create_team"], scope="session")
def test_expire_notice(rq, value):
    rq(value)


@allure.story("获取订单列表")
@pytest.mark.dependency(depends=["create_team"], scope="session")
def test_order_list(rq, value):
    rq(value)


@allure.story("获取套餐信息")
@pytest.mark.dependency(depends=["create_team"], scope="session")
def test_business_package(rq, value):
    rq(value)


@allure.story("创建订单")
@pytest.mark.dependency(name="create_order", depends=["create_team"], scope="session")
def test_create_order(rq, value):
    rq(value)


@allure.story("取消订单")
@pytest.mark.dependency(depends=["create_order"])
def test_cancel_order(rq, value):
    rq(value)


@allure.story("合同")
@pytest.mark.dependency(depends=["create_order"])
def test_contract(rq, value):
    rq(value)


@allure.story("获取历史开票信息")
@pytest.mark.dependency(depends=["create_order"])
def test_invoiceInfo(rq, value):
    rq(value)


@allure.story("获取税号信息")
@pytest.mark.dependency(depends=["create_order"])
def test_company_info(rq, value):
    rq(value)


@allure.story("开发票")
@pytest.mark.dependency(depends=["create_order"])
def test_invoice(rq, value):
    rq(value)
