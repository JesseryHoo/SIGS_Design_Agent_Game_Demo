# design_service.py — 设计流程业务逻辑
# 职责：处理创意输入提交、设计确认、状态查询、列表获取、地图数据等核心设计流程

from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.design import DesignConfirmRequest, DesignInputRequest, DesignListParams


async def submit_input(db: AsyncSession, request: DesignInputRequest) -> dict:
    """保存用户创意输入并触发 Agent 处理

    TODO: 1. 通过 session_id 查找或创建用户
          2. 创建设计记录（位置 + 情绪标签 + 用户输入）
          3. 调用 agent_service.translate_to_design_spec()
          4. 更新设计记录中的 AI 回应
          5. 返回包含 ai_response 的设计数据
    """
    raise NotImplementedError("TODO: 实现设计输入提交逻辑")


async def confirm_design(db: AsyncSession, request: DesignConfirmRequest) -> dict:
    """确认设计说明并触发图生图生成

    TODO: 1. 通过 session_id 查找用户
          2. 更新设计记录为已确认的设计说明
          3. 异步触发 image_service.generate_image()
          4. 返回处理状态
    """
    raise NotImplementedError("TODO: 实现设计确认逻辑")


async def get_design(db: AsyncSession, design_id: str) -> dict | None:
    """根据 id 获取设计完整详情

    TODO: 查询 designs 表，返回完整设计记录
    """
    raise NotImplementedError("TODO: 实现获取设计详情")


async def get_design_status(db: AsyncSession, design_id: str) -> dict:
    """查询异步生成状态（图生图、3D模型）

    TODO: 查询设计记录，返回状态（processing/completed/failed）
          以及可用的 generated_image 和 model_3d_url
    """
    raise NotImplementedError("TODO: 实现设计状态查询")


async def list_designs(db: AsyncSession, params: DesignListParams) -> dict:
    """获取设计列表，支持分页和排序

    TODO: 查询 designs 表，支持按 created_at 或 likes_count 排序，返回分页结果
    """
    raise NotImplementedError("TODO: 实现设计列表查询")


async def get_map_points(db: AsyncSession) -> list[dict]:
    """获取所有设计的地图光点数据（用于社区 Gallery 页面的校园地图可视化）

    TODO: 查询 designs 表，仅返回 id、location_x/y/z、location_label、likes_count
    """
    raise NotImplementedError("TODO: 实现地图光点数据查询")
