# 🚗 Agente Rota Certa

**Agente Rota Certa** é um bot inteligente para motoristas de aplicativo que calcula a rota mais curta em quilômetros entre a localização atual e o destino, ajudando a economizar combustível e tempo. A solução ideal para eliminar divergências entre apps populares como Uber e Waze.

---

## 📱 Como funciona

1. O motorista inicia a conversa no Telegram com o comando `/start`.
2. O bot solicita o envio da localização atual via compartilhamento de localização do Telegram.
3. O motorista informa o endereço de destino digitando o texto.
4. O bot utiliza a API do OpenRouteService para calcular a rota mais curta, e retorna:

   * Distância total em quilômetros
   * Tempo estimado do trajeto
   * Link direto para visualizar o percurso no Google Maps

---

## ✅ Funcionalidades principais

* Captura a localização atual via botão de compartilhamento do Telegram
* Recebe o endereço de destino via mensagem de texto
* Integração com a API do OpenRouteService para geocodificação e cálculo preciso da rota
* Apresenta distância e tempo estimado da viagem
* Gera link clicável para abrir o trajeto no Google Maps
* Emite alerta caso a distância ultrapasse 30 km, auxiliando no controle de viagens longas

---

## 🚀 Como executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/agente-rota-certa.git
```

2. Instale as dependências necessárias (exemplo com `pip`):

```bash
pip install -r requirements.txt
```

3. Configure sua API key do OpenRouteService no arquivo de configuração ou variável de ambiente.

4. Execute o bot:

```bash
python bot.py
```

---

## 🧠 Tecnologias utilizadas

* Python
* Biblioteca Python Telegram Bot
* OpenRouteService API
* Google Maps

