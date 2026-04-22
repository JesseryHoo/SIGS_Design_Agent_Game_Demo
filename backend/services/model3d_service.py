# model3d_service.py — 图转3D模型服务
# 职责：调用图转3D API，将生成的场景图转换为可导入 UE 的3D模型


async def convert_to_3d(generated_image_url: str) -> dict:
    """调用图转3D API，从生成的场景图中生成3D模型

    TODO: 1. 将生成的图片发送给3D转换 API（Hunyuan3D / Tripo3D 等）
          2. 识别并提取新增/修改的结构
          3. 生成3D模型文件（FBX/glTF 格式）
          4. 返回 {"model_3d_url": str, "status": "processing"|"completed"}

    参数:
        generated_image_url: AI 生成的场景图 URL

    返回:
        包含 model_3d_url 和 status 的字典
    """
    raise NotImplementedError("TODO: 实现图转3D转换逻辑")
