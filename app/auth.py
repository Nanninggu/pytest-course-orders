from fastapi import Header, HTTPException

API_TOKEN = "secret-token"


def require_token(x_api_token: str | None = Header(default=None)):
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="인증이 필요합니다.")
