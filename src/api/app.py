from datetime import datetime
from fastapi import FastAPI

app = FastAPI(title='TMS API', version='1.0.0')


@app.get('/health')
def health_check():
    """Ендпоінт для перевірки стану сервісу."""
    return {
        'status': 'ok',
        'service': 'TMS',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }


@app.get('/tasks')
def get_tasks():
    """Повертає список завдань (заглушка)."""
    return {'tasks': [], 'total': 0}
