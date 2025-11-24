from aiohttp import web
import database
from datetime import datetime
import aiosqlite
from picGenerator import make_counter_png

async def handle_index(request):
    ip = request.remote
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    await database.add_visit(ip, user_agent)
    
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
    app.router.add_get('/counter.png', handle_counter_png)

    return app

async def handle_counter_png(request):
    # Получаем количество посещений
    stats = await database.get_stats('all')
    count = stats['total']

    # Генерируем картинку (получаем BytesIO)
    output = make_counter_png(count)
    return web.Response(body=output.read(), content_type='image/png')


if __name__ == '__main__':
    web.run_app(init_app(), port=8080)