from pydantic import BaseModel


class BaseUserOut(BaseModel):
    """
    For general objects. (observations, questions, comments etc.)
    """

    user_id: str
    username: str
    f_name: str
    l_name: str
