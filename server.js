// 创建一个简单的服务器来提供静态文件
const express = require('express');
const path = require('path');
const app = express();
const PORT = 80;

// 提供静态文件
app.use(express.static(path.join(__dirname)));

// 启动服务器
app.listen(PORT, '0.0.0.0', () => {
  console.log(`圣经阅读应用服务器运行在 http://localhost:${PORT}`);
});
