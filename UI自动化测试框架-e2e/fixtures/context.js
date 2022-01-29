/**
 * 封装 context 相关逻辑
 */

const {devices} = require('@playwright/test');

/**
 * 根据指定设备名称，批量创建并返回浏览器 Context 实例
 *
 * @param {Object} browser - 浏览器实例
 * @param {String} deviceName - 设备名称
 * @param {Number} [sum = 1] - 批量创建的实例个数，默认值为 1
 *
 * @return {Promise<Context>[]} 返回指定设备的 Context 实例的数组
 */
const createContexts = (browser, deviceName, sum = 1) => {
  const tasks = [];
  const permissions = ['clipboard-read', 'clipboard-write'];

  for (let i=0; i<sum; i++) {
    tasks.push(browser.newContext({permissions, ...devices[deviceName]}));
  }

  return Promise.all(tasks);
};

/**
 * 批量创建桌面 Chrome 浏览器环境
 *
 * @param {Object} browser - 浏览器实例
 * @param {Number} [sum = 1] - 批量创建的实例个数，默认值为 1
 *
 * @return {Promise<Context>[]} 返回桌面 Chrome 浏览器设备实例的数组
 */
const createDesktopChromeContexts = (browser, sum = 1) => {
  return createContexts(browser, 'Desktop Chrome', sum);
};

/**
 * 批量创建桌面 Safari 浏览器环境
 *
 * @param {Object} browser - 浏览器实例
 * @param {Number} [sum = 1] - 批量创建的实例个数，默认值为 1
 *
 * @return {Promise<Context>[]} 返回桌面 Safari 浏览器设备实例的数组
 */
const createDesktopSafariContexts = (browser, sum = 1) => {
  return createContexts(browser, 'Desktop Safari', sum);
};

module.exports = {
  createDesktopChromeContexts,
  createDesktopSafariContexts,
};
