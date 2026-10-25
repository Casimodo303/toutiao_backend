#===============================================================
# 名称：utils/security.py
# 作用：安全模块，实现对隐私数据的加密操作
# 主要依赖：
#===============================================================
# 三方库
from passlib.context import CryptContext

# 创建密码上下文
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# 密码加密
def get_hash_password(password: str):
    return pwd_context.hash(password)

# 密码验证 (返回值：True或False)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)





