const config = {
  // 指定测试用例路径
  testDir: '../tests',

  // timeout 字段定义了每一个测试用例的超时时间
  // 由于端到端测试耗时较长，超时先设置一个值，后面再根据实际情况调优
  timeout: 2 * 60 * 1000,

  // 所有失败的测试用例，自动重试 3 次
  retries: 0,
  // 指定 reporter 类型,增加allure报告
  reporter: [['line'], ['experimental-allure-playwright']],


  use: {
    // 指定在运行测试用例时是否使用 headless 模式
    headless: false,

    // 为方便管理，浏览器资源与测试用例分开部署，因此测试用例不必负责准备浏览器资源
    // channel 字段定义所有的测试用例优先使用的浏览器频道
    channel: 'chrome',

    // 为每个测试用例开启追踪，追踪文件会打包放在 test-results 文件夹下
    trace: 'on',
    screenshot: 'on',
    video: 'retain-on-failure',
  },
};

module.exports = config;
