

from sanic.request import Request 
from ...model.pos.right import UserPO

def getCtxUserId(request:Request):
   if "current_user" in request.ctx.__dict__.keys():
      return request.ctx.current_user["id"]  
   return None

def getCtxData(user:UserPO):
   """
   通过user获取 dict 保存在 request.ctx.current_user 中 
   """
   return user.to_jwt_dict()