#模型管理 CRUD
#app/crud/llm_model.py
from sqlalchemy.orm import Session
from app.models.llm_model import LLMModel
from app.schemas.llm_model import LLMModelCreate, LLMModelUpdate
import uuid

def create_llm_model(db: Session, model: LLMModelCreate) -> LLMModel:
    """创建模型配置"""
    db_model = LLMModel(
        id=str(uuid.uuid4()),
        name=model.name,
        description=model.description,
        type=model.type,
        model_key=model.model_key,  # 生产环境需加密存储
        base_url=str(model.base_url),
        real_model_name=model.real_model_name,
        is_active=model.is_active,
        extra_config=str(model.extra_config) if model.extra_config else None
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_llm_model(db: Session, model_id: str) -> LLMModel:
    """通过ID获取模型配置"""
    #return db.query(LLMModel).filter(LLMModel.id == model_id, LLMModel.is_active == True).first()
    return db.query(LLMModel).filter(LLMModel.id == model_id).first()

def get_llm_model_by_name(db: Session, name: str) -> LLMModel:
    """通过名称获取模型配置"""
    #return db.query(LLMModel).filter(LLMModel.name == name, LLMModel.is_active == True).first()
    return db.query(LLMModel).filter(LLMModel.name == name).first()

def get_all_llm_models(db: Session, skip: int = 0, limit: int = 100) -> list[LLMModel]:
    """获取所有的模型配置"""
    #return db.query(LLMModel).filter(LLMModel.is_active == True).offset(skip).limit(limit).all()
    return db.query(LLMModel).offset(skip).limit(limit).all()

def update_llm_model(db: Session, model_id: str, model_update: LLMModelUpdate) -> LLMModel:
    """更新模型配置"""
    db_model = get_llm_model(db, model_id)
    if not db_model:
        return None
    # 只更新传入的字段
    update_data = model_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "base_url":
            value = str(value)  # 处理HttpUrl类型
        setattr(db_model, key, value)
    db.commit()
    db.refresh(db_model)
    return db_model

def delete_llm_model(db: Session, model_id: str) -> bool:
    """删除模型"""
    db_model = get_llm_model(db, model_id)
    if not db_model:
        return False
    # 直接从数据库中删除（硬删除），不要软删除
    db.delete(db_model)
    db.commit()
    return True