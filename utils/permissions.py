# utils/permissions.py

ROLE_PERMISSIONS = {
    "gestor": {
        "can_create": True,
        "can_edit": True,
        "can_delete_items": True,  # Casos de teste, bugs, personas, historias, matriz
        "can_delete_project": False,  # NÃO deleta projeto
    },
    "editor": {
        "can_create": True,
        "can_edit": True,
        "can_delete_items": False,  # NÃO deleta nada
        "can_delete_project": False,
    },
    "leitor": {
        "can_create": False,
        "can_edit": False,
        "can_delete_items": False,
        "can_delete_project": False,
    },
}


def get_user_role(user_info: dict) -> str:
    """Retorna o papel/nível de acesso formatado do usuário."""
    if not user_info:
        return "leitor"
    if user_info.get("is_master") or user_info.get("is_team_owner"):
        return "owner"
    return user_info.get("role", "leitor").lower()


def can_create(user_info: dict) -> bool:
    """Verifica se o usuário tem permissão de criação."""
    role = get_user_role(user_info)
    if role == "owner":
        return True
    return ROLE_PERMISSIONS.get(role, {}).get("can_create", False)


def can_edit(user_info: dict) -> bool:
    """Verifica se o usuário tem permissão de edição."""
    role = get_user_role(user_info)
    if role == "owner":
        return True
    return ROLE_PERMISSIONS.get(role, {}).get("can_edit", False)


def can_delete_items(user_info: dict) -> bool:
    """Verifica se o usuário tem permissão de exclusão de itens (casos de teste, bugs, etc.)."""
    role = get_user_role(user_info)
    if role == "owner":
        return True
    return ROLE_PERMISSIONS.get(role, {}).get("can_delete_items", False)


def can_delete_project(user_info: dict) -> bool:
    """Verifica se o usuário tem permissão para deletar o projeto completo."""
    role = get_user_role(user_info)
    if role == "owner":
        return True
    return ROLE_PERMISSIONS.get(role, {}).get("can_delete_project", False)
