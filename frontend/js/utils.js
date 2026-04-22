// utils.js — DOM 和格式化工具函数
// 职责：提供选择器快捷方式、日期格式化、防抖、加载状态管理等通用工具

function $(selector) {
    /** querySelector 快捷方式 */
    return document.querySelector(selector);
}

function $$(selector) {
    /** querySelectorAll 快捷方式 */
    return document.querySelectorAll(selector);
}

function formatDate(dateStr) {
    /** 格式化日期为中文格式 */
    const date = new Date(dateStr);
    return date.toLocaleDateString("zh-CN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function debounce(fn, delay = 300) {
    /** 防抖函数 */
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}

function showLoading(container) {
    /** 在指定容器内显示加载遮罩 */
    const overlay = document.createElement("div");
    overlay.className = "loading-overlay";
    overlay.innerHTML = '<div class="loading-spinner"></div>';
    container.style.position = "relative";
    container.appendChild(overlay);
}

function hideLoading(container) {
    /** 移除指定容器内的加载遮罩 */
    const overlay = container.querySelector(".loading-overlay");
    if (overlay) overlay.remove();
}
