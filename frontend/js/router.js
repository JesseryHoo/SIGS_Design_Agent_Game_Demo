// router.js — 页面导航管理
// 职责：提供页面跳转功能，自动计算 pages 目录的基础路径

function navigateTo(pageName) {
    /** 跳转到指定页面 */
    const baseUrl = getPagesBasePath();
    window.location.href = `${baseUrl}${pageName}`;
}

function getPagesBasePath() {
    /** 获取 pages 目录的基础路径 */
    const currentPath = window.location.pathname;
    if (currentPath.includes("/pages/")) {
        return currentPath.substring(0, currentPath.indexOf("/pages/") + "/pages/".length);
    }
    return "/pages/";
}
