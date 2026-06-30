from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings


def get_settings_dependency() -> Settings:
    """Placeholder para injeção de dependências estáticas em rotas."""
    return get_settings()


SettingsDep = Annotated[Settings, Depends(get_settings_dependency)]
