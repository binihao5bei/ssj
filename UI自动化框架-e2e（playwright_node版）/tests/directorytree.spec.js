/**
 * 这个测试文件中的测试用例主要是测试目录树
 *
 *
 *            1）新建父级文档、创建子级文档、创建同级文档
 *            2）拖拽文档
 *            3）搜索文档
 *            4）删除文档
 *
 */

const {test, expect} = require('@playwright/test');

const {createDesktopChromeContexts} = require('../fixtures/context');
const {
  loginWithUserA,
  createDocument,
  createSubDocument,
  removeTreeDocument,
  nowTime,
  searchDocument,
  // removeBlocks,
} = require('../fixtures/page');

// 模拟用户登录的函数
const login = async (browser) => {
  // 使用桌面 Chrome 浏览器环境
  const [context] = await createDesktopChromeContexts(browser);

  return loginWithUserA(context);
};


test.describe.serial('测试目录树', () => {
  // 主站包含 TS 文档的页面对象
  let page;

  // TS 文档的 iframe 对象
  let frame;

  // 创建的默认文档名称
  const defaultTitle = `[${nowTime()}树]`;

  // 在所有测试用例执行前，运行一次
  test.beforeAll(async ({browser}) => {
    // 在所有测试用例启动前，进行登录
    page = await login(browser);

    // 在所有测试用例启动前，创建页面
    frame = await createDocument(defaultTitle, page);
  });

  // 在所有测试用例执行后，运行一次
  test.afterAll(async () => {
    // 从导航树删除当前测试页面
    await removeTreeDocument(frame, `[data-name="${defaultTitle}"]`);
    // 在所有测试用例完成后，回收资源
    await page.close();
  });

  test('创建子文档,删除文档', async () => {
    const sunnames = [];
    const grandsunNames = [];

    // 依次创建层级文档 A-(B1\B2)-(B11\B12)(B21\B22)
    for (let i=1; i< 3; i++) {
      await createSubDocument(
          frame,
          `text=${defaultTitle}`,
          1,
          `二级${i}`,
      );
      await frame.waitForSelector(`text=二级${i}`);
      sunnames.push(`二级${i}`);
    };
    for (let j=0; j< sunnames.length; j++) {
      for (let k=1; k< 3; k++) {
        await createSubDocument(
            frame,
            `text=${sunnames[j]}`,
            1,
            `三级${j+1}${k}`,
        );
        await frame.waitForSelector(`text=三级${j+1}${k}`);
        grandsunNames.push(`三级${j+1}${k}`);
      };
    };
    // 拖拽文档

    await frame.dragAndDrop(`text=${grandsunNames[2]}`, `text=${sunnames[0]}`);
    // 搜索文档
    await searchDocument(frame, grandsunNames[1]);
    // 断言搜索有结果
    await expect(frame.locator('ts-tree-search-empty')).toBeHidden();
    // 关闭搜索弹窗
    await frame.click('.el-icon-error', {delay: 200});
    // 鼠标回到目录树页面
    await frame.click(`text=${grandsunNames[2]}`, {delay: 200});

    // 依次删除创建的文档
    for (let m=0; m<grandsunNames.length; m++) {
      await removeTreeDocument(frame, `[data-name="${grandsunNames[m]}"]`);
    };
    // 依次删除创建的文档
    for (let n=0; n<sunnames.length; n++) {
      await removeTreeDocument(frame, `[data-name="${sunnames[n]}"]`);
    };
  });
});

