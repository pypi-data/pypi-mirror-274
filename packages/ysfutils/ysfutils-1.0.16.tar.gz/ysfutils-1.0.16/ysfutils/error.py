class BaseError(Exception):
    """ 基础异常 """

    def __init__(self, msg, err=None):
        if err:
            self.message = msg + self.__err_msg(err)
        else:
            self.message = msg
        super().__init__(self.message)

    def __repr__(self):
        return self.message

    @staticmethod
    def __err_msg(err):
        """ 格式化err信息, 异常名: 异常消息"""
        err_msg = None
        if isinstance(err, Exception):
            err_msg = f"{type(err).__name__}: {err}"
        return err_msg
