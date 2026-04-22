# agent_service.py — AI 交互 Agent 服务
# 职责：调用大语言模型 API，将用户的非专业描述翻译为结构化设计说明


async def translate_to_design_spec(
    emotion_tags: list[str] | None,
    user_input: str,
    location_label: str | None,
) -> dict:
    """调用 LLM API，将非专业描述翻译为专业设计语言

    TODO: 1. 根据 emotion_tags、user_input、location_label 构建 Prompt
          2. 调用 LLM API（Claude / GPT 等）
          3. 解析响应为结构化的设计说明
          4. 返回 {"design_description": str, "ai_response": str}

    参数:
        emotion_tags: 用户选择的情绪标签列表
        user_input: 用户自由文字描述
        location_label: 选中的位置名称

    返回:
        包含 design_description 和 ai_response 的字典
    """
    raise NotImplementedError("TODO: 实现 Agent 与 LLM API 的交互")
