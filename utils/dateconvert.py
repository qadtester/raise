from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def format_datetime_br(dt_string):
    """Converte uma string ISO (UTC) para o fuso horário de Brasília (GMT-3)."""
    if not dt_string:
        return "Nunca"
    try:
        # Se a string terminar em 'Z', ajusta para o formato correto ISO
        if dt_string.endswith("Z"):
            dt_string = dt_string[:-1] + "+00:00"
        
        # Converte a string ISO em objeto datetime
        utc_dt = datetime.fromisoformat(dt_string)
        
        # Se não tiver fuso associado, força ser UTC
        if utc_dt.tzinfo is None:
            utc_dt = utc_dt.replace(tzinfo=timezone.utc)

        # Converte para América/São Paulo
        br_dt = utc_dt.astimezone(ZoneInfo("America/Sao_Paulo"))
        
        # Retorna no formato brasileiro dd/mm/aaaa hh:mm
        return br_dt.strftime("%d/%m/%Y às %H:%M")
    except Exception:
        return dt_string
