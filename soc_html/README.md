# YunSong_web_app

> YunSong (SOC)'s web app project

# 基础环境部署

## 安装nodejs环境

```
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
```

```
sudo aptitude install -y nodejs
```

## 安装依赖

```
npm install
```
# 开发环境部署

## 启动服务并支持热加载, 访问 http://localhost:10080

```
npm run dev
```

# 生产环境部署

## 构建生产环境文件, 文件生成在dist目录下

```
npm run build
```

# 运行测试用例

## 运行测试用例

```
npm test
```

For detailed explanation on how things work, consult the [docs for vue-loader](http://vuejs.github.io/vue-loader).
