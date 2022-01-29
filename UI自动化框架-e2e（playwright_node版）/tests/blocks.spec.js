/**
 * 这个测试文件中的测试用例主要覆盖了当前所有类型 block 基本操作的正确性（增加、简单编辑、删除）
 *
 * block 名单：
 *            1）文本
 *            2）图片
 *            2）标题（包含一级、二级、三级标题）
 *            3）列表（包含无序、有序列表）
 *            4）分割线
 *            5）特殊说明
 *            6）待办事项
 *            7）普通表格
 *            8）超级表格
 *            9）蓝湖设计图
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
const {userEnv} = require('../config/env');


const {
  // 测试蓝湖设计图 block 所使用的蓝湖主站的项目地址
  lanhuProjectURL,
  // 测试蓝湖设计图 block 所使用的蓝湖主站的项目名称
  lanhuProjectName,
} = require(`../fixtures/users/${userEnv}/userA`);

// 测试上传图片的文件路径
const uploadImagePath = 'fixtures/images/sample.jpeg';

// 模拟用户登录的函数
const login = async (browser) => {
  // 使用桌面 Chrome 浏览器环境
  const [context] = await createDesktopChromeContexts(browser);

  return loginWithUserA(context);
};

// 模拟用户点击 block 左侧 "+"，创建标题 block
const testHeaderBlock = async (level, frame) => {
  const map = {
    1: {title: '一级标题', fontSize: '28px'},
    2: {title: '二级标题', fontSize: '22px'},
    3: {title: '三级标题', fontSize: '18px'},
  };
  const title = map[level].title;
  const fontSize = map[level].fontSize;

  await createBlock(title, frame);

  const text = `这是新建的${title} block。`;
  const selector = '.ce-header >> nth=0';
  const locator = frame.locator(selector);

  // 在新创建的标题 block 中输入内容
  await frame.fill(selector, text);
  // 断言内容正确更新到 DOM
  await expect(locator).toHaveText(text);
  // 断言字体大小为正确的样式
  await expect(locator).toHaveCSS('font-size', fontSize);
};

// 模拟用户添加无序/有序列表项并输入内容
const testListBlock = async ({ordered = false}, frame) => {
  await createBlock(ordered ? '有序列表' : '无序列表', frame);
  const textList = ['item-a', 'item-b', 'item-c'];

  // 在新建的列表 block 中输入内容
  for (let i=0; i<textList.length; i++) {
    const selector = `.cdx-nested-list__item-content >> nth=${i}`;
    await frame.fill(selector, textList[i]);

    // 输入最后一项内容后，不必再按下回车键
    if (i < textList.length - 1) await frame.press(selector, 'Enter');
  };

  const selector = `.cdx-nested-list--${ordered ? '' : 'un'}ordered >> nth=0`;
  // 断言列表的内容正确
  await expect(frame.locator(selector)).toHaveText(textList.join(''));
  const style = ordered ?
    '--order-list-style:decimal;' : '--unordered-list-style:"•";';

  // 断言列表项的个数正确
  await expect(frame.locator('.cdx-nested-list__item'))
      .toHaveCount(textList.length);

  // 断言列表每个项的符号正确
  for (let i=0; i<textList.length; i++) {
    await expect(frame.locator(`.cdx-nested-list__item >> nth=${i}`))
        .toHaveAttribute('style', style);
  }
};

test.describe.serial('测试全部 block 增删改功能', () => {
  // 主站包含 TS 文档的页面对象
  let page;

  // TS 文档的 iframe 对象
  let frame;

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
  });

  // 在每个测试用例执行后，运行一次
  test.afterEach(async () => {
    // 清理新建的 block
    await removeBlocks(frame);
  });

  test('超级表格 block', async () => {
    // 由于默认情况下：
    //    1）playwright 进行点击模拟时，要求被点击元素在 viewport 中可见，
    //       所以会预先滚动被点击元素，待其进入 viewport 后再进行点击模拟。
    //    2) 我们通过编辑器中前 3 个 block 左侧的 "+" 按钮唤起菜单后，
    //       playwright 会推动菜单面板将 "超级表格" 菜单项滚动到 viewport，
    //       由于无法滚动（这是我们程序的问题），这会导致测试用例执行失败。
    // 因此：
    //     测试用例在进行超级表格的测试时，在第 4 个 block 添加超级表格
    for (let i=0; i<2; i++) {
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
  });

  test('普通表格 block', async () => {
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
  });

  test('图片 block', async () => {
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
  });

  // test('蓝湖设计图 block', async () => {
  //   // 由于默认情况下：
  //   //    1）playwright 进行点击模拟时，要求被点击元素在 viewport 中可见，
  //   //       所以会预先滚动被点击元素，待其进入 viewport 后再进行点击模拟。
  //   //    2) 我们通过编辑器中前 5 个 block 左侧的 "+" 按钮唤起菜单后，
  //   //       playwright 会推动菜单面板将 "蓝湖设计图" 菜单项滚动到 viewport，
  //   //       由于无法滚动（这是我们程序的问题），这会导致测试用例执行失败。
  //   // 因此：
  //   //     测试用例在进行蓝湖设计图 block 的测试时，在第 6 个 block 添加超级表格
  //   for (let i=0; i<4; i++) {
  //     await frame.press('.ce-paragraph >> nth=-1', 'Enter');
  //   }
  //
  //   // 添加蓝湖设计图 block
  //   await createBlock('蓝湖设计图', frame);
  //
  //   const inputSelector = '[placeholder="粘贴蓝湖链接 https://lanhuapp.com/..."]';
  //   // 等待输入框 DOM 渲染完毕
  //   await frame.waitForSelector(inputSelector);
  //   // 在输入框中输入蓝湖设计图地址
  //   await frame.fill(inputSelector, lanhuProjectURL);
  //
  //   const buttomSelector = '.ce-lanhu-stage-confirm-show';
  //   // 等待 "确定" 按钮 DOM 渲染完毕
  //   await frame.waitForSelector(buttomSelector);
  //   // 模拟用户点击 "确定" 按钮
  //   await frame.click(buttomSelector);
  //
  //   // 蓝湖设计图 block 内容部分的 iframe 选择器
  //   const iframeSelector = '.ce-lanhu-stage-iframe-wrapper iframe';
  //   // 蓝湖设计图 block 标题部分的选择器
  //   const titleSelector = '.ce-lanhu-stage-bar-title';
  //   // 等待相关 DOM 渲染完毕
  //   await Promise.all([
  //     // 等待蓝湖设计图的 iframe 渲染完毕
  //     frame.waitForSelector(iframeSelector),
  //     // 等待蓝湖设计图标题的 DOM 渲染完毕
  //     frame.waitForSelector(titleSelector),
  //   ]);
  //   // 断言蓝湖设计图 iframe 样式正确
  //   await Promise.all([
  //     expect(frame.locator(iframeSelector)).toHaveAttribute('width', '133.33%'),
  //     expect(frame.locator(iframeSelector))
  //         .toHaveAttribute('height', '133.33%'),
  //   ]);
  //   // 断言蓝湖设计图标题内容正确
  //   // await expect(frame.locator(titleSelector)).toHaveText(lanhuProjectName);
  // });

  // 最新改动的蓝湖设计图
  test('蓝湖设计图 block', async () => {
    //   三种创建蓝湖block的规则
    //       1-搜索框勾选
    //       2-设计图长链接复制
    //       3-设计图锻连接复制
    for (let i=0; i<4; i++) {
      await frame.press('.ce-paragraph >> nth=-1', 'Enter');
    }

    // 添加蓝湖设计图 block
    await createBlock('蓝湖设计图', frame);

    const lanhuSelector = '.ce-lanhu-stage-wrapper';
    // 等待输入框 DOM 渲染完毕
    await frame.waitForSelector(lanhuSelector);
    // 在输入框中输入蓝湖设计图地址
    await frame.click(lanhuSelector);
    // 点击搜索框上的输入
    const inputSelector = '.lanhu-design-selector-input';
    await frame.click(inputSelector);
    await frame.fill(inputSelector, lanhuProjectName);
    const resultSelector = '.lanhu-design-selector-list-item >>nth=0';
    await frame.click(resultSelector, {delay: 500});

    // 蓝湖设计图 block 内容部分的 iframe 选择器
    const iframeSelector = '.ce-lanhu-stage-iframe-wrapper iframe';

    // 蓝湖设计图 block 标题部分的选择器
    const titleSelector = '.ce-lanhu-stage-bar-title';
    // 等待相关 DOM 渲染完毕
    await Promise.all([
      // 等待蓝湖设计图的 iframe 渲染完毕
      frame.waitForSelector(iframeSelector),
      // 等待蓝湖设计图标题的 DOM 渲染完毕
      frame.waitForSelector(titleSelector),
    ]);
    // 断言蓝湖设计图 iframe 样式正确
    await Promise.all([
      expect(frame.locator(iframeSelector)).toHaveAttribute('width', '133.33%'),
      expect(frame.locator(iframeSelector))
          .toHaveAttribute('height', '133.33%'),
    ]);
    // 断言蓝湖设计图标题内容正确
    await expect(frame.locator(titleSelector)).toHaveText(lanhuProjectName);
  });

  test('分割线 block', async () => {
    // 在最后一个文本 block 中输入分割线内容
    await frame.fill('.ce-paragraph >> nth=-1', '---');
    // 模拟用户按下空格键，从而添加分割线 block
    await frame.press('text=---', ' ');
    // 分割线 block 的选择器
    const selector = '.ce-delimiter';
    // 等待分割线 block 的 DOM 渲染完毕
    await frame.waitForSelector(selector);
    // 断言分割线 block 可见
    await expect(frame.locator(selector)).toBeVisible();
  });

  test('特殊说明 block', async () => {
    // 添加特殊说明 block
    await createBlock('特殊说明', frame);
    // 特殊说明 block 的选择器
    const selector = 'div[data-placeholder="输入内容..."]';
    // 特殊说明 block 第一行的内容
    const contentFirstLine = '特殊说明 block 第一行内容';
    // 特殊说明 block 第二行的内容
    const contentSecondLine = '特殊说明 block 第二行内容';
    // 等待输入框 DOM 渲染完毕
    await frame.waitForSelector(selector);
    // 模拟用户在特殊说明 block 中输入第一行内容
    await frame.type(selector, contentFirstLine, {delay: 100});
    // 模拟用户按下 Shift + Enter 键
    await frame.press(selector, 'Shift+Enter');
    // 模拟用户在特殊说明 block 中输入第二行内容
    await frame.type(selector, contentSecondLine, {delay: 100});
    // 断言特殊说明中的内容正确
    await expect(frame.locator(selector))
        .toHaveText(contentFirstLine + contentSecondLine);
  });

  test('待办事项 block', async () => {
    // 添加待办事项 block
    await createBlock('待办事项', frame);

    // 勾选完成后的 class 名称的匹配模式
    const doneClassNamePattern = /cdx-checklist__item--checked/;

    // 第一个待办事项编辑框选择器
    const firstListItemSelector =
      '.lanhu-list-content[contenteditable="true"] >> nth=0';
    // 第一个待办事项内容
    const firstListItemContent = '第一个待办事项';
    // 等待第一个编辑框 DOM 渲染完毕
    await frame.waitForSelector(firstListItemSelector);
    // 模拟用户在第一个待办事项 block 中输入内容
    await frame.fill(firstListItemSelector, firstListItemContent);
    // 断言第一个待办事项内容正确
    await expect(frame.locator(firstListItemSelector))
        .toHaveText(firstListItemContent);
    // 模拟用户勾选第一个待办事项
    await frame.click('.cdx-checklist__item-checkbox >> nth=0');
    // 断言第一个待办事项勾选状态正确
    await expect(frame.locator('.cdx-checklist >> nth=0'))
        .toHaveClass(doneClassNamePattern);

    // 模拟用户按下回车键创建第二个待办事项
    await frame.press(firstListItemSelector, 'Enter');

    // 第二个待办事项编辑框选择器
    const secondListItemSelector =
      '.lanhu-list-content[contenteditable="true"] >> nth=1';
    // 第二个待办事项内容
    const secondListItemContent = '第二个待办事项';
    // 等待第二个编辑框 DOM 渲染完毕
    await frame.waitForSelector(secondListItemSelector);
    // 模拟用户在第二个待办事项 block 中输入内容
    await frame.fill(secondListItemSelector, secondListItemContent);
    // 断言第二个待办事项内容正确
    await expect(frame.locator(secondListItemSelector))
        .toHaveText(secondListItemContent);
    // 模拟用户勾选第二个待办事项
    await frame.click('.cdx-checklist__item-checkbox >> nth=1');
    // 断言第二个待办事项勾选状态正确
    await expect(frame.locator('.cdx-checklist >> nth=1'))
        .toHaveClass(doneClassNamePattern);
  });

  test('文本 block', async () => {
    // 创建一个新的 block (默认为文本类型)
    await frame.press('.ce-paragraph', 'Enter');

    const text = '这是新建的文本 block。';

    // 在新创建的文本 block 中输入内容
    await frame.fill('.ce-paragraph >> nth=-1', text);
    const locator = frame.locator('.ce-paragraph >> nth=-1');
    // 断言内容正确更新到 DOM
    await expect(locator).toHaveText(text);
    // 断言字体大小为正确的样式
    await expect(locator).toHaveCSS('font-size', '16px');
  });

  test('一级标题 block', async () => {
    await testHeaderBlock(1, frame);
  });

  test('二级标题 block', async () => {
    await testHeaderBlock(2, frame);
  });

  test('三级标题 block', async () => {
    await testHeaderBlock(3, frame);
  });

  test('无序列表 block', async () => {
    await testListBlock({ordered: false}, frame);
  });

  test('有序列表 block', async () => {
    await testListBlock({ordered: true}, frame);
  });
});
