/**
 * 这个测试文件中的测试用例主要覆盖了拖拽相关的场景，包括:
 *     1) 各类 block 之间的相互拖拽
 *     2) database 表格内部/之间的拖拽
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

test.describe.serial('测试拖拽功能', () => {
  // 主站包含 TS 文档的页面对象
  let page;

  // TS 文档的 iframe 对象
  let frame;

  // 在所有测试用例执行前，运行一次
  test.beforeAll(async ({browser}) => {
    // 在所有测试用例启动前，进行登录
    page = await login(browser);

    // 在所有测试用例启动前，创建页面
    frame = await createDocument(createTitle('测试拖拽功能'), page);
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

  test('多 block 之间的拖拽', async () => {
    // 文本 block
    const text = '这是新建的文本 block。';
    const selectorParagraphBlock = '.ce-paragraph >> nth=0';
    await frame.fill(selectorParagraphBlock, text);
    await expect(frame.locator(selectorParagraphBlock)).toHaveText(text);

    // 分割线 block
    await frame.press(selectorParagraphBlock, 'Enter');
    await frame.fill('.ce-paragraph >> nth=1', '---');
    await frame.press('text=---', ' ');

    // 一级标题
    await createBlock('一级标题', frame);
    await frame.fill('.ce-header >> nth=0', '一级标题');

    // 二级标题
    await frame.press('.ce-header >> nth=0', 'Enter');
    await createBlock('二级标题', frame);
    await frame.fill('.ce-header >> nth=1', '二级标题');

    await frame.press('.ce-header >> nth=1', 'Enter');
    await frame.fill('.ce-paragraph >> nth=-1', '因为标题内回车有bug，因此换为文本block');

    // 模拟用户鼠标hover分割线block，触发6个点组件渲染(因为拖拽需要作用在6个点组件上)
    // let el;
    // let html;

    // 拖拽分割线 block 到三级标题的顶部
    await frame.hover('.ce-delimiter >> nth=0');
    await frame.waitForSelector('.ce-toolbar__actions');
    await frame.dragAndDrop(
        '.ce-toolbar__actions',
        '.ce-header >> nth=1',
        {
          force: true,
          noWaitAfter: true,
          sourcePosition: {x: 0, y: 0},
          targetPosition: {x: 0, y: 40},
        },
    );
    const el = await frame.locator('.ce-block__content >> nth=3');
    const html = await el.innerHTML();
    await expect(html).toContain('ce-delimiter');

    // 拖拽分割线 block 到原来的位置
    // TODO：这里失败的几率很高，等修复后再解注释
    /*
    await frame.hover('.ce-delimiter >> nth=0');
    await frame.waitForSelector('.ce-toolbar__actions');
    await frame.dragAndDrop(
        '.ce-toolbar__actions',
        '.ce-block >> nth=1',
        {
          force: true,
          noWaitAfter: true,
          sourcePosition: {x: 0, y: 0},
          targetPosition: {x: 0, y: -15},
        },
    );
    el = await frame.locator('.ce-block__content >> nth=1');
    html = await el.innerHTML();
    await expect(html).toContain('ce-delimiter');
    */
  });

  test('database的行和列拖拽', async () => {
    // 由于默认情况下：
    //    1）playwright 进行点击模拟时，要求被点击元素在 viewport 中可见，
    //       所以会预先滚动被点击元素，待其进入 viewport 后再进行点击模拟。
    //    2) 我们通过编辑器中前 3 个 block 左侧的 "+" 按钮唤起菜单后，
    //       playwright 会推动菜单面板将 "超级表格" 菜单项滚动到 viewport，
    //       由于无法滚动（这是我们程序的问题），这会导致测试用例执行失败。
    // 因此：
    //     测试用例在进行超级表格的测试时，在第 4 个 block 添加超级表格
    for (let i=0; i<3; i++) {
      await frame.press('.ce-paragraph >> nth=-1', 'Enter');
      await frame.fill(
          '.ce-paragraph >> nth=-1',
          'TODO: remove the block logic after fix the context toolbar bug.',
      );
    }
    await createBlock('超级表格', frame, '.ce-paragraph >> nth=-1');

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

    // 将第一行拖拽到第二行的位置
    /* TODO: 解决行拖拽的问题后解注释这里
    await frame.hover('text=main cell 0');
    await frame.waitForSelector('#rowToolIcon');
    await frame.dragAndDrop(
        '#rowToolIcon svg',
        'text=main cell 1',
        {
          force: true,
          noWaitAfter: true,
          sourcePosition: {x: 3, y:3},
          targetPosition: {x: 150, y: 25},
        },
    );
    const row = await frame.locator('.main-title >> nth=1');
    const html = await row.innerHTML();
    await expect(html).toContain('main cell 0');
    */

    // 将第二列拖拽到第一列的前面
    await frame.dragAndDrop(
        'revogr-header >> :nth-match(div:has-text("单选标签"), 2)',
        'revogr-header >> :nth-match(div:has-text("标题"), 2)',
        {
          force: true,
          noWaitAfter: true,
          sourcePosition: {x: 0, y: 0},
          targetPosition: {x: 0, y: 0},
        },
    );

    const col = await frame.locator('.data-header-cell >> nth=0');
    text = await col.innerText();
    await expect(text).toBe('单选标签');
  });
});
