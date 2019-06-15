request_user = None


class GlobalRequestMiddleware(object):
    """
    这个中间键提供了一个功能：根据用户不同，修改后台管理界面的标题信息，还提供了一个全局 request_user
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        if request.user.is_authenticated:
            global request_user
            request_user = request.user


def get_request_user_id():
    if request_user is None:
        return None
    return request_user.id