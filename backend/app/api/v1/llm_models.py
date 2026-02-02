#模型管理接口
#app/api/v1/llm_models.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.llm_model import LLMModelCreate, LLMModelUpdate, LLMModelResponse
from app.crud.llm_model import (
    create_llm_model, 
    get_llm_model, 
    get_llm_model_by_name, 
    get_all_llm_models, 
    update_llm_model, 
    delete_llm_model
)
from app.db.session import get_db
from app.core.security import get_current_admin, get_current_user

router = APIRouter(prefix="/llm-models", tags=["模型管理"])

# 以下接口逻辑不变，仅确保导入有效
@router.post("/", response_model=LLMModelResponse)
async def create_model(
    model: LLMModelCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_admin)
):
    existing_model = get_llm_model_by_name(db, model.name)
    if existing_model:
        raise HTTPException(status_code=400, detail="模型名称已存在")
    return create_llm_model(db, model)

@router.get("/{model_id}", response_model=LLMModelResponse)
async def get_model(
    model_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_admin)
):
    model = get_llm_model(db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在或已禁用")
    return model

@router.get("/", response_model=list[LLMModelResponse])
async def get_all_models(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user) #这样普通用户也能选择模型
    #current_user: str = Depends(get_current_admin) 
):
    return get_all_llm_models(db, skip, limit)

@router.put("/{model_id}", response_model=LLMModelResponse)
async def update_model(
    model_id: str,
    model_update: LLMModelUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_admin)
):
    model = update_llm_model(db, model_id, model_update)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在或已禁用")
    return model

@router.delete("/{model_id}")
async def delete_model(
    model_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_admin)
):
    success = delete_llm_model(db, model_id)
    if not success:
        raise HTTPException(status_code=404, detail="模型不存在或已禁用")
    return {"success": True, "message": "模型已禁用"}