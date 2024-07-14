from fastapi import HTTPException


class FetchError(HTTPException):
    def __init__(self,
                 status_code: int,
                 detail: str = "Failed fetching resource."
                 ):
        super().__init__(status_code=status_code, detail=detail)

