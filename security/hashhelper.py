from pwdlib import PasswordHash

class HashHelper:
    password_hash=PasswordHash.recommended()

    @classmethod
    def hash_password(cls , password:str)-> str:
        return cls.password_hash.hash(password)
    
    @classmethod
    def verify_password(cls , plain_password:str , hashed_password: str)-> bool:
        return cls.password_hash.verify(plain_password , hashed_password)