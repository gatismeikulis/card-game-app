import dramatiq
from django.core.cache import cache

from .dependencies import table_manager


@dramatiq.actor()
def demo_task(table_id: str) -> None:
    try:
        print(f"Received demo task for table {table_id}")
        table = table_manager.get_table(table_id)
        status = table.status
        cache.set(f"demo_task_{table_id}", status.value)
        print(f"Table found, status stored in cache")
    except Exception as e:
        print(f"Error: {e}")
