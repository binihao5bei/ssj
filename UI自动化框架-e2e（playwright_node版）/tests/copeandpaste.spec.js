/**
 * 这个测试文件中的测试用例主要覆盖了复制粘贴相关的场景，包括:
 *     1) 各类 block 之间的复制粘贴
 *     2) 来自外部内容的复制粘贴
 */

const {test, expect} = require('@playwright/test');
const {createDesktopChromeContexts} = require('../fixtures/context');
const {
  loginWithUserA,
  createTitle,
  createDocument,
  removeDocument,
  createBlock,
  removeBlocks,
} = require('../fixtures/page');

// 模拟用户登录的函数
const login = async (browser) => {
  // 使用桌面 Chrome 浏览器环境
  const [context] = await createDesktopChromeContexts(browser);

  return loginWithUserA(context);
};

test.describe.serial('测试复制粘贴功能', () => {
  // 主站包含 TS 文档的页面对象
  let page;

  // TS 文档的 iframe 对象
  let frame;

  // 在所有测试用例执行前，运行一次
  test.beforeAll(async ({browser}) => {
    // 在所有测试用例启动前，进行登录
    page = await login(browser);

    // 在所有测试用例启动前，创建页面
    frame = await createDocument(createTitle('测试复制粘贴功能'), page);
  });

  // 在所有测试用例执行后，运行一次
  test.afterAll(async () => {
    // 从导航树删除当前测试页面
    await removeDocument(frame);
    // 在所有测试用例完成后，回收资源
    await page.close();
  });

  // 在每个测试用例执行后，运行一次
  test.afterEach(async () => {
    // 清理新建的 block
    await removeBlocks(frame);
  });

  // 通过六个点来执行操作
  const actByMenu = async (selector, action) => {
    const switchSelector = '.ce-toolbar__actions';

    await frame.hover(selector);
    await frame.waitForSelector(switchSelector);
    await frame.click(switchSelector);
    await frame.waitForSelector('.menu');
    await frame.click(`text=${action}`);
  };
  // 通过六个点来复制
  const copeByMenu = async (selector) => actByMenu(selector, '复制+');
  // 通过六个点来粘贴
  const pasteByMenu = async (selector) => actByMenu(selector, '粘贴+');

  test('复制粘贴文本 block', async () => {
    const text = '这是新建的文本 block。';
    const firstBlockSelector = '.ce-paragraph >> nth=0';

    await frame.fill(firstBlockSelector, text);
    await frame.press(firstBlockSelector, 'Enter');
    await frame.press(firstBlockSelector, 'Enter');
    await expect(frame.locator(firstBlockSelector)).toHaveText(text);
    await copeByMenu(firstBlockSelector);

    const secondBlockSelector = '.ce-paragraph >> nth=1';

    await pasteByMenu(secondBlockSelector);
    await expect(frame.locator(secondBlockSelector)).toHaveText(text);
  });

  test('复制粘贴一级标题 block', async () => {
    const firstHeadBlockSelector = '.ce-header >> nth=0';

    await createBlock('一级标题', frame);
    await frame.fill(firstHeadBlockSelector, '一级标题');
    await frame.press(firstHeadBlockSelector, 'Enter');

    const firstCopeSelector = '.ce-paragraph >> nth=1';

    await copeByMenu(firstHeadBlockSelector);
    await pasteByMenu(firstCopeSelector);
    await expect(frame.locator('.ce-header >> nth=1')).toHaveText('一级标题');
  });

  test('复制粘贴二级标题 block', async () => {
    const firstHeadBlockSelector = '.ce-header >> nth=0';

    await createBlock('二级标题', frame);
    await frame.fill(firstHeadBlockSelector, '二级标题');
    await frame.press(firstHeadBlockSelector, 'Enter');

    const firstCopeSelector = '.ce-paragraph >> nth=1';

    await copeByMenu(firstHeadBlockSelector);
    await pasteByMenu(firstCopeSelector);
    await expect(frame.locator('.ce-header >> nth=1')).toHaveText('二级标题');
  });

  test('复制粘贴三级标题 block', async () => {
    const firstHeadBlockSelector = '.ce-header >> nth=0';

    await createBlock('三级标题', frame);
    await frame.fill(firstHeadBlockSelector, '三级标题');
    await frame.press(firstHeadBlockSelector, 'Enter');

    const firstCopeSelector = '.ce-paragraph >> nth=1';

    await copeByMenu(firstHeadBlockSelector);
    await pasteByMenu(firstCopeSelector);
    await expect(frame.locator('.ce-header >> nth=1')).toHaveText('三级标题');
  });

  test('复制粘贴无序列表 block', async () => {
    const firstBlockSelector = '.cdx-nested-list >> nth=0';
    const text = '这是无序列表的内容';

    await createBlock('无序列表', frame);
    await frame.fill(firstBlockSelector, text);
    await frame.press(firstBlockSelector, 'Enter');
    await frame.type(firstBlockSelector, text, {delay: 100});
    await frame.press(firstBlockSelector, 'Enter');
    await frame.press(firstBlockSelector, 'Enter');

    const firstCopeSelector = '.ce-paragraph >> nth=1';

    await copeByMenu(firstBlockSelector);
    await pasteByMenu(firstCopeSelector);
    await expect(frame.locator('.cdx-nested-list >> nth=1'))
        .toHaveText(text + text);
  });

  test('复制粘贴有序列表 block', async () => {
    const firstBlockSelector = '.cdx-nested-list >> nth=0';
    const text = '这是有序列表的内容';

    await createBlock('有序列表', frame);
    await frame.fill(firstBlockSelector, text);
    await frame.press(firstBlockSelector, 'Enter');
    await frame.type(firstBlockSelector, text, {delay: 100});
    await frame.press(firstBlockSelector, 'Enter');
    await frame.press(firstBlockSelector, 'Enter');

    const firstCopeSelector = '.ce-paragraph >> nth=1';

    await copeByMenu(firstBlockSelector);
    await pasteByMenu(firstCopeSelector);
    await expect(frame.locator('.cdx-nested-list >> nth=1'))
        .toHaveText(text + text);
  });

  test('复制粘贴普通表格 block', async () => {
    const firstCopeSelector = '.ce-paragraph >> nth=1';

    await frame.press('.ce-paragraph >> nth=0', 'Enter');
    await frame.press(firstCopeSelector, 'Enter');
    await createBlock('普通表格', frame);
    // 等待普通表格 DOM 渲染完毕
    await frame.waitForSelector('.tc-table');

    const cells = await frame.$$('.tc-cell');

    for (let i=0; i<cells.length; i++) {
      const selector = `.tc-cell >> nth=${i}`;
      const content = `cell ${i}`;
      // 在单元格中输入内容
      await frame.fill(selector, content);
      // 断言内容正确更新到 DOM
      await expect(frame.locator(selector)).toHaveText(content);
    }

    const firstBlockSelector = '.tc-table >> nth=0';
    const expected = 'cell 0cell 1cell 2cell 3cell 4cell 5cell 6cell 7cell 8';

    await frame.hover(firstBlockSelector);
    await frame.waitForSelector('text=普通表格');
    await frame.click('text=普通表格');
    await frame.waitForSelector('.menu');
    await frame.click('text=复制+');
    await pasteByMenu(firstCopeSelector);
    await expect(frame.locator('.tc-table >> nth=0')).toHaveText(expected);
  });

  test('复制粘贴超级表格 block', async () => {
    for (let i=0; i<5; i++) {
      await frame.press('.ce-paragraph >> nth=-1', 'Enter');
    }

    await createBlock('超级表格', frame);

    // 断言超级表格更新到 DOM
    await expect(frame.locator('.ce-database revo-grid')).toBeVisible();

    // 输入超级表格的标题
    const title = `e2e 超级表格`;
    const selector = '[placeholder="表格名称"]';
    const locator = frame.locator(selector);
    await frame.fill(selector, title);
    // 断言超级表格标题的文字正确更新到 DOM
    // 由于超级表格标题的 DOM 是 input，因此这里使用 toHaveValue 方法进行断言
    await expect(locator).toHaveValue(title);
    // 断言超级表格标题的文字样式为粗体
    await expect(locator).toHaveCSS('font-weight', '700');

    // 获取所有的默认标题单元格元素
    const mailCellList = await frame.$$('.main-cell');

    // 输入超级表格所有标题单元格的内容（不涉及子页面弹层）并断言正确性
    for (let i=0; i<mailCellList.length; i++) {
      const currentCellSelector = `.main-cell >> nth=${i}`;
      const currentCellContent = `main cell ${i}`;
      // 点击标题单元格，进入编辑模式
      await frame.click(currentCellSelector);
      // 等待编辑模式 DOM 渲染完毕
      await frame.waitForSelector('.main-cell-editor');

      const editorSelector = '.main-cell-editor';
      // 在编辑模式 DOM 中输入内容
      await frame.fill(editorSelector, currentCellContent);
      // 模拟用户敲下回车键，保存输入的内容
      await frame.press(editorSelector, 'Enter');
      // 断言内容正确更新到 DOM
      await expect(frame.locator(`text=${currentCellContent}`)).toBeVisible();
    };

    // 获取所有的默认单选单元格元素
    const selectCellList = await frame.$$('.select-cell');

    // 输入超级表格所有单选单元格的内容，并断言正确性
    for (let i=0; i<selectCellList.length; i++) {
      const currentCellSelector = `.select-cell >> nth=${i}`;
      const currentCellContent = `select cell ${i}`;
      // 点击单选单元格，进入编辑模式
      await frame.click(currentCellSelector);
      // 等待编辑模式 DOM 渲染完毕
      await frame.waitForSelector('.select-wrapper');

      const editorSelector = '[placeholder="搜索或创建选项"]';
      // 在编辑模式 DOM 中输入内容
      await frame.fill(editorSelector, currentCellContent);
      // 模拟用户敲下回车键，保存输入的内容
      await frame.press(editorSelector, 'Enter');
      // 段元内容正确更新到 DOM
      await expect(frame.locator(`text=${currentCellContent}`)).toBeVisible();
    };

    const firstCopeSelector = '.ce-paragraph >> nth=1';
    const firstBlockSelector = 'revo-grid >> nth=0';
    const expected = '添加行搜索排序设置排序条件添加条件 标题 '+
      '单选标签main cell 0 打开select cell 0main cell 1 打开select cell 1main '+
      'cell 2 打开select cell 2 打开select cell 3添加一行⇧ + 滚轮也能左右滚动';
    const switchSelector = '.ce-toolbar__actions--opened';
    await frame.waitForSelector(switchSelector);
    // 注意，这里的两次 dblclick 是必须的，否则无法展示复制弹窗面板
    await frame.dblclick(switchSelector);
    await frame.dblclick(switchSelector);
    await frame.waitForSelector('.menu');
    await frame.click(`text=复制+`);
    await pasteByMenu(firstCopeSelector);
    await expect(frame.locator(firstBlockSelector)).toHaveText(expected);
  });
});
