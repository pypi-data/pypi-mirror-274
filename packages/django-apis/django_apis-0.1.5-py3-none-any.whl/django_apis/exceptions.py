class UnknownError(RuntimeError):
    args = (-1, "系统开小差了，请联系管理员或稍候再试 ^_^")


class BusinessError(RuntimeError):
    args = (2, "业务逻辑错误")


class InputValidationError(BusinessError):
    """请求参数验证失败。"""

    def __init__(self, form):
        self.form = form

    def json(self):
        messages = []
        for field_name, errors in self.form.errors.as_data().items():
            infos = []
            for error in errors:
                if error.message:
                    message = str(error.message)
                    if message not in infos:
                        infos.append(message)
                for message in error.messages:
                    message = str(message)
                    if message not in infos:
                        infos.append(message)
            message = "".join(infos)
            messages.append(f"{field_name}: {message}")
        return {
            "code": 201,
            "message": "\n".join(messages),
        }


ValidationError = InputValidationError


class JsonPayloadDecodeError(BusinessError):
    args = (202, "请求体不是有效的json格式，无法正常解析。")


class RequestMethodNotAllowed(BusinessError):
    args = (203, "不允许的HTTP请求类型。")


class Forbidden(BusinessError):
    args = (403, "禁止访问...")
