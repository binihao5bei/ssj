/**
 * 封装 page 相关逻辑
 *
 * 包括：
 *      1）登录
 *      2）创建 TS Document page
 *      3）删除 TS Document page
 *      4）创建 Block
 *      5）删除 Block
 *      6）......
 */

const {expect} = require('@playwright/test');
const {selectEnv, userEnv} = require('../config/env');

// 账号环境

const users = {
  UserA: require(`./users/${userEnv}/userA`),
  UserB: require(`./users/${userEnv}/userB`),
  UserC: require(`./users/${userEnv}/userC`),
  UserD: require(`./users/${userEnv}/userD`),
  UserE: require(`./users/${userEnv}/userE`),
  UserF: require(`./users/${userEnv}/userF`),
  UserG: require(`./users/${userEnv}/userG`),
  UserH: require(`./users/${userEnv}/userH`),
  UserI: require(`./users/${userEnv}/userI`),
  UserJ: require(`./users/${userEnv}/userJ`),
  UserK: require(`./users/${userEnv}/userK`),
};

/**
 * 使用 user 登录函数的集合
 *
 * @param {Context} context - 浏览器 context 实例
 *
 * @returns {Promise<Page>} page 已经登录 user 的 page 对象
 */
const loginWithUserFunctionList = {};

Object.keys(users).forEach((userName) => {
  const funcName = `loginWith${ userName }`;
  const user = users[userName];
  const func = (context) => login(context, user.email, user.pwd, user.tsUrl);

  loginWithUserFunctionList[funcName] = func;
});


// 登录页面的 url (开发环境)
const loginUrl = selectEnv.loginURL;

/**
 * 获取今天的日期
 *
 * @return {String} 今天的日期 例如： '2021-01-01'
 */
const today = () => {
  const dt = new Date();

  return dt.toJSON().split('T')[0];
};

/**
 * 获取当前的时间
 *
 * @return {String} 现在的时间 例如： '2021-01-01'
 */
const nowTime = () => {
  const d = new Date();
  let nowTime = '';
  nowTime += d.getHours() + '时';
  nowTime += d.getMinutes() + '分';
  nowTime += d.getSeconds() + '秒';
  return nowTime;
};


/**
 * 创建测试页面的标题
 *
 * @param {String} topic - 测试主题
 *
 * @return {String} title 测试页面的标题
 */
const createTitle = (topic) => `[e2e ${today()}] ${topic}`;

/**
 * 接收一个 context 实例，一个账户信息，创建并返回一个已登录的 page 对象
 *
 * @param {Context} context - Context 实例
 * @param {String} email - 账户的登录邮箱
 * @param {String} pwd - 账户的登录密码
 * @param {String} tsUrl - 账户的页面地址
 *
 * @return {Promise<Page>} 已登录的 page 对象
 */
const login = async (context, email, pwd, tsUrl) => {
  const page = await context.newPage();

  // 第一步：进入登录页面
  // 这里需要注意，playwright 的每一个测试用例默认都是资源隔离的，不共享任何状态
  // 因此，对于多个测试用例都需要的登录态等资源，需要单独做处理。
  await page.goto(loginUrl);

  // 填写账号
  await page.fill('input[name="email"]', email);

  // 填写密码
  await page.fill('input[name="password"]', pwd);

  // 点击登录按钮
  await page.click('button.login_btn');


  // 等待页面跳转到有『超级文档』的页面
  await page.waitForSelector('text=超级文档');
  await expect(page.locator('.tabs .tabs-link >> nth=0')).toHaveText('超级文档');
  // await page.click('text=超级文档');

  await page.goto(tsUrl);

  return page;
};

/**
 * 根据 page 对象获取 TS 的 iframe 对象
 *
 * @param {Page} page - page 对象
 *
 * @return {Promise<Frame>} frame 对象
 */
const getTsFrame = (page) => page.frame('micro-app-ts-iframe');

/**
 * 模拟用户点击导航树上方的按钮新建页面的函数
 *
 * @param {String} title - TS Document page 的标题
 * @param {Page} page - page 对象
 * @param {String} [defaultContent='默认文本 block。'] 默认的文本 block 内容
 *
 * @return {Promise<Frame>} frame 对象
 */
const createDocument = async (title, page, defaultContent = '默认文本 block。') => {
  // 由于主站的页面在一个 iframe 中嵌套了 ts 页面，因此需要先定位到 ts 的 iframe
  const frame = await getTsFrame(page);
  // 等待 ts 页面中的 "创建文档" 渲染完毕
  await frame.waitForSelector('button.create-btn');
  await expect(frame.locator('button.create-btn')).toHaveText('新建文档');

  // 模拟用户点击 "创建文档" 按钮，创建一个新页面
  await frame.click('button.create-btn', {delay: 1500});

  // 等待模板弹层中的 "使用空白模板" 按钮渲染完毕
  await frame.waitForSelector('.ts-template-wrapper .create-default-doc-btn');

  // 模拟用户点击模板弹层中的 "使用空白模板" 按钮
  await frame.click('.ts-template-wrapper .create-default-doc-btn', {delay: 500});

  // 模拟用户在新页面输入标题
  await frame.waitForSelector('#title');
  await frame.fill('#title', title);

  // 模拟用户在默认文本 block 输入文字内容
  await frame.fill('.ce-paragraph >> nth=0', defaultContent);

  return frame;
};

/**
 * 模拟用户点击右上角 "..." 菜单中的 "删除" 选项，从导航树中删除当前页面
 *
 * @param {Frame} frame - frame 对象
 *
 * @return {Void}
 */
const removeDocument = async (frame) => {
  await frame.click('.bar_menu');
  const deleteItemClass = '.bar_delete';
  await frame.waitForSelector(deleteItemClass);
  await frame.click(deleteItemClass);
  const confirmButtomClass = 'button :text("删除")';
  await frame.waitForSelector(confirmButtomClass);
  await frame.click(confirmButtomClass);
};

/**
 * 模拟用户点击 block 左侧 "+", 创建指定类型 block
 *
 * @param {String} title - 菜单选项名称
 * @param {Frame} frame - frame 对象
 * @param {String} selector - 选择器
 *
 * @return {Void}
 */
const createBlock = async (
    title,
    frame,
    selector = '.ce-paragraph >> nth=-1',
) => {
  await frame.hover(selector);
  await frame.waitForSelector('.ce-toolbar__plus');
  await frame.click('.ce-toolbar__plus');
  await frame.waitForSelector('.ce-toolbox');
  await frame.click(`text=${title}`);
};

/**
 * 模拟用户点击 "六个点" 并点击 "删除"，来删除指定的 block
 *
 * @param {String} blockSelector - block 选择器
 * @param {Frame} frame - frame 对象
 *
 * @return {Void}
 */
const removeBlock = async (blockSelector, frame) => {
  // 目前有三个 block 支持等宽功能：普通表格、图片、蓝湖设计图
  // 由于它们的关闭方式与其它 block 不同，因此需要单独处理
  const newBlockClassList = [
    'ts-block-table',
    'ts-block-image',
    'ts-block-ddt',
  ];
  const blockLocator = await frame.locator(blockSelector);
  const classListString = await blockLocator.getAttribute('class');
  const classList = classListString.split(' ');
  const intersectClassList = newBlockClassList
      .filter((item) => classList.includes(item));

  // 模拟用户鼠标 hover 当前 block，触发菜单按钮展示
  await frame.hover(blockSelector, {position: {x: 0, y: 1}});

  // 根据当前 block 的 class 名称来决定使用哪个菜单按钮
  const buttomSelector = intersectClassList.length ?
    '.ce-toolbar__style' : '.ce-toolbar__actions--opened';

  // 等待按钮 DOM 渲染完毕
  await frame.waitForSelector(buttomSelector);
  // 模拟用户点击按钮
  await frame.click(buttomSelector);
  // 等到菜单面板 DOM 渲染完毕
  await frame.waitForSelector('.menu .delete');
  // 模拟用户点击 "删除" 菜单
  await frame.click('.menu .delete');
};

/**
 * 删除除第一个 block 外，其他所有的block
 *
 * @param {Frame} frame - frame 对象
 *
 * @return {Void}
 */
const removeBlocks = async (frame) => {
  const blocks = await frame.$$('.ce-block');

  if (!blocks.length || blocks.length === 1) return;

  // 清理新建的 block
  for (let i=blocks.length - 1; i>0; i--) {
    await removeBlock(`.ce-block >> nth=${i}`, frame);
  }
};

/**
 * 键盘操作模拟用户选中行内文本
 *
 * @param {Frame} frame - frame 对象，title 文本内容
 * @param {String} text - 文本内容
 *
 * @return {Void}
 */
const selectInlineText = async (frame, text) => {
  await frame.click(`text=${text}`);

  // 使用键盘，向左依次选中文本内容
  for (let i=0; i< text.length; i++) {
    await frame.press(`text=${text}`, 'Shift+ArrowLeft');
  };
};


/**
 * 鼠标操作，右键点击文档，模拟用户创建子文档，同级文档
 *
 * @param {Frame} frame - frame 对象
 * @param {String} target - DocumentUrl要创建文档的url
 * @param {Number} flag - 1子页面，2下方添加页面，3上方添加页面
 * @param {String} title - 创建的文档标题
 *
 * @return {Void}
 */
const createSubDocument = async (frame, target, flag, title) => {
  const map = {
    1: {text: '添加子页面'},
    2: {text: '下方添加页面'},
    3: {text: '上方添加页面'},
  };
  const text = map[flag].text;

  // 目标文档右键展示快捷面板
  // await frame.click(target, { button: 'right' });
  // 选中当前文档
  await frame.click(target, {delay: 1000});
  // 选中当前文档的右边操作按钮
  const selectLocator = '.curSelectedNode';
  await frame.hover(selectLocator);
  await frame.click('.curSelectedNode .plus-icon');


  // 点击对应的文案
  await frame.click(`text=${text}`, {delay: 500});

  // 等待模板弹层中的 "使用空白模板" 按钮渲染完毕
  await frame.waitForSelector('.ts-template-wrapper .btn-use-default');

  // 模拟用户点击模板弹层中的 "使用空白模板" 按钮
  await frame.click('.ts-template-wrapper .btn-use-default', {delay: 500});

  // 模拟用户在新页面输入标题
  await frame.waitForSelector('#title');
  await frame.fill('#title', title);

  // 模拟用户在默认文本 block 输入文字内容
  await frame.fill('.ce-paragraph >> nth=0', '创建的默认文本');
};


/**
 * 模拟用户目录树右键点击文档，菜单上删除文档
 *
 * @param {Frame} frame - frame 对象
 * @param {String} target - 被删除目标文档
 *
 * @return {Void}
 */
const removeTreeDocument = async (frame, target) => {
  // 目标文档右键展示快捷面板
  // await frame.click(target, { button: 'right' });
  //  选中当前文档
  await frame.click(target, {delay: 500});
  // 选中当前文档的右边操作按钮
  const selectLocator = '.curSelectedNode';
  await frame.hover(selectLocator);
  await frame.click('.curSelectedNode .plus-icon');

  // 点击对应的文案
  await frame.click('text=删除', {delay: 300});

  const confirmButtomClass = 'button:has-text("是")';
  await frame.waitForSelector(confirmButtomClass);
  await frame.click(confirmButtomClass);
};


/**
 * 根据url返回对应的文档选择器
 *
 * @param {Frame} frame - frame 对象
 *
 * @return {string}documentSelector 当前文档的选择器
 */
const returnDocumentSelector = async (frame) => {
  // 返回当前frame的url
  const url = frame.url();
  const urls = url.split('/');

  const documentId = urls[urls.length-1];

  const documentSelector = `[data-id="${documentId}"]`;
  return documentSelector;
};

/**
 * 搜索对应的文档
 *
 * @param {Frame} frame - frame 对象
 * @param {String} searchValue - 搜索的名称
 *
 */
const searchDocument = async (frame, searchValue) => {
  const searchSelector = '.tree-node-search';
  // 点击搜索图标
  await frame.click(searchSelector, {delay: 500});
  const searchInput = '[placeholder="搜索..."]';
  await frame.waitForSelector(searchInput);
  // 点击输入框
  await frame.click(searchInput);
  // 输入搜索内容
  await frame.fill(searchInput, searchValue);
  // 按enter键
  await frame.press(searchInput, 'Enter');
};

/**
 * 模拟用户分享该文档
 *
 * @param {Frame} frame - frame 对象
 *
 * @return {Void}
 */
const shareDocument = async (frame) => {
  const shareItemClass = '.primary_btn > .shareIcon';
  // 等待文档右上角的分享按钮渲染完毕
  await frame.waitForSelector(shareItemClass);
  // 点击分享按钮
  await frame.click(shareItemClass);
  const urlSelector = '.page-share-select > input[type="text"]';
  // 等待分享url渲染完毕
  await frame.waitForSelector(urlSelector);
  // 匹配分享链接是否正确
  await expect(frame.locator(urlSelector))
      .toHaveValue(/https:\/\/lanhuapp.com\/url.*/g);
  // 点击复制链接按钮
  await frame.click('.page-share-btn', {delay: 200});
  // 断言复制成功
  await expect(frame.locator('.page-share-btn'))
      .toHaveClass('el-button el-button--primary page-share-btn share-copy-done');
  // 关闭分享的弹窗
  await frame.click('.el-overlay', {delay: 200});
};

/**
 * 获取控制台的信息
 *
 * @param {Page} page - page 对象
 * @param {String} getType - 控制台信息类型'log', 'debug', 'info', 'error', 'warning'等
 *
 * @return {string}msgs 获得的错误信息
 */
const consoleMsg = async (page, getType) => {
  let msgs = '';
  // Listen for all console events and handle errors
  page.on('console', (msg) => {
    if (msg.type() === getType) {
      return msgs = `${getType} text: "${msg.text()}"`;
    }
  });
};


module.exports = {
  getTsFrame,
  createTitle,
  login,
  ...loginWithUserFunctionList,
  createDocument,
  removeDocument,
  createBlock,
  removeBlock,
  removeBlocks,
  selectInlineText,
  createSubDocument,
  removeTreeDocument,
  returnDocumentSelector,
  nowTime,
  searchDocument,
  consoleMsg,
  shareDocument,
};
