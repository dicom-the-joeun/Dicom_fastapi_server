from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_pw(pw : str):
    return password_context.hash(pw)

def verify_pw(pw:str, hashed_pass: str):
    return password_context.verify(pw,hashed_pass)

hashed_password = get_hashed_pw("admin")

# 해싱된 비밀번호 출력
print(hashed_password)