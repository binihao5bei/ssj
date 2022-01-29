/**
 * 这个测试文件中的测试用例主要是测试行内文本
 *
 *
 *            1）加粗、删除、颜色、背景色、链接
 *            2）改变block类型-标题（h1、h2、h3）-列表（有序无序）-待办事项
 */

const {test, expect} = require('@playwright/test');
const {createDesktopChromeContexts} = require('../fixtures/context');
const {
  loginWithUserA,
  createTitle,
  createDocument,
  removeDocument,
  removeBlocks,
  selectInlineText,
} = require('../fixtures/page');

// 模拟用户登录的函数
const login = async (browser) => {
  // 使用桌面 Chrome 浏览器环境
  const [context] = await createDesktopChromeContexts(browser);

  return loginWithUserA(context);
};

const inlineToHeader = async (frame, level, defaultText) => {
  const map = {
    1: {selector: '.lanhu-inline-heading1', fontSize: '28px'},
    2: {selector: '.lanhu-inline-heading2', fontSize: '22px'},
    3: {selector: '.lanhu-inline-heading3', fontSize: '18px'},
  };
  const selector = map[level].selector;
  const fontSize = map[level].fontSize;


  await frame.click(selector);

  const locator = frame.locator('.ce-header >> nth=0');
  // 断言内容正确更新到 DOM
  await expect(locator).toHaveText(defaultText);
  // 断言字体大小为正确的样式
  await expect(locator).toHaveCSS('font-size', fontSize);
};


test.describe.serial('测试行内文本', () => {
  // 主站包含 TS 文档的页面对象
  let page;

  // TS 文档的 iframe 对象
  let frame;

  // 创建的行内文本文字
  const defaultText = '测试行内文本样式内容';

  // 在所有测试用例执行前，运行一次
  test.beforeAll(async ({browser}) => {
    // 在所有测试用例启动前，进行登录
    page = await login(browser);

    // 在所有测试用例启动前，创建页面
    frame = await createDocument(createTitle('测试全部 block 增删改功能'), page);
  });

  // 在所有测试用例执行后，运行一次
  test.afterAll(async () => {
    // 从导航树删除当前测试页面
    await removeDocument(frame);
    // 在所有测试用例完成后，回收资源
    await page.close();
  });

  // 在每个测试用例执行前，运行一次
  test.beforeEach(async () => {
    // 创建一个新的 block
    await frame.press('.ce-block [contenteditable="true"]', 'Enter');
    // 模拟用户在默认文本 block 输入文字内容
    await frame.fill('.ce-paragraph >> nth=-1', defaultText);
  });

  // 在每个测试用例执行后，运行一次
  test.afterEach(async () => {
    // 清理新建的 block
    await removeBlocks(frame);
  });

  test('行内文本加粗', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);

    await frame.click('.ce-inline-tool.ce-inline-tool--bold');
    // 文本内容的选择器
    const locator = frame.locator('b');
    // 断言b标签样式正确
    await expect(locator).toBeVisible();
    // 断言内容正确更新到 DOM
    await expect(locator).toHaveText(defaultText);
  });

  test('行内文本加删除线', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);

    await frame.click('.lanhu-inline-strikethrough');
    // 文本内容的选择器
    const locator = frame.locator('s');
    await expect(locator).toBeVisible();
    // 断言内容正确更新到 DOM
    await expect(locator).toHaveText(defaultText);
  });

  test('行内文本加字体颜色', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);

    await frame.click('.lanhu_colour_picker');
    await frame.waitForSelector('.font_colour_orange');
    await frame.click('.font_colour_orange');

    const locator = frame.locator(`text=${defaultText}`);
    // 断言字体大小为正确的样式
    await expect(locator).toHaveClass('font_colour_orange');
  });

  test('行内文本加字体背景颜色', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);

    await frame.click('.lanhu_colour_picker');
    await frame.click('.bg_colour_red');

    const locator = frame.locator(`text=${defaultText}`);
    // 断言字体大小为正确的样式
    await expect(locator).toHaveClass('bg_colour_red');
  });

  test('行内文本加链接', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);

    await frame.click('button:nth-child(8)');
    await frame.fill('#link_input_href', 'https://www.baidu.com/');
    await frame.press('#link_input_href', 'Enter');

    const locator = frame.locator(`text=${defaultText}`);
    // 断言字体大小为正确的样式
    await expect(locator).toHaveAttribute('href', 'https://www.baidu.com/');
  });

  test('行内文本转化为一级标题', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);
    await inlineToHeader(frame, 1, defaultText);
  });

  test('行内文本转化为二级标题', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);
    await inlineToHeader(frame, 2, defaultText);
  });

  test('行内文本转化为三级标题', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);
    await inlineToHeader(frame, 3, defaultText);
  });

  test('行内文本转化为有序列表', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);

    await frame.click('.lanhu-inline-list-ordered');


    const selector = '.cdx-nested-list--ordered >> nth=0';
    // 断言列表的内容正确
    await expect(frame.locator(selector)).toHaveText(defaultText);
    await expect(frame.locator('.cdx-nested-list__item >> nth=0'))
        .toHaveAttribute('style', '--order-list-style:decimal;');
  });

  test('行内文本转化为无序列表', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);

    await frame.click('.lanhu-inline-list-unordered');


    const selector = '.cdx-nested-list--unordered >> nth=0';
    // 断言列表的内容正确
    await expect(frame.locator(selector)).toHaveText(defaultText);
    await expect(frame.locator('.cdx-nested-list__item >> nth=0'))
        .toHaveAttribute('style', '--unordered-list-style:"•";');
  });

  test('行内文本转化为待办事项', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);

    await frame.click('.lanhu-inline-list-todo');

    // 模拟用户勾选第一个待办事项
    await frame.click('.cdx-checklist__item-checkbox >> nth=0');
    // 断言第一个待办事项勾选状态正确
    await expect(frame.locator('.cdx-checklist >> nth=0'))
        .toHaveClass(/cdx-checklist__item--checked/);
  });


  test('行内文本加多个样式重叠', async () => {
    // 模拟键盘操作选中文本block
    await selectInlineText(frame, defaultText);
    // 加粗
    await frame.click('.ce-inline-tool.ce-inline-tool--bold');
    // 斜体
    await frame.click('.lanhu-inline-strikethrough');


    // 文本内容的选择器
    const locator = frame.locator('b');
    // 断言b标签样式正确
    await expect(locator).toBeVisible();
    // 断言s标签样式正确
    await expect(frame.locator('s')).toBeVisible();
  });
});

