/**
 * 这个测试文件中的测试用例主要覆盖了多人协作场景下数据的正确性
 *
 * 名单：
 *            1）数据广播
 *            2）虚拟光标
 *            3）用户头像
 */

const {test, expect} = require('@playwright/test');
const config = require('../config/playwright.config');
const {createChromiumBrowser} = require('../fixtures/browser');
const {createDesktopChromeContexts} = require('../fixtures/context');
const {
  loginWithUserA,
  loginWithUserB,
  loginWithUserC,
  loginWithUserD,
  loginWithUserE,
  loginWithUserF,
  loginWithUserG,
  loginWithUserH,
  loginWithUserI,
  loginWithUserJ,
  loginWithUserK,
  createTitle,
  createDocument,
  removeDocument,
  removeBlocks,
  getTsFrame,
} = require('../fixtures/page');
const {userEnv} = require('../config/env');
const userB = require(`../fixtures/users/${userEnv}/userB`);

test.describe.serial('测试多人协作场景下的功能', () => {
  // 测试用例自待的浏览器
  let defaultBrowser;

  // 浏览器实例列表
  const browsers = [];

  // 在所有测试用例执行前，运行一次
  test.beforeAll(async ({browser}) => {
    defaultBrowser = browser;
  });

  // 在所有测试用例执行后，运行一次
  test.afterAll(async () => {
    // 释放所有浏览器实例
    browsers.forEach(async (browser) => browser.close());
  });


  test('两个用户场景下，头像-广播数据-虚拟光标', async () => {
    // 创建用户A 的浏览器环境
    const [contextA] = await createDesktopChromeContexts(defaultBrowser);
    // 登录用户A
    const pageA = await loginWithUserA(contextA);
    // 创建用户B 的浏览器环境
    const browserForChrome = await createChromiumBrowser({
      headless: config.use.headless,
    });

    browsers.push(browserForChrome);

    const [contextB] = await createDesktopChromeContexts(browserForChrome);
    // 登录用户B
    const pageB = await loginWithUserB(contextB);
    // 页面标题
    const title = createTitle('两个用户场景下，头像-广播数据-虚拟光标');

    // 使用用户A 创建一个测试页面
    const frameA = await createDocument(title, pageA, '');

    // 用户B 不需要再次创建页面，只需要等到广播，并进入页面即可
    await pageB.goto(pageA.url());

    const frameB = await getTsFrame(pageB);

    // 用户头像
    // 断言用户头像个数正确
    await frameB.waitForSelector(`span:has-text("${ userB.name }")`);
    await expect(frameB.locator('.avatar')).toHaveCount(2);

    // 广播数据
    const content = '来自用户B的输入内容';
    const firstParagraphSelector = '.ce-paragraph >> nth=0';
    await frameB.waitForSelector(firstParagraphSelector);
    await frameA.fill(firstParagraphSelector, content);
    await frameB.waitForSelector(`text=${content}`);
    await expect(frameB.locator(firstParagraphSelector)).toHaveText(content);

    // 虚拟光标
    const userACursorSelector = '.ts_cursor';

    await Promise.all([
      // 将 userA 的光标移动到 block 尾部
      frameA.press(firstParagraphSelector, 'ArrowUp'),
      // 等待用户A的虚拟光标渲染完毕
      expect(frameB.locator(userACursorSelector)).toHaveCount(1),
    ]);

    // TODO: 虚拟光标定位功能有问题，修复后再开启测试用例
    // 断言虚拟光标位置正确
    // await expect(frameB.locator(firstCursorSelector))
    //  .toHaveCSS('left', '61px');
    // await expect(frameB.locator(firstCursorSelector))
    //  .toHaveCSS('top', '51px');

    // 清理新建的 block
    await removeBlocks(frameA);

    // 从导航树删除当前测试页面
    // 注意，两个用户访问的是同一个页面，随意只需要删除一次即可
    await removeDocument(frameA);

    // 在所有测试用例完成后，回收资源
    await Promise.all([
      pageA.close(),
      pageB.close(),
    ]);
  });

  test('11个用户场景下，头像列表收起和展开功能', async () => {
    // 浏览器较多，需要适当增加超时阈值
    test.setTimeout(15 * 60 * 1000);

    const pages = {};
    const loginFnList = {
      loginWithUserA,
      loginWithUserB,
      loginWithUserC,
      loginWithUserD,
      loginWithUserE,
      loginWithUserF,
      loginWithUserG,
      loginWithUserH,
      loginWithUserI,
      loginWithUserJ,
      loginWithUserK,
    };

    let frameA;

    const fnNameList = Object.keys(loginFnList);

    for (let i=0; i<fnNameList.length; i++) {
      const fnName = fnNameList[i];
      const index = fnName.split('loginWithUser')[1];
      const login = loginFnList[fnName];

      // 创建用户 C-K 的浏览器环境
      const browserForChrome = await createChromiumBrowser({
        headless: config.use.headless,
      });

      browsers.push(browserForChrome);

      const [context] = await createDesktopChromeContexts(browserForChrome);

      const name = `page` + index;
      // 登录用户B
      pages[name] = await login(context);
      const frame = await getTsFrame(pages[name]);

      if (index === 'A') frameA = frame;

      await frame.waitForSelector(`text=新建文档`);
    }

    await frameA.waitForSelector('text=4');
    await expect(frameA.locator('.avatar')).toHaveCount(7);
  });
});
