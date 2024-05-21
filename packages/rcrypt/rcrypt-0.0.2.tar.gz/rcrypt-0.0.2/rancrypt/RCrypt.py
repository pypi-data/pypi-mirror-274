import bcrypt


class DataBaseCrypt(object):
    """
    数据库加密
    采用的是 BCrypt 加密算法
    每个用户独立生成属于自己的 salt
    """

    @staticmethod
    def get_salt():
        """ 生成随机 salt """
        salt = bcrypt.gensalt()
        return salt.decode("utf8")

    @staticmethod
    def get_hash(password, salt):
        """ 使用 password 和 salt 通过 BCrypt 加密算法的 hash 值 """
        phash = bcrypt.hashpw(password.encode(), salt.encode())
        return phash.decode("utf8")

    @staticmethod
    def get_hash_and_salt(password):
        """ 获取 password 生成的 hash 和随机 salt """
        salt = DataBaseCrypt.get_salt()
        phash = DataBaseCrypt.get_hash(password, salt)

        return phash, salt

    @staticmethod
    def auth(password, phash, salt):
        """
        认证
        比较 password、salt 生成 _hash 是否与 phash 相同
        """
        _hash = DataBaseCrypt.get_hash(password, salt)
        return _hash == phash
