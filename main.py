from aiohttp import web
import database
from datetime import datetime
import aiosqlite

async def handle_index(request):
    # Получаем данные о клиенте
    ip = request.remote
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Записываем посещение
    await database.add_visit(ip, user_agent)
    
    # Возвращаем простой ответ
    return web.Response(text="Welcome to our website!")

async def handle_stats(request):
    period = request.match_info.get('period', 'all')
    
    if period not in ['day', 'month', 'year', 'all']:
        return web.Response(text="Invalid period", status=400)
    
    stats = await database.get_stats(period)
    
    return web.json_response({
        'period': period,
        'total_visits': stats['total'],
        'unique_visits': stats['unique']
    })

async def init_app():
    app = web.Application()
    
    # Инициализация БД
    await database.init_db()
    
    # Добавляем маршруты
    app.router.add_get('/', handle_index)
    app.router.add_get('/stats/{period}', handle_stats)
    app.router.add_get('/stats/', handle_stats)  # Для случая без указания периода
    
    return app

if __name__ == '__main__':
    web.run_app(init_app(), port=8080)