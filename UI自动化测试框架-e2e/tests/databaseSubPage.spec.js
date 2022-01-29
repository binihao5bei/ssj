/**
 * 这个测试文件中的测试用例主要是对database子页面相关的场景进行模拟,包含:
 *            1）展开子页面
 *            2）子页面title emoji
 */

const {test, expect} = require('@playwright/test');
const {createDesktopChromeContexts} = require('../fixtures/context');
const {
  loginWithUserB,
  createTitle,
  createDocument,
  createBlock,
} = require('../fixtures/page');

// 模拟用户登录的函数
const login = async (browser) => {
  // 使用桌面 Chrome 浏览器环境
  const [context] = await createDesktopChromeContexts(browser);

  return loginWithUserB(context);
};


test.describe.serial('测试database子页面相关场景', () => {
  // 主站包含 TS 文档的页面对象
  let page;

  // TS 文档的 iframe 对象
  let frame;

  // 在所有测试用例执行前，运行一次
  test.beforeAll(async ({browser}) => {
    // 在所有测试用例启动前，进行登录
    page = await login(browser);

    // 在所有测试用例启动前，创建页面
    frame = await createDocument(createTitle('测试database子页面相关场景'), page);
  });

  // 在所有测试用例执行后，运行一次
  test.afterAll(async () => {
    // 从导航树删除当前测试页面
    await frame.click(`#ts-tree li >> nth=1`, {button: 'right'});
    await frame.click('.tree-menu .text-red');
    const confirmButtonClass = 'button :text("是")';
    await frame.waitForSelector(confirmButtonClass);
    await frame.click(confirmButtonClass);
    // 在所有测试用例完成后，回收资源
    await page.close();
  });

  test('超级表格 block', async () => {
    // 直接enter 会有概率出现undefined 且新建blocks失败
    await frame.click('.ce-paragraph >> nth=0', {delay: 1000});
    // 左侧加号弹窗不在视窗里显示 无法选中超级表格 多建几个空白block
    for (let i=0; i<6; i++) {
      await frame.press(`.ce-paragraph >> nth=-1`, 'Enter');
    }
    await createBlock('超级表格', frame, '.ce-paragraph >> nth=4');
    // 断言超级表格更新到 DOM
    await expect(frame.locator('.ce-database revo-grid')).toBeVisible();
    // 添加列弹窗无法滚动显示不全 多建几个空白block 把database顶到页面上半部分
    for (let i=0; i<4; i++) {
      await frame.press('.ce-paragraph >> nth=-1', 'Enter');
    }
  });

  test('超级表格 添加列', async () => {
    // 添加初始不包含的三类database列
    for (let i = 1; i<=4; i++) {
      if (i === 2) continue;
      await frame.click('.column-plus.data-header-cell');
      await frame.waitForSelector('.column-add-dialog');
      await frame.click('.select-type');
      await frame.waitForSelector('.column-selects');
      await frame.click(`.select-type >> nth = ${i}`);
      await frame.click('.operator-item.confirm');
    }
    // 断言正常添加了列
    for (let i = 0; i<5; i++) {
      await expect(frame.locator(`.data-header-cell >> nth = ${i}`)).toBeVisible();
    }
  });

  test('超级表格 填充行内容', async () => {
    // 点击标题单元格，进入编辑模式
    await frame.click(`[data-col='0'][data-row='0']`);
    // 等待编辑模式 DOM 渲染完毕
    await frame.waitForSelector('.main-cell-editor');
    // 在编辑模式 DOM 中输入内容
    await frame.fill('.main-cell-editor', `main cell 0`);
    // 模拟用户敲下回车键，保存输入的内容
    await frame.press('.main-cell-editor', 'Enter');
    // 断言内容正确更新到 DOM
    await expect(frame.locator(`text='main cell 0'`)).toBeVisible();

    // 填充其他列数据
  });

  test('超级表格 打开弹层', async () => {
    const emoji = 'sweat_smile';
    const emojiCode ='1f605';
    // hover标题单元格
    await frame.hover(`[data-col='0'][data-row='0']`);
    // 展开弹层
    await frame.click('.main-open-button');
    // 断言弹层正常显示
    await expect(frame.locator(`.sub-document`)).toBeVisible();
    // 断言标题正常显示
    await expect(frame.locator(`.sub-document #title`)).toHaveText('main cell 0');
    // 断言弹层头部的信息栏正常显示
    for (let i = 0; i<4; i++) {
      await expect(frame.locator(`.database-cell >> nth = ${i}`)).toBeVisible();
    }
    // 悬停标题 等待添加emoji按钮动画
    await frame.hover(`.sub-document #title`);
    // 添加emoji
    await frame.click('.sub-document .add-page-icon');
    // 断言emoji正常显示
    await expect(frame.locator(`.emoji-preview`)).toBeVisible();
    // 打开编辑emoji的弹窗 选择emoji
    await expect(frame.locator(`.emoji-preview`)).toBeVisible();
    await frame.click('.emoji-preview');
    await frame.waitForSelector('.emoji-mart.emoji-mart-static.emoji-modal');
    await frame.click(`[data-title="${emoji}"]`);
    await frame.click('.emoji-picker-modal', {delay: 1000});

    // TODO: emoji比对 e2e和实际线上环境dom不一致
    // const locator = await page.locator(`.sub-document use`);
    // await expect(locator).toHaveAttribute('xlink:href', '/sprite.symbol.svg#'+emojiCode);

    // 展开子页面
    await frame.click('.unfold-button');
    // 断言弹层关闭
    await expect(frame.locator(`.sub-document`)).toBeHidden();
    // 断言展开页面的标题正常显示
    await expect(frame.locator(`#title`)).toHaveText('main cell 0');
    // 断言展开页面头部的信息栏正常显示
    for (let i = 0; i<4; i++) {
      await expect(frame.locator(`.database-cell >> nth = ${i}`)).toBeVisible();
    }
    // 返回父级文档
    await frame.click('.bread-name >> nth=0');
  });
});
