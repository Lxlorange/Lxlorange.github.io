module.exports = {
  entry: async (params) => {
    const quickAddApi = params.quickAddApi;
    const app = params.app;
    const notice = (msg, duration = 5000) => new Notice(msg, duration);

    const slugify = (text) => {
      if (!text) return "";
      return text.toString().toLowerCase().trim()
        .replace(/[\s_]+/g, '-').replace(/[^\w\u4e00-\u9fa5\-]+/g, '')
        .replace(/\-\-+/g, '-').replace(/^-+/, '').replace(/-+$/, '');
    };

    const postTitle = await quickAddApi.inputPrompt("请输入文章标题 (Enter Post Title)");
    if (!postTitle) {
      notice("❌ 操作已取消。");
      return;
    }

    const slug = slugify(postTitle);
    const folderPath = `assets/img/${slug}`;
    const date = new Date().toISOString().slice(0, 10);
    const dateTime = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const filePath = `_posts/${date}-${slug}.md`;

    const fileContent = `---
title: ${postTitle}
author: 凉香栾
date: ${dateTime} +0800
categories:
tags:
description: 
toc: true
pin: false
math: true
mermaid: true
comment: true
media_subpath: "${slug}"
image:
  path: cover.jpg
  lqip:
  alt: "${postTitle}"
---

`;

    // 3. 创建文件夹
    try {
      await app.vault.createFolder(folderPath);
    } catch (e) {
      if (!e.message.includes("already exists")) {
        notice(`❌ 创建文件夹失败: ${e.message}`);
        return;
      }
    }

    // 4. 创建文章文件
    if (await app.vault.adapter.exists(filePath)) {
      notice(`文件已存在: ${filePath}`);
      return;
    }
    const newFile = await app.vault.create(filePath, fileContent);
    notice(`文章已创建: ${newFile.basename}`);

    // 5. 在新的标签页中打开创建的文件
    app.workspace.openLinkText(newFile.path, '', true);
  },
  settings: {
    name: "新建文章并创建专属资源文件夹",
    author: "Lxl",
    options: {}
  }
};