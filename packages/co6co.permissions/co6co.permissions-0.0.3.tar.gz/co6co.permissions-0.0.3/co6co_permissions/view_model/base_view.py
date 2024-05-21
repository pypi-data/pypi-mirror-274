from co6co_web_db.view_model import BaseMethodView,Request
from .aop.api_auth import authorized,ctx,getCtxUserId
 
class CtxMethodView(BaseMethodView): 
   decorators=[ctx]  

class AuthMethodView(BaseMethodView): 
   decorators=[authorized] 
   
   def getUserId(self, request: Request):
      """
      获取用户ID
      """  
      return getCtxUserId(request)
   
   def getUserName(self, request: Request): 
       """
       获取当前用户名
       """
       current_user=request.ctx.current_user  
       return current_user.get("userName") 

