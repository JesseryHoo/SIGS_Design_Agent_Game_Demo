// config.js — 前端全局配置
// 职责：定义 API 地址、页面路径常量、情绪标签配置

const API_BASE_URL = "http://localhost:8989/api/v1";

const PAGES = {
    LANDING: "landing.html",      // 阶段一：进入与吸引
    EXPLORE: "explore.html",      // 阶段二：场景漫游选点
    CREATE: "create.html",        // 阶段三：创意输入
    CONFIRM: "confirm.html",      // 阶段四：确认设计说明
    GENERATE: "generate.html",    // 阶段五：生成与呈现
    GALLERY: "gallery.html",      // 阶段六：社区沉淀
};

const EMOTION_TAGS = [
    { emoji: "\u{1F624}", label: "不够用" },
    { emoji: "\u{1F60C}", label: "太单调" },
    { emoji: "\u{1F33F}", label: "想要绿色" },
    { emoji: "☀️", label: "采光不好" },
    { emoji: "\u{1F9CD}", label: "太拥挤" },
    { emoji: "\u{1F507}", label: "太吵了" },
];
