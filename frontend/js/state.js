// state.js — 客户端状态管理
// 职责：基于 sessionStorage 的简单状态存取，用于页面间传递 sessionId、designId 等数据

function setState(key, value) {
    /** 存储状态到 sessionStorage */
    sessionStorage.setItem(key, JSON.stringify(value));
}

function getState(key) {
    /** 从 sessionStorage 读取状态 */
    const raw = sessionStorage.getItem(key);
    if (raw === null) return null;
    try {
        return JSON.parse(raw);
    } catch {
        return raw;
    }
}

function clearState(key) {
    /** 清除指定状态，不传参则清除全部 */
    if (key) {
        sessionStorage.removeItem(key);
    } else {
        sessionStorage.clear();
    }
}
