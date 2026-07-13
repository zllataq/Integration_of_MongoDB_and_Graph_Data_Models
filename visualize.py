"""
visualize.py — Визуализация графа и алгоритм Дейкстры.
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from src.config import get_collections
from src.queries import get_city_by_id, get_city_by_name, get_neighbors


# 1. Загрузка данных из MongoDB


def build_graph_from_mongodb():
    """
    Загружает данные из MongoDB и строит граф NetworkX.
    
    Returns:
        nx.Graph: Граф с атрибутами вершин и рёбер
    """
    cities_collection, routes_collection = get_collections()
    
    G = nx.Graph()
    
    cities = list(cities_collection.find())
    for city in cities:
        G.add_node(
            city["_id"],
            name=city["name"],
            name_en=city["name_en"],
            country=city["country"],
            type=city["type"],
            lat=city.get("lat", 0),
            lon=city.get("lon", 0)
        )
    
    routes = list(routes_collection.find())
    for route in routes:
        G.add_edge(
            route["from"],
            route["to"],
            weight=route["weight"],
            airline=route.get("airline", "Unknown")
        )
    
    print(f"\nХарактеристики графа:")
    print(f"   Вершин: {G.number_of_nodes()}")
    print(f"   Рёбер: {G.number_of_edges()}")
    
    return G


# 2. Визуализация графов


def visualize_graph(G, title="Граф авиаперелётов"):
    """
    Визуализирует граф с цветовой кодировкой по типу города.
    
    Args:
        G: граф NetworkX
        title: заголовок графика
    """
    # Цвета для разных типов городов
    color_map = {
        "hub": "#FF4444",       # Красный для хабов
        "capital": "#4488FF",   # Синий для столиц
        "major_city": "#44BB44" # Зелёный для крупных городов
    }
    
    # Получаем цвета для каждой вершины
    node_colors = []
    for node in G.nodes():
        node_type = G.nodes[node].get("type", "major_city")
        node_colors.append(color_map.get(node_type, "#888888"))
    
    # Подписи для узлов (названия городов)
    labels = {node: G.nodes[node]["name"] for node in G.nodes()}
    
    # Размер узлов в зависимости от типа
    node_sizes = []
    for node in G.nodes():
        node_type = G.nodes[node].get("type", "major_city")
        if node_type == "hub":
            node_sizes.append(1200)
        elif node_type == "capital":
            node_sizes.append(800)
        else:
            node_sizes.append(500)
    
    # Позиционирование узлов по координатам (если есть)
    pos = {}
    for node in G.nodes():
        lat = G.nodes[node].get("lat", 0)
        lon = G.nodes[node].get("lon", 0)
        if lat != 0 and lon != 0:
            pos[node] = (lon, lat)
    
    # Если координат нет — используем spring layout
    if not pos or len(pos) < G.number_of_nodes():
        pos = nx.spring_layout(G, k=1.5, iterations=100)
    
    # Создаём рисунок
    plt.figure(figsize=(20, 16))
    
    # Рисуем рёбра (с разной толщиной в зависимости от веса)
    edges = G.edges(data=True)
    for u, v, data in edges:
        weight = data.get("weight", 1)
        # Нормализуем толщину (от 0.5 до 3)
        width = max(0.5, min(3, weight / 1000))
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], 
                               width=width, alpha=0.5, edge_color='gray')
    
    # Рисуем узлы
    nx.draw_networkx_nodes(G, pos, 
                           node_color=node_colors, 
                           node_size=node_sizes,
                           alpha=0.9,
                           edgecolors='black',
                           linewidths=1.5)
    
    # Подписи узлов
    nx.draw_networkx_labels(G, pos, labels, 
                            font_size=8, 
                            font_weight='bold',
                            bbox=dict(boxstyle="round,pad=0.2", 
                                     facecolor="white", 
                                     edgecolor="none", 
                                     alpha=0.7))
    
    # Легенда
    legend_elements = [
        mpatches.Patch(facecolor='#FF4444', label='Хаб', edgecolor='black'),
        mpatches.Patch(facecolor='#4488FF', label='Столица', edgecolor='black'),
        mpatches.Patch(facecolor='#44BB44', label='Крупный город', edgecolor='black'),
        Line2D([0], [0], color='gray', linewidth=2, label='Маршрут (толщина = расстояние)')
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=12)
    
    # Заголовок
    plt.title(title, fontsize=20, fontweight='bold', pad=20)
    plt.xlabel("Долгота", fontsize=12)
    plt.ylabel("Широта", fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Сохраняем в файл
    output_file = "output/asia_flights_graph.png"
    os.makedirs("output", exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Граф сохранён в {output_file}")
    
    plt.show()


# 3. Алгоритм Дейкстры

def dijkstra_shortest_path(G, start_id, end_id):
    """
    Находит кратчайший путь между двумя городами, используя алгоритм Дейкстры.
    
    Args:
        G: граф NetworkX
        start_id: ID начального города
        end_id: ID конечного города
        
    Returns:
        tuple: (путь (список ID городов), общее расстояние)
    """
    # Используем встроенную реализацию NetworkX
    try:
        path = nx.dijkstra_path(G, start_id, end_id, weight='weight')
        total_weight = nx.dijkstra_path_length(G, start_id, end_id, weight='weight')
        return path, total_weight
    except nx.NetworkXNoPath:
        return None, None


def find_path_between_cities(G, city1_name, city2_name):
    """
    Находит кратчайший путь между двумя городами по их названиям.
    
    Args:
        G: граф NetworkX
        city1_name: название первого города (на английском)
        city2_name: название второго города (на английском)
    """
    # Находим ID городов
    start_id = None
    end_id = None
    
    for node, data in G.nodes(data=True):
        if data.get("name_en", "").lower() == city1_name.lower():
            start_id = node
        if data.get("name_en", "").lower() == city2_name.lower():
            end_id = node
    
    if start_id is None:
        print(f"Город '{city1_name}' не найден!")
        return
    if end_id is None:
        print(f"Город '{city2_name}' не найден!")
        return
    
    print(f"\n🔍 Поиск кратчайшего пути из '{G.nodes[start_id]['name']}' в '{G.nodes[end_id]['name']}'...")
    
    # Замеряем время
    import time
    start_time = time.time()
    path, total_weight = dijkstra_shortest_path(G, start_id, end_id)
    elapsed = time.time() - start_time
    
    if path is None:
        print(f"  Путь не найден!")
        return
    
    print(f"   Путь найден за {elapsed:.6f} сек")
    print(f"   Всего городов в пути: {len(path)}")
    print(f"   Общее расстояние: {total_weight:.0f} км")
    print(f"   Маршрут:")
    
    # Выводим путь с расстояниями между городами
    for i in range(len(path) - 1):
        from_city = G.nodes[path[i]]
        to_city = G.nodes[path[i + 1]]
        edge_data = G.get_edge_data(path[i], path[i + 1])
        weight = edge_data.get("weight", 0)
        airline = edge_data.get("airline", "Unknown")
        print(f"      {from_city['name']} → {to_city['name']} "
              f"({weight:.0f} км, {airline})")
    
    return path, total_weight


# 4. Демонстрация

def demo_shortest_paths(G):
    """
    Демонстрирует поиск кратчайших путей для нескольких пар городов.
    """
    print("\n" + "=" * 70)
    print("✈️ ПОИСК КРАТЧАЙШИХ ПУТЕЙ")
    print("=" * 70)
    
    # Примеры пар городов
    pairs = [
        ("Dubai", "Tokyo"),
        ("Dubai", "Singapore"),
        ("Dubai", "Moscow"),
        ("Moscow", "Beijing"),
        ("London", "Singapore"),
        ("Dubai", "London")
    ]
    
    for city1, city2 in pairs:
        find_path_between_cities(G, city1, city2)
        print("-" * 50)

def main():
    """Основная функция для демонстрации всех возможностей."""
    
    print("=" * 70)
    print("ВИЗУАЛИЗАЦИЯ ГРАФА И ПОИСК КРАТЧАЙШИХ ПУТЕЙ")
    print("=" * 70)
    
    # 1. Загрузка графа из MongoDB
    print("\n📂 Загрузка данных из MongoDB...")
    G = build_graph_from_mongodb()
    
    if G.number_of_nodes() == 0:
        print("Граф пуст! Запустите load_data.py для загрузки данных.")
        return
    
    # 2. Визуализация
    print("\n" + "=" * 70)
    print("📊 ВИЗУАЛИЗАЦИЯ ГРАФА")
    print("=" * 70)
    visualize_graph(G, title="Граф авиаперелётов (Азия)")
    
    # 3. Поиск кратчайших путей
    demo_shortest_paths(G)


if __name__ == "__main__":
    main()