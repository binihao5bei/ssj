/**
 * 这个测试文件中的测试用例主要是对后端接口调用的场景进行模拟，防止跨域问题出现
 *
 *
 *            1）分享场景
 *            2）获取用户信息相关场景
 *            3）搜索场景
 *            4）上传图片场景
 *            5）回收站场景（后期补充）
 */

const {test, expect} = require('@playwright/test');
const {createDesktopChromeContexts} = require('../fixtures/context');
const {
  loginWithUserB,
  createTitle,
  createDocument,
  removeDocument,
  shareDocument,
  searchDocument,
  removeBlocks,
  createBlock,
} = require('../fixtures/page');
const {userEnv} = require('../config/env');
const userB = require(`../fixtures/users/${userEnv}/userB`);
// 测试上传图片的文件路径
const uploadImagePath = 'fixtures/images/sample.jpeg';

// 模拟用户登录的函数
const login = async (browser) => {
  // 使用桌面 Chrome 浏览器环境
  const [context] = await createDesktopChromeContexts(browser);

  return loginWithUserB(context);
};


test.describe.serial('测试跨域场景', () => {
  // 主站包含 TS 文档的页面对象
  let page;

  // TS 文档的 iframe 对象
  let frame;

  // 在所有测试用例执行前，运行一次
  test.beforeAll(async ({browser}) => {
    // 在所有测试用例启动前，进行登录
    page = await login(browser);

    // 在所有测试用例启动前，创建页面
    frame = await createDocument(createTitle('测试跨域场景'), page);
  });

  // 在所有测试用例执行后，运行一次
  test.afterAll(async () => {
    // 从导航树删除当前测试页面
    await removeDocument(frame);
    // 在所有测试用例完成后，回收资源
    await page.close();
  });

  // // 在每个测试用例执行前，运行一次
  // test.beforeEach(async () => {
  //     // 创建一个新的 block
  //     await frame.press('.ce-block [contenteditable="true"]', 'Enter');
  //     // 模拟用户在默认文本 block 输入文字内容
  //     await frame.fill('.ce-paragraph >> nth=-1', defaultText);
  // });
  //
  // // 在每个测试用例执行后，运行一次
  // test.afterEach(async () => {
  //     // 清理新建的 block
  //     await removeBlocks(frame);
  // });

  test('文档分享场景/获取团队详情接口', async () => {
    await shareDocument(frame);
  });

  test('获取用户信息场景', async () => {
    // 点击文档右上角用户头像
    await frame.hover('.my-avatar > .name_avatar');
    // 等待hover后的用户名称，邮箱正确
    await frame.waitForSelector('.avatar-tooltip');
    // 断言邮箱信息正确
    await expect(frame.locator('.avatar-tooltip  .tooltip-email'))
        .toHaveText(userB.email);
  });

  test('搜索场景', async () => {
    // 搜索文档
    await searchDocument(frame, '测试跨域场景');
    // 断言搜索有结果
    await expect(frame.locator('ts-tree-search-empty')).toBeHidden();
    // 关闭搜索弹窗
    await frame.click('.el-icon-error', {delay: 200});
  });

  test('上传图片场景', async () => {
    // 创建一个新的 block
    await frame.press('.ce-block [contenteditable="true"]', 'Enter');

    // 捕获动态创建的 input[type="file"] 元素，并劫持 filechooser 事件
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser'),
      createBlock('图片', frame),
    ]);

    // 上传测试图片
    await fileChooser.setFiles(uploadImagePath);

    const selector = '.cdx-simple-image__picture img';
    // 等待图片预览 DOM 渲染完毕
    await frame.waitForSelector(selector);
    // 断言图片上传成功
    await expect(frame.locator(selector)).toBeVisible();
    // 断言图片宽度样式正确
    await expect(frame.locator(selector)).toHaveAttribute('data-width', '610');

    // 清理新建的 block
    await removeBlocks(frame);
  });
});

