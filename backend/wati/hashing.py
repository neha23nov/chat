import bcrypt

class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        # Hash password and return string
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        # Verify password against hashed password
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
