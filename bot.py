import logging
import httpx
from geopy.distance import geodesic
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Configurações dos logs
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Chaves e tokens
TELEGRAM_BOT_TOKEN = "7900619637:AAHdCmDYYLjr66V-lt382KnsKJENTZKP8RU"
ORS_API_KEY = "5b3ce3597851110001cf624811291c65b6b9693d719ab5232336921c5c46af395409c5ff1520cebf"

# Armazenar localizações temporariamente
user_data = {}

# Função para lidar com o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location_button = KeyboardButton(text="Enviar localização", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Olá! Por favor, envie sua localização atual:", reply_markup=reply_markup)

# Função para salvar a localização atual do motorista
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    location = update.message.location
    user_data[user_id] = {"origem": (location.latitude, location.longitude)}
    await update.message.reply_text("Localização recebida! Agora, envie o endereço de destino.")

# Função para obter coordenadas do destino via OpenRouteService
async def geocode_address(address: str) -> tuple:
    url = "https://api.openrouteservice.org/geocode/search"
    headers = {"Authorization": ORS_API_KEY}
    params = {"text": address, "size": 1}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            coords = data["features"][0]["geometry"]["coordinates"]
            return coords[1], coords[0]  # latitude, longitude
        return None

# Função para calcular rota usando OpenRouteService
async def calcular_rota(origem: tuple, destino: tuple) -> dict:
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
    body = {"coordinates": [[origem[1], origem[0]], [destino[1], destino[0]]]}  # lng, lat
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json()
        return None

# Função para lidar com o endereço de destino
async def destination_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    destino = update.message.text
    if user_id not in user_data:
        await update.message.reply_text("Por favor, envie sua localização primeiro com /start.")
        return

    coordenadas_destino = await geocode_address(destino)
    if not coordenadas_destino:
        await update.message.reply_text("Não foi possível encontrar o endereço. Tente novamente.")
        return

    origem = user_data[user_id]["origem"]
    rota = await calcular_rota(origem, coordenadas_destino)
    if rota:
        distancia_km = rota["routes"][0]["summary"]["distance"] / 1000
        duracao_min = rota["routes"][0]["summary"]["duration"] / 60
        await update.message.reply_text(f"A rota mais curta tem {distancia_km:.2f} km e leva cerca de {duracao_min:.1f} minutos.")
    else:
        await update.message.reply_text("Erro ao calcular a rota. Tente novamente.")

# Função principal
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, destination_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
