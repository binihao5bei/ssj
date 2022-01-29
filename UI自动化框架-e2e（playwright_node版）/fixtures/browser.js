const {chromium, firefox, webkit} = require('@playwright/test');

/**
 * 创建 Browser 实例: chromium
 *
 * @param {config} config - browser 实例的配置对象
 *
 * @return {Promise<Browser>} Browser 实例
 */
const createChromiumBrowser = (config = {}) => chromium.launch(config);

/**
 * 创建 Browser 实例: firefox
 *
 * @param {config} config - browser 实例的配置对象
 *
 * @return {Promise<Browser>} Browser 实例
 */
const createFirefoxBrowser = (config = {}) => firefox.launch(config);

/**
 * 创建 Browser 实例: webkit
 *
 * @param {config} config - browser 实例的配置对象
 *
 * @return {Promise<Browser>} Browser 实例
 */
const createWebkitBrowser = (config = {}) => webkit.launch(config);

module.exports = {
  createChromiumBrowser,
  createFirefoxBrowser,
  createWebkitBrowser,
};
