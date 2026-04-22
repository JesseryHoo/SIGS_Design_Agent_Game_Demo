# image_service.py — 图生图生成服务
# 职责：调用图生图 API，基于场景截图和设计说明生成新场景图


async def generate_image(original_screenshot_url: str | None, design_description: str) -> dict:
    """调用图生图 API，基于截图和设计说明生成新的场景图

    TODO: 1. 准备输入：原始截图作为参考图 + 设计说明作为 Prompt
          2. 调用图生图 API（Stable Diffusion / Midjourney 等）
          3. 保存生成的图片并返回 URL
          4. 返回 {"generated_image_url": str}

    参数:
        original_screenshot_url: 原始视角截图 URL
        design_description: 已确认的设计改进说明

    返回:
        包含 generated_image_url 的字典
    """
    raise NotImplementedError("TODO: 实现图生图生成逻辑")


async def check_generation_status(task_id: str) -> dict:
    """查询异步图生图任务的状态

    TODO: 查询外部 API 或内部任务队列的生成状态
          返回 {"status": "processing"|"completed"|"failed", "generated_image_url": str|None}
    """
    raise NotImplementedError("TODO: 实现生成状态查询")
