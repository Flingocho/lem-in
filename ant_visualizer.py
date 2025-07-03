#!/usr/bin/env python3

import sys
import re
from typing import List, Tuple, Dict, Set, Optional
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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
    """Añade tooltip interactivo"""
    annot = ax.annotate('', xy=(0,0), xytext=(20,20), textcoords="offset points",
                       bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.9),
                       arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"),
                       fontsize=10, fontweight='bold')
    annot.set_visible(False)
    
    def update_annot(ind):
        pos = scatter.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        node = nodes[ind["ind"][0]]
        
        # Construir texto del tooltip con información del nodo
        tooltip_text = f"{node.name}\n({node.x}, {node.y})"
        if node.is_start:
            tooltip_text += "\n[INICIO]"
        elif node.is_end:
            tooltip_text += "\n[FINAL]"
        
        annot.set_text(tooltip_text)
    
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

def show_graph(num_ants: int, nodes: List[Node], connections: List[Connection], paths: List[Path] = None):
    """Muestra los nodos y conexiones en una ventana interactiva"""
    if not nodes:
        print("No hay nodos para mostrar")
        return
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Crear diccionario de nodos para búsqueda rápida
    node_dict = {node.name: node for node in nodes}
    
    # Crear conjunto de conexiones de caminos para resaltarlas
    path_connections = set()
    if paths:
        for path in paths:
            for i in range(len(path.nodes) - 1):
                # Agregar conexión en ambas direcciones
                path_connections.add((path.nodes[i], path.nodes[i + 1]))
                path_connections.add((path.nodes[i + 1], path.nodes[i]))
    
    # Dibujar conexiones normales primero
    for connection in connections:
        if connection.node1 in node_dict and connection.node2 in node_dict:
            node1 = node_dict[connection.node1]
            node2 = node_dict[connection.node2]
            
            # Verificar si esta conexión es parte de un camino
            if (connection.node1, connection.node2) in path_connections:
                continue  # La dibujaremos después como camino resaltado
            
            ax.plot([node1.x, node2.x], [node1.y, node2.y], 
                   'gray', linewidth=1, alpha=0.6, zorder=1)
    
    # Dibujar caminos resaltados
    if paths:
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'cyan']
        for i, path in enumerate(paths):
            color = colors[i % len(colors)]
            # Calcular grosor basado en el número de hormigas
            line_width = max(3, min(10, 2 + path.ant_count * 0.5))
            
            for j in range(len(path.nodes) - 1):
                node1_name = path.nodes[j]
                node2_name = path.nodes[j + 1]
                
                if node1_name in node_dict and node2_name in node_dict:
                    node1 = node_dict[node1_name]
                    node2 = node_dict[node2_name]
                    
                    ax.plot([node1.x, node2.x], [node1.y, node2.y], 
                           color=color, linewidth=line_width, alpha=0.8, zorder=3,
                           label=f'Camino {path.path_num} ({path.ant_count} hormigas)' if j == 0 else "")
    
    # Preparar datos para nodos
    x_coords = [node.x for node in nodes]
    y_coords = [node.y for node in nodes]
    colors = []
    
    # Asignar colores según tipo de nodo
    for node in nodes:
        if node.is_start:
            colors.append('green')
        elif node.is_end:
            colors.append('red')
        else:
            colors.append('blue')
    
    # Ajustar tamaño según cantidad de nodos
    if len(nodes) > 5000:
        point_size = 30
        alpha = 0.7
    elif len(nodes) > 1000:
        point_size = 60
        alpha = 0.8
    else:
        point_size = 120
        alpha = 0.9
    
    # Crear gráfico de nodos
    scatter = ax.scatter(x_coords, y_coords, s=point_size, c=colors, alpha=alpha, 
                        edgecolors='black', linewidth=1, zorder=4)
    
    # Añadir nombres de nodos como etiquetas
    for node in nodes:
        ax.annotate(node.name, (node.x, node.y), xytext=(5, 5), 
                   textcoords='offset points', fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))
    
    # Añadir interactividad
    _add_interactive_tooltip(fig, ax, scatter, nodes)
    
    # Configurar ejes y título
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    title = f'Lem-in Graph: {num_ants} hormigas, {len(nodes)} nodos, {len(connections)} conexiones'
    if paths:
        title += f', {len(paths)} camino(s) encontrado(s)'
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    # Añadir leyenda
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', 
                   markersize=10, label='Inicio', markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                   markersize=10, label='Final', markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', 
                   markersize=10, label='Nodo', markeredgecolor='black'),
        plt.Line2D([0], [0], color='gray', linewidth=2, label='Conexión')
    ]
    
    # Añadir caminos a la leyenda
    if paths:
        path_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'cyan']
        for i, path in enumerate(paths):
            color = path_colors[i % len(path_colors)]
            legend_elements.append(
                plt.Line2D([0], [0], color=color, linewidth=4, 
                          label=f'Camino {path.path_num} ({path.ant_count} hormigas)')
            )
    
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Ajustar límites
    if x_coords and y_coords:
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        margin_x = max(1, (max_x - min_x) * 0.1)
        margin_y = max(1, (max_y - min_y) * 0.1)
        
        ax.set_xlim(min_x - margin_x, max_x + margin_x)
        ax.set_ylim(min_y - margin_y, max_y + margin_y)
    
    # Habilitar navegación mejorada
    fig.canvas.toolbar_visible = True
    
    plt.tight_layout()
    plt.show()

def main():
    """Función principal"""
    num_ants, nodes, connections, paths, simulation_lines = parse_lem_in_with_simulation()
    
    if not nodes:
        print("No se encontraron nodos válidos en la entrada")
        return
    
    # Mostrar estadísticas
    print(f"=== Estadísticas del Grafo ===")
    print(f"Hormigas: {num_ants}")
    print(f"Nodos: {len(nodes)}")
    print(f"Conexiones: {len(connections)}")
    
    # Mostrar información de nodos especiales
    start_nodes = [n for n in nodes if n.is_start]
    end_nodes = [n for n in nodes if n.is_end]
    
    if start_nodes:
        print(f"Nodo de inicio: {start_nodes[0].name} ({start_nodes[0].x}, {start_nodes[0].y})")
    else:
        print("⚠️  No se encontró nodo de inicio")
        
    if end_nodes:
        print(f"Nodo final: {end_nodes[0].name} ({end_nodes[0].x}, {end_nodes[0].y})")
    else:
        print("⚠️  No se encontró nodo final")
    
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
        print(f"⚠️  Conexiones inválidas: {len(invalid_connections)}")
        if len(invalid_connections) <= 5:
            print(f"   {', '.join(invalid_connections)}")
        else:
            print(f"   {', '.join(invalid_connections[:5])}... (+{len(invalid_connections)-5} más)")
    
    # Mostrar información de caminos
    if paths:
        print(f"\n=== Caminos Encontrados ===")
        for path in paths:
            print(f"Camino {path.path_num}: {path.ant_count} hormigas")
            print(f"  Ruta: {' -> '.join(path.nodes)}")
            print(f"  Longitud: {len(path.nodes)} nodos")
    
    # Mostrar información de simulación
    if simulation_lines:
        print(f"\nSimulación: {len(simulation_lines)} pasos registrados")
    
    print(f"\n🚀 Abriendo visualización...")
    
    show_graph(num_ants, nodes, connections, paths)

if __name__ == "__main__":
    main()

