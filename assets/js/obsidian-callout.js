document.addEventListener("DOMContentLoaded", function() {
  // 定义Obsidian callout类型与Chirpy prompt样式的映射关系
  const calloutMap = {
    "note": "info",
    "info": "info",
    "todo": "info",
    "tip": "tip",
    "success": "success",
    "question": "question",
    "warning": "warning",
    "caution": "warning",
    "failure": "danger",
    "danger": "danger",
    "error": "danger",
    "bug": "danger",
    "example": "info",
    "quote": "info"
  };

  // 选取所有的 blockquote 元素
  const blockquotes = document.querySelectorAll("blockquote");

  blockquotes.forEach(quote => {
    // 获取第一个p元素，Obsidian callout的标题就在这里
    const firstP = quote.querySelector("p:first-child");
    if (!firstP) return;

    // 用正则表达式匹配 `[!TYPE]` 格式
    const match = firstP.innerHTML.match(/^\[!(\w+)\]/);
    
    if (match) {
      const calloutType = match[1].toLowerCase(); // 提取类型，转为小写
      const promptClass = calloutMap[calloutType] || "info"; // 查找映射，找不到默认为 info

      // 为 blockquote 添加 Chirpy 的 prompt class
      quote.classList.add("prompt-" + promptClass);
      
      //移除 `[!TYPE]` 部分，保留后面的文本作为标题
      let titleText = firstP.innerHTML.substring(match[0].length).trim();
      if (titleText) {
          firstP.innerHTML = titleText;
          // firstP.classList.add("prompt-title"); // 给标题加上样式
      } else {
          firstP.remove(); // 如果没有额外标题，就移除这行
      }
    }
  });
});