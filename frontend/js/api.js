// api.js — 后端 API 客户端
// 职责：封装 fetch 请求，统一处理认证头、响应格式和错误

async function apiRequest(method, path, body = null) {
    /** 通用 API 请求方法，自动附加认证头并解析统一响应格式 */
    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
            "X-API-Key": API_KEY || "",
        },
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${path}`, options);
    const data = await response.json();

    if (data.code !== 0) {
        throw new Error(data.message || "请求失败");
    }

    return data;
}

function apiGet(path) {
    /** GET 请求快捷方法 */
    return apiRequest("GET", path);
}

function apiPost(path, data) {
    /** POST 请求快捷方法 */
    return apiRequest("POST", path, data);
}

function apiDelete(path) {
    /** DELETE 请求快捷方法 */
    return apiRequest("DELETE", path);
}
