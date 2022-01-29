
const dev = {
  baseURL: 'https://dev.lanhuapp.com',
  loginURL: 'https://dev.lanhuapp.com/web/feature/micro-app-ts-ui3/#/user/login',
};

const test = {
  baseURL: 'https://dev.lanhuapp.com',
  loginURL: 'https://dev.lanhuapp.com/web/feature/micro-app-ts-ui3-test/#/user/login',
};

const pre = {
  baseURL: 'https://pre.lanhuapp.com',
  loginURL: 'https://pre.lanhuapp.com/web/#/user/login',
};

const prod = {
  baseURL: 'https://lanhuapp.com',
  loginURL: 'https://lanhuapp.com/web/#/user/login',
};

const selectEnv = prod;
const userEnv = 'prod';


module.exports = {
  dev,
  test,
  prod,
  pre,
  selectEnv,
  userEnv,
};


