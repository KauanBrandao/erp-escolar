import unicodedata


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(char for char in normalized if not unicodedata.combining(char))
    return without_accents.strip().lower()


PROFILE_ALIASES = {
    "administrador": "administrador",
    "admin": "administrador",
    "secretaria": "secretaria",
    "coordenacao pedagogica": "coordenacao_pedagogica",
    "coordenacao_pedagogica": "coordenacao_pedagogica",
    "financeiro": "financeiro",
    "responsavel": "responsavel",
}

PROFILE_PERMISSIONS = {
    "administrador": {"*"},
    "secretaria": {
        "alunos:read",
        "alunos:write",
        "responsaveis:read",
        "responsaveis:write",
        "turmas:read",
        "turmas:write",
        "matriculas:read",
        "matriculas:write",
    },
    "coordenacao_pedagogica": {
        "alunos:read",
        "turmas:read",
        "matriculas:read",
        "disciplinas:read",
        "disciplinas:write",
        "notas:read",
        "notas:write",
        "frequencias:read",
        "frequencias:write",
        "comunicados:read",
        "comunicados:write",
    },
    "financeiro": {
        "mensalidades:read",
        "mensalidades:write",
        "pagamentos:read",
        "pagamentos:write",
        "comprovantes:read",
        "comprovantes:write",
    },
    "responsavel": {
        "alunos:read",
        "notas:read",
        "frequencias:read",
        "mensalidades:read",
        "comunicados:read",
    },
}


def normalize_profile_name(profile_name: str) -> str:
    normalized = _normalize_text(profile_name)
    return PROFILE_ALIASES.get(normalized, normalized)


def get_permissions_for_profile(profile_name: str) -> set[str]:
    key = normalize_profile_name(profile_name)
    return PROFILE_PERMISSIONS.get(key, set())


def has_permission(profile_name: str, permission: str) -> bool:
    permissions = get_permissions_for_profile(profile_name)
    if "*" in permissions:
        return True
    return permission in permissions
