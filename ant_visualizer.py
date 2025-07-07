#!/usr/bin/env python3

import sys
import re
from typing import List, Tuple, Dict, Set, Optional
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patches as mpatches

class Node:
    """Representa un nodo con nombre y coordenadas"""
    def __init__(self, name: str, x: int, y: int, is_start: bool = False, is_end: bool = False):
        self.name = name
        self.x = x
        self.y = y
        self.is_start = is_start
        self.is_end = is_end

class Connection:
    """Representa una conexión entre dos nodos"""
    def __init__(self, node1: str, node2: str):
        self.node1 = node1
        self.node2 = node2

class Path:
    """Representa un camino encontrado por el algoritmo"""
    def __init__(self, path_num: int, ant_count: int, nodes: List[str]):
        self.path_num = path_num
        self.ant_count = ant_count
        self.nodes = nodes

def parse_node_line(line: str) -> Node:
    """Parsea una línea con formato: nombre coordx coordy"""
    pattern = r'^([a-zA-Z0-9_]+)\s+(-?\d+)\s+(-?\d+)$'
    match = re.match(pattern, line.strip())
    
    if not match:
        raise ValueError(f"Formato inválido")
    
    name = match.group(1)
    x = int(match.group(2))
    y = int(match.group(3))
    
    return Node(name, x, y)

def parse_connection_line(line: str) -> Connection:
    """Parsea una línea con formato: nodo1-nodo2"""
    pattern = r'^([a-zA-Z0-9_]+)-([a-zA-Z0-9_]+)$'
    match = re.match(pattern, line.strip())
    
    if not match:
        raise ValueError(f"Formato de conexión inválido")
    
    return Connection(match.group(1), match.group(2))

def parse_path_line(line: str) -> Optional[Path]:
    """Parsea una línea de camino: path num: 0     ants assigned: 15       start: center -> n3 -> e1 -> e2 -> exit"""
    pattern = r'path num:\s*(\d+)\s+ants assigned:\s*(\d+)\s+start:\s*(.+)'
    match = re.match(pattern, line.strip())
    
    if not match:
        return None
    
    path_num = int(match.group(1))
    ant_count = int(match.group(2))
    path_str = match.group(3)
    
    # Parsear la secuencia de nodos: "center -> n3 -> e1 -> e2 -> exit"
    nodes = [node.strip() for node in path_str.split('->')]
    
    return Path(path_num, ant_count, nodes)

def parse_lem_in_with_simulation() -> Tuple[int, List[Node], List[Connection], List[Path], List[str]]:
    """Parsea el formato completo de lem-in con datos de simulación desde stdin"""
    lines = []
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if line:
                lines.append(line)
    except KeyboardInterrupt:
        sys.exit(1)
    
    if not lines:
        return 0, [], [], [], []
    
    # Primera línea: número de hormigas
    try:
        num_ants = int(lines[0])
    except (ValueError, IndexError):
        num_ants = 0
    
    nodes = []
    connections = []
    paths = []
    simulation_lines = []
    current_line = 1
    next_is_start = False
    next_is_end = False
    parsing_simulation = False
    
    # Parsear nodos
    while current_line < len(lines):
        line = lines[current_line]
        
        # Detectar inicio de simulación
        if line == "=== SIMULATION ===":
            parsing_simulation = True
            current_line += 1
            continue
        
        if parsing_simulation:
            # Capturar líneas de simulación
            if line.startswith('L') and '->' in line:
                simulation_lines.append(line)
            current_line += 1
            continue
        
        # Detectar líneas de caminos
        path = parse_path_line(line)
        if path:
            paths.append(path)
            current_line += 1
            continue
        
        # Saltar comentarios que no son marcadores especiales
        if line.startswith('#') and line not in ["##start", "##end"]:
            current_line += 1
            continue
        
        # Verificar marcadores especiales
        if line == "##start":
            next_is_start = True
            current_line += 1
            continue
        elif line == "##end":
            next_is_end = True
            current_line += 1
            continue
        
        # Intentar parsear como nodo
        try:
            node = parse_node_line(line)
            node.is_start = next_is_start
            node.is_end = next_is_end
            nodes.append(node)
            next_is_start = False
            next_is_end = False
            current_line += 1
        except ValueError:
            # Si no es un nodo, puede ser una conexión
            break
    
    # Parsear conexiones (si no estamos en simulación)
    while current_line < len(lines) and not parsing_simulation:
        line = lines[current_line]
        
        # Detectar líneas de caminos
        path = parse_path_line(line)
        if path:
            paths.append(path)
            current_line += 1
            continue
        
        # Detectar inicio de simulación
        if line == "=== SIMULATION ===":
            parsing_simulation = True
            current_line += 1
            continue
        
        # Saltar comentarios
        if line.startswith('#'):
            current_line += 1
            continue
            
        try:
            connection = parse_connection_line(line)
            connections.append(connection)
        except ValueError:
            pass  # Ignorar líneas que no son conexiones válidas
        current_line += 1
    
    # Capturar líneas de simulación restantes
    while current_line < len(lines):
        line = lines[current_line]
        if line.startswith('L') and '->' in line:
            simulation_lines.append(line)
        current_line += 1
    
    return num_ants, nodes, connections, paths, simulation_lines

def _add_interactive_tooltip(fig, ax, scatter, nodes: List[Node]):
    """Añade tooltip interactivo con estilo mejorado"""
    annot = ax.annotate('', xy=(0,0), xytext=(20,20), textcoords="offset points",
                       bbox=dict(boxstyle="round,pad=0.8", facecolor='#2D2D2D', 
                               edgecolor='#00FF88', linewidth=2, alpha=0.95),
                       arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3",
                                     color='#00FF88', linewidth=2),
                       fontsize=12, fontweight='bold', color='white',
                       zorder=1000)  # Asegurar que esté por encima de todo
    annot.set_visible(False)
    
    def update_annot(ind):
        pos = scatter.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        node = nodes[ind["ind"][0]]
        
        # Construir texto del tooltip con información del nodo
        tooltip_text = f"NODE: {node.name}\nPOS: ({node.x}, {node.y})"
        if node.is_start:
            tooltip_text += "\n[START]"
        elif node.is_end:
            tooltip_text += "\n[END]"
        
        annot.set_text(tooltip_text)
        # Ajustar posición para evitar que se salga de la pantalla
        if pos[0] > ax.get_xlim()[1] * 0.8:  # Si está muy a la derecha
            annot.set_position((-40, 20))  # Mover tooltip a la izquierda
        else:
            annot.set_position((20, 20))  # Posición normal
    
    def hover(event):
        if event.inaxes == ax:
            cont, ind = scatter.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw()
            else:
                if annot.get_visible():
                    annot.set_visible(False)
                    fig.canvas.draw()
    
    fig.canvas.mpl_connect("motion_notify_event", hover)

def _apply_dark_theme(fig, ax):
    """Aplica tema oscuro elegante"""
    # Configurar colores de fondo
    fig.patch.set_facecolor('#0F0F0F')
    ax.set_facecolor('#1A1A1A')
    
    # Configurar grid con estilo futurista
    ax.grid(True, alpha=0.3, color='#333333', linewidth=0.8, linestyle='--')
    
    # Configurar ejes
    ax.spines['bottom'].set_color('#555555')
    ax.spines['top'].set_color('#555555')
    ax.spines['right'].set_color('#555555')
    ax.spines['left'].set_color('#555555')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    
    # Configurar etiquetas de ejes
    ax.tick_params(axis='x', colors='#CCCCCC', labelsize=10)
    ax.tick_params(axis='y', colors='#CCCCCC', labelsize=10)
    ax.xaxis.label.set_color('#CCCCCC')
    ax.yaxis.label.set_color('#CCCCCC')
    ax.xaxis.label.set_fontsize(12)
    ax.yaxis.label.set_fontsize(12)
    ax.xaxis.label.set_fontweight('bold')
    ax.yaxis.label.set_fontweight('bold')

def _add_glow_effect(ax, x, y, color, size=50):
    """Añade efecto de resplandor a los nodos importantes"""
    # Crear círculos concéntricos para el efecto de resplandor
    for i in range(3):
        alpha = 0.1 - i * 0.03
        radius = size * (1 + i * 0.3)
        circle = Circle((x, y), radius, facecolor=color, alpha=alpha, 
                       edgecolor='none', zorder=1)
        ax.add_patch(circle)

def show_graph(num_ants: int, nodes: List[Node], connections: List[Connection], paths: List[Path] = None):
    """Muestra los nodos y conexiones en una ventana interactiva con estilo mejorado"""
    if not nodes:
        print("No hay nodos para mostrar")
        return
    
    # Crear figura con estilo moderno
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Aplicar tema oscuro
    _apply_dark_theme(fig, ax)
    
    # Crear diccionario de nodos para búsqueda rápida
    node_dict = {node.name: node for node in nodes}
    
    # Crear conjunto de conexiones de caminos para resaltarlas
    path_connections = set()
    if paths:
        for path in paths:
            for i in range(len(path.nodes) - 1):
                path_connections.add((path.nodes[i], path.nodes[i + 1]))
                path_connections.add((path.nodes[i + 1], path.nodes[i]))
    
    # Paleta de colores moderna para caminos
    path_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                   '#F06292', '#AED581', '#FFB74D', '#BA68C8', '#81C784']
    
    # Dibujar conexiones normales con efecto de profundidad
    for connection in connections:
        if connection.node1 in node_dict and connection.node2 in node_dict:
            node1 = node_dict[connection.node1]
            node2 = node_dict[connection.node2]
            
            # Verificar si esta conexión es parte de un camino
            if (connection.node1, connection.node2) in path_connections:
                continue
            
            # Línea principal
            ax.plot([node1.x, node2.x], [node1.y, node2.y], 
                   color='#444444', linewidth=1.5, alpha=0.7, zorder=2)
            
            # Línea de brillo sutil
            ax.plot([node1.x, node2.x], [node1.y, node2.y], 
                   color='#666666', linewidth=0.5, alpha=0.5, zorder=2)
    
    # Dibujar caminos resaltados con efectos especiales
    if paths:
        for i, path in enumerate(paths):
            color = path_colors[i % len(path_colors)]
            # Calcular grosor basado en el número de hormigas
            base_width = max(4, min(12, 3 + path.ant_count * 0.6))
            
            for j in range(len(path.nodes) - 1):
                node1_name = path.nodes[j]
                node2_name = path.nodes[j + 1]
                
                if node1_name in node_dict and node2_name in node_dict:
                    node1 = node_dict[node1_name]
                    node2 = node_dict[node2_name]
                    
                    # Línea de fondo (más gruesa, más oscura)
                    ax.plot([node1.x, node2.x], [node1.y, node2.y], 
                           color=color, linewidth=base_width + 2, alpha=0.4, zorder=3)
                    
                    # Línea principal
                    ax.plot([node1.x, node2.x], [node1.y, node2.y], 
                           color=color, linewidth=base_width, alpha=0.9, zorder=4,
                           label=f'Path {path.path_num} ({path.ant_count} ants)' if j == 0 else "")
                    
                    # Línea de brillo
                    ax.plot([node1.x, node2.x], [node1.y, node2.y], 
                           color='white', linewidth=base_width * 0.3, alpha=0.6, zorder=5)
    
    # Preparar datos para nodos con colores mejorados
    x_coords = [node.x for node in nodes]
    y_coords = [node.y for node in nodes]
    
    # Encontrar nodos especiales para efectos
    start_nodes = [node for node in nodes if node.is_start]
    end_nodes = [node for node in nodes if node.is_end]
    
    # Añadir efectos de resplandor a nodos especiales
    for node in start_nodes:
        _add_glow_effect(ax, node.x, node.y, '#00FF88', 15)
    
    for node in end_nodes:
        _add_glow_effect(ax, node.x, node.y, '#FF4444', 15)
    
    # Configurar tamaños y colores de nodos
    node_sizes = []
    node_colors = []
    edge_colors = []
    
    for node in nodes:
        if node.is_start:
            node_sizes.append(300)
            node_colors.append('#00FF88')
            edge_colors.append('#00CC66')
        elif node.is_end:
            node_sizes.append(300)
            node_colors.append('#FF4444')
            edge_colors.append('#CC2222')
        else:
            node_sizes.append(150)
            node_colors.append('#4A9EFF')
            edge_colors.append('#3A7ECC')
    
    # Crear gráfico de nodos con efectos mejorados
    scatter = ax.scatter(x_coords, y_coords, s=node_sizes, c=node_colors, 
                        alpha=0.9, edgecolors=edge_colors, linewidth=2.5, 
                        zorder=6, marker='o')
    
    # Añadir segundo anillo para nodos especiales
    for i, node in enumerate(nodes):
        if node.is_start or node.is_end:
            ax.scatter(node.x, node.y, s=node_sizes[i] * 1.3, 
                      c='none', edgecolors=node_colors[i], linewidth=1, 
                      alpha=0.6, zorder=5)
    
    # Añadir nombres de nodos con estilo mejorado
    for node in nodes:
        # Fondo para el texto
        bbox_props = dict(boxstyle='round,pad=0.3', facecolor='#2D2D2D', 
                         alpha=0.8, edgecolor='#555555', linewidth=1)
        
        if node.is_start:
            text_color = '#00FF88'
            bbox_props['edgecolor'] = '#00FF88'
        elif node.is_end:
            text_color = '#FF4444'
            bbox_props['edgecolor'] = '#FF4444'
        else:
            text_color = '#CCCCCC'
        
        ax.annotate(node.name, (node.x, node.y), xytext=(8, 8), 
                   textcoords='offset points', fontsize=9, fontweight='bold',
                   color=text_color, bbox=bbox_props, zorder=7)
    
    # Añadir interactividad
    _add_interactive_tooltip(fig, ax, scatter, nodes)
    
    # Configurar título con estilo futurista
    title = f'Lem-in Graph Visualizer\n{num_ants} ants • {len(nodes)} nodes • {len(connections)} connections'
    if paths:
        title += f' • {len(paths)} path(s) found'
    
    ax.set_title(title, fontsize=16, fontweight='bold', color='#FFFFFF', 
                pad=20, bbox=dict(boxstyle='round,pad=1', facecolor='#333333', 
                                alpha=0.8, edgecolor='#00FF88', linewidth=2))
    
    # Etiquetas de ejes con estilo
    ax.set_xlabel('X Coordinate', fontsize=12, fontweight='bold', color='#CCCCCC')
    ax.set_ylabel('Y Coordinate', fontsize=12, fontweight='bold', color='#CCCCCC')
    
    # Crear leyenda con estilo mejorado
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#00FF88', 
                   markersize=12, label='START', markeredgecolor='#00CC66', 
                   markeredgewidth=2),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF4444', 
                   markersize=12, label='END', markeredgecolor='#CC2222',
                   markeredgewidth=2),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4A9EFF', 
                   markersize=10, label='NODE', markeredgecolor='#3A7ECC',
                   markeredgewidth=2),
        plt.Line2D([0], [0], color='#666666', linewidth=3, label='CONNECTION')
    ]
    
    # Añadir caminos a la leyenda
    if paths:
        for i, path in enumerate(paths):
            color = path_colors[i % len(path_colors)]
            legend_elements.append(
                plt.Line2D([0], [0], color=color, linewidth=4, 
                          label=f'Path {path.path_num} ({path.ant_count} ants)')
            )
    
    # Configurar leyenda con estilo oscuro
    legend = ax.legend(handles=legend_elements, loc='upper right', 
                      frameon=True, fancybox=True, shadow=True,
                      facecolor='#2D2D2D', edgecolor='#555555', 
                      fontsize=10, labelcolor='#CCCCCC')
    legend.get_frame().set_alpha(0.9)
    legend.get_frame().set_linewidth(2)
    
    # Ajustar límites con márgenes elegantes
    if x_coords and y_coords:
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        margin_x = max(5, (max_x - min_x) * 0.15)
        margin_y = max(5, (max_y - min_y) * 0.15)
        
        ax.set_xlim(min_x - margin_x, max_x + margin_x)
        ax.set_ylim(min_y - margin_y, max_y + margin_y)
    
    # Configurar ventana
    fig.canvas.toolbar_visible = True
    fig.canvas.manager.set_window_title('Lem-in Graph Visualizer - Dark Theme')
    
    plt.tight_layout()
    plt.show()

def main():
    """Función principal con mensajes mejorados"""
    print(">> Iniciando Lem-in Graph Visualizer...")
    print(">> Procesando datos de entrada...")
    
    num_ants, nodes, connections, paths, simulation_lines = parse_lem_in_with_simulation()
    
    if not nodes:
        print("ERROR: No se encontraron nodos válidos en la entrada")
        return
    
    # Mostrar estadísticas con estilo
    print(f"\n=== ESTADISTICAS DEL GRAFO ===")
    print(f"Hormigas: {num_ants}")
    print(f"Nodos: {len(nodes)}")
    print(f"Conexiones: {len(connections)}")
    
    # Mostrar información de nodos especiales
    start_nodes = [n for n in nodes if n.is_start]
    end_nodes = [n for n in nodes if n.is_end]
    
    if start_nodes:
        print(f"Nodo de inicio: {start_nodes[0].name} ({start_nodes[0].x}, {start_nodes[0].y})")
    else:
        print("WARNING: No se encontró nodo de inicio")
        
    if end_nodes:
        print(f"Nodo final: {end_nodes[0].name} ({end_nodes[0].x}, {end_nodes[0].y})")
    else:
        print("WARNING: No se encontró nodo final")
    
    # Validar conexiones
    node_names = {node.name for node in nodes}
    valid_connections = 0
    invalid_connections = []
    
    for conn in connections:
        if conn.node1 in node_names and conn.node2 in node_names:
            valid_connections += 1
        else:
            invalid_connections.append(f"{conn.node1}-{conn.node2}")
    
    print(f"Conexiones válidas: {valid_connections}")
    if invalid_connections:
        print(f"WARNING: Conexiones inválidas: {len(invalid_connections)}")
        if len(invalid_connections) <= 5:
            print(f"   {', '.join(invalid_connections)}")
        else:
            print(f"   {', '.join(invalid_connections[:5])}... (+{len(invalid_connections)-5} más)")
    
    # Mostrar información de caminos
    if paths:
        print(f"\n=== CAMINOS ENCONTRADOS ===")
        for path in paths:
            print(f"Camino {path.path_num}: {path.ant_count} hormigas")
            print(f"   Ruta: {' -> '.join(path.nodes)}")
            print(f"   Longitud: {len(path.nodes)} nodos")
    
    # Mostrar información de simulación
    if simulation_lines:
        print(f"\nSimulación: {len(simulation_lines)} pasos registrados")
    
    print(f"\n>> Abriendo visualización con tema oscuro...")
    
    show_graph(num_ants, nodes, connections, paths)

if __name__ == "__main__":
    main()

