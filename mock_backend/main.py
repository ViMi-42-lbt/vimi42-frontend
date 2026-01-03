import time
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse



app = FastAPI(title="Mock Auth Backend")

# ─────────────────────────────
# Models
# ─────────────────────────────

class RegisterRequest(BaseModel):
    email: str
    password: str
    person_type: str
    display_name: str
    # Campos PF
    full_name: str | None = None
    cpf: str | None = None
    birth_date: str | None = None
    # Campos PJ
    corporate_name: str | None = None
    cnpj: str | None = None
    is_mei: bool = False

USERS_DB = []

class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ValidateResetTokenRequest(BaseModel):
    token: str


class ResetPasswordRequest(BaseModel):
    reset_session: str
    new_password: str


# ─────────────────────────────
# Fake database (em memória)
# ─────────────────────────────

FAKE_USER = {
    "email": "teste@vimi42.com",
    "password": "Senha@123",
}

PASSWORD_RESET = {
    "token": "fake-token-123",
    "expires_at": datetime.utcnow() + timedelta(minutes=15),
    "attempts": 0,
    "validated_at": None,
    "reset_session": None,
}

# ─────────────────────────────
# Routes
# ─────────────────────────────

@app.post("/auth/register")
def register(data: dict):
    email = data.get("email")
    person_type = data.get("person_type")
    
    # Simulação de verificação de campos obrigatórios no Backend
    if person_type == "PF":
        required = ["full_name", "cpf", "birth_date"]
    else:
        required = ["corporate_name", "cnpj"]
    
    for field in required:
        if not data.get(field):
            raise HTTPException(
                status_code=422, 
                detail=f"O campo {field} é obrigatório para {person_type}"
            )

    if any(u["email"] == email for u in USERS_DB) or email == FAKE_USER["email"]:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    
    print(f"[MOCK BACKEND] Cadastro Recebido: {data}")
    USERS_DB.append(data)
    return {"success": True, "message": "Usuário criado com sucesso"}

@app.post("/auth/complete-registration")
def complete_registration(data: dict = Body(...)):
    """
    Finaliza o cadastro social e salva no banco fake.
    """
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=422, detail="Email ausente no payload complementar")

    print(f"[MOCK] Finalizando registro social para: {email}")
    print(f"[MOCK] Dados recebidos (sanitizados): {data}")

    # Remove registro antigo se existir para evitar duplicidade no mock
    global USERS_DB
    USERS_DB = [u for u in USERS_DB if u.get("email") != email]
    
    # Adiciona o usuário com perfil completo
    USERS_DB.append(data)
    
    return {
        "success": True, 
        "message": "Cadastro social finalizado e perfil criado no mock."
    }

@app.post("/auth/login")
def login(data: dict): # Simplificado para aceitar dict
    email = data.get("email")
    password = data.get("password")
    
    if email == FAKE_USER["email"] and password == FAKE_USER["password"]:
        return {
            "success": True,
            "token": "jwt-fake-token",
            "user": {"email": email, "name": "Usuário Fake"}
        }
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.post("/auth/forgot-password")
def forgot_password(payload: dict):
    email = payload.get("email")

    if not email:
        raise HTTPException(status_code=422, detail="Email é obrigatório")

    if email != FAKE_USER["email"]:
        raise HTTPException(status_code=404, detail="Email não cadastrado")

    # ──────────────── Gerar novo token e reset_session ────────────────
    PASSWORD_RESET["token"] = "fake-token-123"
    PASSWORD_RESET["expires_at"] = datetime.utcnow() + timedelta(minutes=15)
    PASSWORD_RESET["attempts"] = 0
    PASSWORD_RESET["validated_at"] = None
    PASSWORD_RESET["reset_session"] = None
    # ────────────────────────────────────────────────────────────────

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Token enviado com sucesso"
        }
    )


@app.post("/auth/validate-reset-token")
def validate_reset_token(data: ValidateResetTokenRequest):
    if PASSWORD_RESET["attempts"] >= 3:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Token bloqueado por excesso de tentativas",
        )

    if datetime.utcnow() > PASSWORD_RESET["expires_at"]:
        raise HTTPException(status_code=400, detail="Token expirado")

    if data.token != PASSWORD_RESET["token"]:
        PASSWORD_RESET["attempts"] += 1
        remaining = 3 - PASSWORD_RESET["attempts"]

        raise HTTPException(
            status_code=422,
            detail=f"Token inválido. Tentativas restantes: {remaining}",
        )

    reset_session = str(uuid4())

    PASSWORD_RESET.update({
        "validated_at": datetime.utcnow(),
        "reset_session": reset_session,
    })

    return {
        "success": True,
        "reset_session": reset_session,
    }

@app.post("/auth/reset-password")
def reset_password(data: ResetPasswordRequest):
    if PASSWORD_RESET["reset_session"] != data.reset_session:
        raise HTTPException(status_code=403, detail="Sessão inválida")

    FAKE_USER["password"] = data.new_password

    PASSWORD_RESET.update({
        "token": None,
        "reset_session": None,
        "validated_at": None,
        "attempts": 0,
    })

    return {
        "success": True,
        "message": "Senha redefinida com sucesso",
    }