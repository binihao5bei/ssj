# @ts-web/test-e2e

存放 ts-web 工程端到端相关测试用例


官方文档：https://playwright.dev/docs/intro

1-安装node环境，

2-安装依赖
npm i -D @playwright/test
npm i -D experimental-allure-playwright
npx playwright install

3-运行
npx playwright test（运行全部）
带命令的运行：
npx playwright test tests/blocks.spec.js --config ./config/playwright.config.js 
带bug调试
npx playwright test tests/blocks.spec.js --config ./config/playwright.config.js --debug
或者直接在package.json配置script
npm run test

4-自动录制工具
npx playwright codegen https://lanhuapp.com

5-更改测试环境
直接修改config.env.js
selectEnv、userEnv修改为对应的环境

6-获取报告
allure generate ./allure-results -o ./allure-results/exportReport --clean
或者npm run allure

