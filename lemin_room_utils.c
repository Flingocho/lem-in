/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lemin_rooms_utils.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jainavas <jainavas@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/10/21 19:42:03 by jainavas          #+#    #+#             */
/*   Updated: 2024/10/21 19:42:03 by jainavas         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "lemin.h"

t_room	*roomNew(char *name, int isStart, int roomNum)
{
	t_room	*new;
	new = ft_calloc(1, sizeof(t_room));
	new->current_ant = -1;
	new->room_name = name;
	new->room_id = roomNum;	new->conn_count = 0;
	new->conn_capacity = 2; // Capacidad inicial de 2 para tener espacio para el terminador NULL
	new->connections = ft_calloc(2, sizeof(t_room *));
	new->connections[0] = NULL;
	new->is_end = 0;
	new->is_start = 0;
	if (isStart == 1)
		new->is_start = 1;
	else if (isStart == 2)
		new->is_end = 1;
	return (new);
}

t_room **addRoomToArray(t_room *room, t_lemin *vars)
{
	if (vars->room_count >= vars->room_capacity - 1)
	{
		int old_capacity = vars->room_capacity;
		vars->room_capacity *= 2;
		vars->rooms = ft_realloc(vars->rooms, sizeof(t_room *) * old_capacity, sizeof(t_room *) * vars->room_capacity);
	}
	vars->rooms[vars->room_count] = room;
	vars->room_count++;
	vars->rooms[vars->room_count] = NULL;
	return (vars->rooms);
}

t_room	*findRoomName(t_lemin *vars, char *name)
{
	for (int i = 0; i < vars->room_count; i++)
    {
		if (ft_strlen(vars->rooms[i]->room_name) > ft_strlen(name))
		{
			if (ft_strncmp(vars->rooms[i]->room_name, name, ft_strlen(vars->rooms[i]->room_name)) == 0)
            	return (vars->rooms[i]);
		}
		else
		{
			if (ft_strncmp(vars->rooms[i]->room_name, name, ft_strlen(name)) == 0)
            	return (vars->rooms[i]);
		}
    }
    return (NULL);
}

t_room	*findRoomCoord(t_lemin *vars, int x, int y)
{
	for (int i = 0; i < vars->room_count; i++)
    {
        if (vars->rooms[i]->x == x && vars->rooms[i]->y == y)
            return (vars->rooms[i]);
    }
    return (NULL);
}

t_room	*findRoomById(t_lemin *vars, int id)
{
	for (int i = 0; i < vars->room_count; i++)
    {
        if (vars->rooms[i]->room_id == id)
            return (vars->rooms[i]);
    }
    return (NULL);
}

void	roomsClear(t_lemin *vars)
{
	for (int i = 0; i < vars->room_count; i++)
    {
        if (vars->rooms[i])
		{
			free(vars->rooms[i]->room_name);
			free(vars->rooms[i]->connections);
            free(vars->rooms[i]);
		}
    }
	free(vars->rooms);
}

void roomAddConn(t_room *room, t_room *new_connection)
{
	for (int i = 0; i < room->conn_count; i++)
	{
		if (room->connections[i] == new_connection)
			return;
	}
    if (room->conn_count >= room->conn_capacity - 1) // Dejar espacio para NULL
    {
        room->conn_capacity *= 2;
        room->connections = ft_realloc(room->connections, room->conn_capacity/2 * sizeof(t_room*), room->conn_capacity * sizeof(t_room*));
    }
    room->connections[room->conn_count++] = new_connection;
    room->connections[room->conn_count] = NULL; // Mantener terminador NULL
    
	if (new_connection->conn_count >= new_connection->conn_capacity - 1) // Dejar espacio para NULL
	{
		new_connection->conn_capacity *= 2;
        new_connection->connections = ft_realloc(new_connection->connections, new_connection->conn_capacity/2 * sizeof(t_room*), new_connection->conn_capacity * sizeof(t_room*));
	}
	new_connection->connections[new_connection->conn_count++] = room;
    new_connection->connections[new_connection->conn_count] = NULL; // Mantener terminador NULL
}
