"""
generate_data.py — Генерация данных для тестирования производительности.
Создаёт 200 городов и ~600 маршрутов.
"""

import json
import random
import os


cities_base = [
    # Япония (6)
    {"name": "Токио", "name_en": "Tokyo", "country": "Япония", "type": "hub", "lat": 35.6762, "lon": 139.6503},
    {"name": "Осака", "name_en": "Osaka", "country": "Япония", "type": "major_city", "lat": 34.6937, "lon": 135.5023},
    {"name": "Нагоя", "name_en": "Nagoya", "country": "Япония", "type": "major_city", "lat": 35.1815, "lon": 136.9066},
    {"name": "Саппоро", "name_en": "Sapporo", "country": "Япония", "type": "major_city", "lat": 43.0618, "lon": 141.3545},
    {"name": "Фукуока", "name_en": "Fukuoka", "country": "Япония", "type": "major_city", "lat": 33.5904, "lon": 130.4017},
    {"name": "Хиросима", "name_en": "Hiroshima", "country": "Япония", "type": "major_city", "lat": 34.3853, "lon": 132.4553},
    
    # Южная Корея (5)
    {"name": "Сеул", "name_en": "Seoul", "country": "Южная Корея", "type": "hub", "lat": 37.5665, "lon": 126.9780},
    {"name": "Пусан", "name_en": "Busan", "country": "Южная Корея", "type": "major_city", "lat": 35.1796, "lon": 129.0756},
    {"name": "Инчхон", "name_en": "Incheon", "country": "Южная Корея", "type": "major_city", "lat": 37.4563, "lon": 126.7052},
    {"name": "Тэгу", "name_en": "Daegu", "country": "Южная Корея", "type": "major_city", "lat": 35.8714, "lon": 128.6014},
    {"name": "Тэджон", "name_en": "Daejeon", "country": "Южная Корея", "type": "major_city", "lat": 36.3504, "lon": 127.3845},
    
    # Китай (20)
    {"name": "Пекин", "name_en": "Beijing", "country": "Китай", "type": "hub", "lat": 39.9042, "lon": 116.4074},
    {"name": "Шанхай", "name_en": "Shanghai", "country": "Китай", "type": "hub", "lat": 31.2304, "lon": 121.4737},
    {"name": "Гонконг", "name_en": "Hong Kong", "country": "Китай (САР)", "type": "hub", "lat": 22.3193, "lon": 114.1694},
    {"name": "Гуанчжоу", "name_en": "Guangzhou", "country": "Китай", "type": "major_city", "lat": 23.1291, "lon": 113.2644},
    {"name": "Шэньчжэнь", "name_en": "Shenzhen", "country": "Китай", "type": "major_city", "lat": 22.5431, "lon": 114.0579},
    {"name": "Чэнду", "name_en": "Chengdu", "country": "Китай", "type": "major_city", "lat": 30.5728, "lon": 104.0668},
    {"name": "Чунцин", "name_en": "Chongqing", "country": "Китай", "type": "major_city", "lat": 29.5630, "lon": 106.5516},
    {"name": "Тяньцзинь", "name_en": "Tianjin", "country": "Китай", "type": "major_city", "lat": 39.0842, "lon": 117.2009},
    {"name": "Ханчжоу", "name_en": "Hangzhou", "country": "Китай", "type": "major_city", "lat": 30.2741, "lon": 120.1551},
    {"name": "Нанкин", "name_en": "Nanjing", "country": "Китай", "type": "major_city", "lat": 32.0603, "lon": 118.7969},
    {"name": "Ухань", "name_en": "Wuhan", "country": "Китай", "type": "major_city", "lat": 30.5928, "lon": 114.3055},
    {"name": "Сиань", "name_en": "Xi'an", "country": "Китай", "type": "major_city", "lat": 34.3416, "lon": 108.9398},
    {"name": "Шэньян", "name_en": "Shenyang", "country": "Китай", "type": "major_city", "lat": 41.8057, "lon": 123.4315},
    {"name": "Циндао", "name_en": "Qingdao", "country": "Китай", "type": "major_city", "lat": 36.0671, "lon": 120.3826},
    {"name": "Далянь", "name_en": "Dalian", "country": "Китай", "type": "major_city", "lat": 38.9140, "lon": 121.6147},
    {"name": "Чанша", "name_en": "Changsha", "country": "Китай", "type": "major_city", "lat": 28.2282, "lon": 112.9388},
    {"name": "Фучжоу", "name_en": "Fuzhou", "country": "Китай", "type": "major_city", "lat": 26.0745, "lon": 119.2965},
    {"name": "Наньнин", "name_en": "Nanning", "country": "Китай", "type": "major_city", "lat": 22.8176, "lon": 108.3665},
    {"name": "Гуйян", "name_en": "Guiyang", "country": "Китай", "type": "major_city", "lat": 26.5783, "lon": 106.7135},
    {"name": "Ланьчжоу", "name_en": "Lanzhou", "country": "Китай", "type": "major_city", "lat": 36.0611, "lon": 103.8343},
    
    # Тайвань (3)
    {"name": "Тайбэй", "name_en": "Taipei", "country": "Тайвань", "type": "capital", "lat": 25.0330, "lon": 121.5654},
    {"name": "Гаосюн", "name_en": "Kaohsiung", "country": "Тайвань", "type": "major_city", "lat": 22.6273, "lon": 120.3014},
    {"name": "Тайчжун", "name_en": "Taichung", "country": "Тайвань", "type": "major_city", "lat": 24.1477, "lon": 120.6736},
    
    # Филиппины (3)
    {"name": "Манила", "name_en": "Manila", "country": "Филиппины", "type": "capital", "lat": 14.5995, "lon": 120.9842},
    {"name": "Себу", "name_en": "Cebu", "country": "Филиппины", "type": "major_city", "lat": 10.3157, "lon": 123.8854},
    {"name": "Давао", "name_en": "Davao", "country": "Филиппины", "type": "major_city", "lat": 7.1907, "lon": 125.4553},
    
    # Индонезия (6)
    {"name": "Джакарта", "name_en": "Jakarta", "country": "Индонезия", "type": "capital", "lat": -6.2088, "lon": 106.8456},
    {"name": "Сурабая", "name_en": "Surabaya", "country": "Индонезия", "type": "major_city", "lat": -7.2575, "lon": 112.7521},
    {"name": "Бандунг", "name_en": "Bandung", "country": "Индонезия", "type": "major_city", "lat": -6.9175, "lon": 107.6191},
    {"name": "Медан", "name_en": "Medan", "country": "Индонезия", "type": "major_city", "lat": 3.5952, "lon": 98.6722},
    {"name": "Денпасар", "name_en": "Denpasar", "country": "Индонезия", "type": "major_city", "lat": -8.6705, "lon": 115.2126},
    {"name": "Макасар", "name_en": "Makassar", "country": "Индонезия", "type": "major_city", "lat": -5.1477, "lon": 119.4327},
    
    # Малайзия (4)
    {"name": "Куала-Лумпур", "name_en": "Kuala Lumpur", "country": "Малайзия", "type": "hub", "lat": 3.1390, "lon": 101.6869},
    {"name": "Джохор-Бару", "name_en": "Johor Bahru", "country": "Малайзия", "type": "major_city", "lat": 1.4927, "lon": 103.7414},
    {"name": "Пенанг", "name_en": "Penang", "country": "Малайзия", "type": "major_city", "lat": 5.4164, "lon": 100.3327},
    {"name": "Кота-Кинабалу", "name_en": "Kota Kinabalu", "country": "Малайзия", "type": "major_city", "lat": 5.9804, "lon": 116.0735},
    
    # Сингапур (1)
    {"name": "Сингапур", "name_en": "Singapore", "country": "Сингапур", "type": "hub", "lat": 1.3521, "lon": 103.8198},
    
    # Таиланд (4)
    {"name": "Бангкок", "name_en": "Bangkok", "country": "Таиланд", "type": "hub", "lat": 13.7563, "lon": 100.5018},
    {"name": "Чиангмай", "name_en": "Chiang Mai", "country": "Таиланд", "type": "major_city", "lat": 18.7883, "lon": 98.9853},
    {"name": "Пхукет", "name_en": "Phuket", "country": "Таиланд", "type": "major_city", "lat": 7.8804, "lon": 98.3923},
    {"name": "Паттайя", "name_en": "Pattaya", "country": "Таиланд", "type": "major_city", "lat": 12.9236, "lon": 100.8824},
    
    # Вьетнам (4)
    {"name": "Ханой", "name_en": "Hanoi", "country": "Вьетнам", "type": "capital", "lat": 21.0278, "lon": 105.8342},
    {"name": "Хошимин", "name_en": "Ho Chi Minh", "country": "Вьетнам", "type": "major_city", "lat": 10.8231, "lon": 106.6297},
    {"name": "Дананг", "name_en": "Da Nang", "country": "Вьетнам", "type": "major_city", "lat": 16.0544, "lon": 108.2022},
    {"name": "Нячанг", "name_en": "Nha Trang", "country": "Вьетнам", "type": "major_city", "lat": 12.2388, "lon": 109.1967},
    
    # Мьянма (2)
    {"name": "Янгон", "name_en": "Yangon", "country": "Мьянма", "type": "capital", "lat": 16.8661, "lon": 96.1951},
    {"name": "Мандалай", "name_en": "Mandalay", "country": "Мьянма", "type": "major_city", "lat": 21.9588, "lon": 96.0891},
    
    # Бангладеш (2)
    {"name": "Дакка", "name_en": "Dhaka", "country": "Бангладеш", "type": "capital", "lat": 23.8103, "lon": 90.4125},
    {"name": "Читтагонг", "name_en": "Chittagong", "country": "Бангладеш", "type": "major_city", "lat": 22.3569, "lon": 91.7832},
    
    # Индия (20)
    {"name": "Дели", "name_en": "Delhi", "country": "Индия", "type": "capital", "lat": 28.6139, "lon": 77.2090},
    {"name": "Мумбаи", "name_en": "Mumbai", "country": "Индия", "type": "hub", "lat": 19.0760, "lon": 72.8777},
    {"name": "Бангалор", "name_en": "Bangalore", "country": "Индия", "type": "major_city", "lat": 12.9716, "lon": 77.5946},
    {"name": "Ченнай", "name_en": "Chennai", "country": "Индия", "type": "major_city", "lat": 13.0827, "lon": 80.2707},
    {"name": "Хайдарабад", "name_en": "Hyderabad", "country": "Индия", "type": "major_city", "lat": 17.3850, "lon": 78.4867},
    {"name": "Калькутта", "name_en": "Kolkata", "country": "Индия", "type": "major_city", "lat": 22.5726, "lon": 88.3639},
    {"name": "Пуна", "name_en": "Pune", "country": "Индия", "type": "major_city", "lat": 18.5204, "lon": 73.8567},
    {"name": "Ахмедабад", "name_en": "Ahmedabad", "country": "Индия", "type": "major_city", "lat": 23.0225, "lon": 72.5714},
    {"name": "Сурат", "name_en": "Surat", "country": "Индия", "type": "major_city", "lat": 21.1702, "lon": 72.8311},
    {"name": "Джайпур", "name_en": "Jaipur", "country": "Индия", "type": "major_city", "lat": 26.9124, "lon": 75.7873},
    {"name": "Лакхнау", "name_en": "Lucknow", "country": "Индия", "type": "major_city", "lat": 26.8467, "lon": 80.9462},
    {"name": "Нагпур", "name_en": "Nagpur", "country": "Индия", "type": "major_city", "lat": 21.1458, "lon": 79.0882},
    {"name": "Индаур", "name_en": "Indore", "country": "Индия", "type": "major_city", "lat": 22.7196, "lon": 75.8577},
    {"name": "Бхопал", "name_en": "Bhopal", "country": "Индия", "type": "major_city", "lat": 23.2599, "lon": 77.4126},
    {"name": "Висахапатнам", "name_en": "Visakhapatnam", "country": "Индия", "type": "major_city", "lat": 17.6868, "lon": 83.2185},
    {"name": "Патна", "name_en": "Patna", "country": "Индия", "type": "major_city", "lat": 25.5941, "lon": 85.1376},
    {"name": "Вадодара", "name_en": "Vadodara", "country": "Индия", "type": "major_city", "lat": 22.3072, "lon": 73.1812},
    {"name": "Газиабад", "name_en": "Ghaziabad", "country": "Индия", "type": "major_city", "lat": 28.6692, "lon": 77.4538},
    {"name": "Канпур", "name_en": "Kanpur", "country": "Индия", "type": "major_city", "lat": 26.4499, "lon": 80.3319},
    {"name": "Коимбатур", "name_en": "Coimbatore", "country": "Индия", "type": "major_city", "lat": 11.0168, "lon": 76.9558},
    
    # Пакистан (6)
    {"name": "Карачи", "name_en": "Karachi", "country": "Пакистан", "type": "major_city", "lat": 24.8607, "lon": 67.0011},
    {"name": "Лахор", "name_en": "Lahore", "country": "Пакистан", "type": "major_city", "lat": 31.5204, "lon": 74.3587},
    {"name": "Исламабад", "name_en": "Islamabad", "country": "Пакистан", "type": "capital", "lat": 33.6844, "lon": 73.0479},
    {"name": "Фейсалабад", "name_en": "Faisalabad", "country": "Пакистан", "type": "major_city", "lat": 31.4504, "lon": 73.1350},
    {"name": "Равалпинди", "name_en": "Rawalpindi", "country": "Пакистан", "type": "major_city", "lat": 33.5651, "lon": 73.0169},
    {"name": "Мултан", "name_en": "Multan", "country": "Пакистан", "type": "major_city", "lat": 30.1575, "lon": 71.5249},
    
    # Шри-Ланка (1)
    {"name": "Коломбо", "name_en": "Colombo", "country": "Шри-Ланка", "type": "capital", "lat": 6.9271, "lon": 79.8612},
    
    # Непал (1)
    {"name": "Катманду", "name_en": "Kathmandu", "country": "Непал", "type": "capital", "lat": 27.7172, "lon": 85.3240},
    
    # Иран (5)
    {"name": "Тегеран", "name_en": "Tehran", "country": "Иран", "type": "capital", "lat": 35.6892, "lon": 51.3890},
    {"name": "Шираз", "name_en": "Shiraz", "country": "Иран", "type": "major_city", "lat": 29.5918, "lon": 52.5837},
    {"name": "Исфахан", "name_en": "Isfahan", "country": "Иран", "type": "major_city", "lat": 32.6546, "lon": 51.6680},
    {"name": "Мешхед", "name_en": "Mashhad", "country": "Иран", "type": "major_city", "lat": 36.2972, "lon": 59.6062},
    {"name": "Тебриз", "name_en": "Tabriz", "country": "Иран", "type": "major_city", "lat": 38.0800, "lon": 46.2919},
    
    # Ирак (3)
    {"name": "Багдад", "name_en": "Baghdad", "country": "Ирак", "type": "capital", "lat": 33.3152, "lon": 44.3661},
    {"name": "Эрбиль", "name_en": "Erbil", "country": "Ирак", "type": "major_city", "lat": 36.1825, "lon": 44.0085},
    {"name": "Басра", "name_en": "Basra", "country": "Ирак", "type": "major_city", "lat": 30.5085, "lon": 47.7804},
    
    # Саудовская Аравия (5)
    {"name": "Эр-Рияд", "name_en": "Riyadh", "country": "Саудовская Аравия", "type": "capital", "lat": 24.7136, "lon": 46.6753},
    {"name": "Джидда", "name_en": "Jeddah", "country": "Саудовская Аравия", "type": "major_city", "lat": 21.4858, "lon": 39.1925},
    {"name": "Мекка", "name_en": "Mecca", "country": "Саудовская Аравия", "type": "major_city", "lat": 21.3891, "lon": 39.8579},
    {"name": "Медина", "name_en": "Medina", "country": "Саудовская Аравия", "type": "major_city", "lat": 24.4672, "lon": 39.6112},
    {"name": "Даммам", "name_en": "Dammam", "country": "Саудовская Аравия", "type": "major_city", "lat": 26.3927, "lon": 49.9777},
    
    # ОАЭ (4)
    {"name": "Дубай", "name_en": "Dubai", "country": "ОАЭ", "type": "hub", "lat": 25.2048, "lon": 55.2708},
    {"name": "Абу-Даби", "name_en": "Abu Dhabi", "country": "ОАЭ", "type": "capital", "lat": 24.4539, "lon": 54.3773},
    {"name": "Шарджа", "name_en": "Sharjah", "country": "ОАЭ", "type": "major_city", "lat": 25.3463, "lon": 55.4209},
    {"name": "Аджман", "name_en": "Ajman", "country": "ОАЭ", "type": "major_city", "lat": 25.4052, "lon": 55.5136},
    
    # Катар (1)
    {"name": "Доха", "name_en": "Doha", "country": "Катар", "type": "hub", "lat": 25.2854, "lon": 51.5310},
    
    # Турция (7)
    {"name": "Стамбул", "name_en": "Istanbul", "country": "Турция", "type": "hub", "lat": 41.0082, "lon": 28.9784},
    {"name": "Анкара", "name_en": "Ankara", "country": "Турция", "type": "capital", "lat": 39.9334, "lon": 32.8597},
    {"name": "Измир", "name_en": "Izmir", "country": "Турция", "type": "major_city", "lat": 38.4237, "lon": 27.1428},
    {"name": "Бурса", "name_en": "Bursa", "country": "Турция", "type": "major_city", "lat": 40.1826, "lon": 29.0670},
    {"name": "Анталья", "name_en": "Antalya", "country": "Турция", "type": "major_city", "lat": 36.8969, "lon": 30.7133},
    {"name": "Адана", "name_en": "Adana", "country": "Турция", "type": "major_city", "lat": 37.0000, "lon": 35.3213},
    {"name": "Конья", "name_en": "Konya", "country": "Турция", "type": "major_city", "lat": 37.8714, "lon": 32.4994},
    
    # Иордания (1)
    {"name": "Амман", "name_en": "Amman", "country": "Иордания", "type": "capital", "lat": 31.9454, "lon": 35.9284},
    
    # Ливан (1)
    {"name": "Бейрут", "name_en": "Beirut", "country": "Ливан", "type": "capital", "lat": 33.8938, "lon": 35.5018},
    
    # Сирия (1)
    {"name": "Дамаск", "name_en": "Damascus", "country": "Сирия", "type": "capital", "lat": 33.5138, "lon": 36.2765},
    
    # Кувейт (1)
    {"name": "Кувейт", "name_en": "Kuwait City", "country": "Кувейт", "type": "capital", "lat": 29.3759, "lon": 47.9774},
    
    # Бахрейн (1)
    {"name": "Манама", "name_en": "Manama", "country": "Бахрейн", "type": "capital", "lat": 26.2285, "lon": 50.5860},
    
    # Оман (1)
    {"name": "Маскат", "name_en": "Muscat", "country": "Оман", "type": "capital", "lat": 23.5880, "lon": 58.3829},
    
    # Узбекистан (3)
    {"name": "Ташкент", "name_en": "Tashkent", "country": "Узбекистан", "type": "capital", "lat": 41.2995, "lon": 69.2401},
    {"name": "Самарканд", "name_en": "Samarkand", "country": "Узбекистан", "type": "major_city", "lat": 39.6270, "lon": 66.9750},
    {"name": "Бухара", "name_en": "Bukhara", "country": "Узбекистан", "type": "major_city", "lat": 39.7681, "lon": 64.4556},
    
    # Казахстан (4)
    {"name": "Алматы", "name_en": "Almaty", "country": "Казахстан", "type": "major_city", "lat": 43.2220, "lon": 76.8512},
    {"name": "Астана", "name_en": "Astana", "country": "Казахстан", "type": "capital", "lat": 51.1694, "lon": 71.4491},
    {"name": "Шымкент", "name_en": "Shymkent", "country": "Казахстан", "type": "major_city", "lat": 42.3400, "lon": 69.5963},
    {"name": "Актау", "name_en": "Aktau", "country": "Казахстан", "type": "major_city", "lat": 43.6513, "lon": 51.1592},
    
    # Кыргызстан (1)
    {"name": "Бишкек", "name_en": "Bishkek", "country": "Кыргызстан", "type": "capital", "lat": 42.8746, "lon": 74.5698},
    
    # Туркменистан (1)
    {"name": "Ашхабад", "name_en": "Ashgabat", "country": "Туркменистан", "type": "capital", "lat": 37.9601, "lon": 58.3261},
    
    # Азербайджан (1)
    {"name": "Баку", "name_en": "Baku", "country": "Азербайджан", "type": "capital", "lat": 40.4093, "lon": 49.8671},
    
    # Грузия (1)
    {"name": "Тбилиси", "name_en": "Tbilisi", "country": "Грузия", "type": "capital", "lat": 41.7151, "lon": 44.8271},
    
    # Армения (1)
    {"name": "Ереван", "name_en": "Yerevan", "country": "Армения", "type": "capital", "lat": 40.1792, "lon": 44.4991},
]


#генерация маршрутов

def generate_routes(cities, target_routes=600):
    """Генерирует маршруты между городами."""
    city_ids = [city["_id"] for city in cities]
    routes = []
    used_pairs = set()
    
    hubs = [c["_id"] for c in cities if c["type"] == "hub"]
    
    for i in range(len(hubs)):
        for j in range(i + 1, len(hubs)):
            from_id = hubs[i]
            to_id = hubs[j]
            weight = random.randint(300, 8000)
            routes.append({
                "from": from_id,
                "to": to_id,
                "weight": weight,
                "airline": random.choice(["Emirates", "Turkish Airlines", "Qatar Airways", 
                                         "Singapore Airlines", "Cathay Pacific", "Air China",
                                         "Korean Air", "Japan Airlines", "Thai Airways",
                                         "Malaysia Airlines", "Air India", "Etihad"])
            })
            used_pairs.add((from_id, to_id))
            used_pairs.add((to_id, from_id))
    
    attempts = 0
    while len(routes) < target_routes and attempts < 20000:
        attempts += 1
        from_id = random.choice(city_ids)
        to_id = random.choice(city_ids)
        
        if from_id == to_id:
            continue
        if (from_id, to_id) in used_pairs:
            continue
        
        weight = random.randint(200, 9000)
        routes.append({
            "from": from_id,
            "to": to_id,
            "weight": weight,
            "airline": random.choice(["Emirates", "Turkish Airlines", "Qatar Airways", 
                                     "Singapore Airlines", "Cathay Pacific", "Air China",
                                     "Korean Air", "Japan Airlines", "Thai Airways",
                                     "Malaysia Airlines", "Air India", "Etihad",
                                     "IndiGo", "China Eastern", "China Southern",
                                     "Lufthansa", "British Airways", "KLM"])
        })
        used_pairs.add((from_id, to_id))
        used_pairs.add((to_id, from_id))
    
    return routes


#создание json-файлов

def generate_data():
    """Генерирует данные и сохраняет в JSON-файлы."""
    
    for i, city in enumerate(cities_base):
        city["_id"] = i + 1
    
    print(f"Генерация маршрутов для {len(cities_base)} городов...")
    routes = generate_routes(cities_base, target_routes=600)
    print(f"Сгенерировано {len(routes)} маршрутов")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    cities_file = os.path.join(base_dir, "data", "cities.json")
    routes_file = os.path.join(base_dir, "data", "routes.json")
    
    with open(cities_file, 'w', encoding='utf-8') as f:
        json.dump(cities_base, f, ensure_ascii=False, indent=2)
    print(f"Города сохранены в {cities_file}")
    
    with open(routes_file, 'w', encoding='utf-8') as f:
        json.dump(routes, f, ensure_ascii=False, indent=2)
    print(f"Маршруты сохранены в {routes_file}")
    
    # Статистика
    hubs = [c for c in cities_base if c["type"] == "hub"]
    capitals = [c for c in cities_base if c["type"] == "capital"]
    major_cities = [c for c in cities_base if c["type"] == "major_city"]
    
    return cities_base, routes


if __name__ == "__main__":
    generate_data()