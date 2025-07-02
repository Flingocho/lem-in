/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lemin.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jainavas <jainavas@student.42.fr>          +#+  +:+       +#+           */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/10/17 17:06:21 by jainavas          #+#    #+#             */
/*   Updated: 2025/05/11 21:07:55 by jainavas         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "lemin.h"

char **extractData()
{
	char **res;
	char *line;
	int i;
	int capacity;

	i = 0;
	capacity = 2;
	res = ft_calloc(capacity, sizeof(char *));
	line = get_next_line(0);
	while (line)
	{
		if (i >= capacity - 1)
		{
			capacity *= 2;
			res = ft_realloc(res, (capacity / 2) * sizeof(char *), capacity * sizeof(char *));
		}
		res[i++] = ft_strtrim(line, "\n");
		free(line);
		line = get_next_line(0);
	}
	res[i] = NULL;
	return (res);
}

int is_valid_room_line(char *line)
{
	char **parts;
	int count;

	if (!line || line[0] == '#' || line[0] == 'L' || line[0] == '\0')
		return (0);
	parts = ft_split(line, ' ');
	count = 0;
	while (parts[count])
		count++;
	if (count == 3)
	{
		freedoublepointer(parts);
		return (1);
	}
	freedoublepointer(parts);
	return (0);
}

t_room *parse_room_from_line(char *line, int room_id)
{
	char **parts = ft_split(line, ' ');
	t_room *room;

	room = ft_calloc(1, sizeof(t_room));
	room->room_name = ft_strdup(parts[0]);
	room->room_id = room_id;
	room->conn_capacity = 4;
	room->connections = ft_calloc(room->conn_capacity, sizeof(t_room *));
	room->current_ant = -1;
	room->is_start = 0;
	room->is_end = 0;
	freedoublepointer(parts);
	return (room);
}

int makeRoomsArray(char **input, t_lemin *vars)
{
	int i = 0;
	t_room *tmp;
	int next_is_start = 0;
	int next_is_end = 0;

	if (input[0])
		vars->ant_count = ft_atoi(input[0]);
	i = 1;
	while (input[i] && !ft_strchr(input[i], '-'))
	{
		if (ft_strncmp("##start", input[i], 7) == 0)
		{
			if (vars->start_room)
				return (ft_printf("Error: Too many ##start\n"), -1);
			next_is_start = 1;
		}
		else if (ft_strncmp("##end", input[i], 5) == 0)
		{
			if (vars->end_room)
				return (ft_printf("Error: Too many ##end\n"), -1);
			next_is_end = 1;
		}
		else if (input[i][0] == '#')
		{
		}
		else if (is_valid_room_line(input[i]))
		{
			tmp = parse_room_from_line(input[i], vars->room_count);
			if (next_is_start)
			{
				tmp->is_start = 1;
				vars->start_room = tmp;
				next_is_start = 0;
			}
			if (next_is_end)
			{
				tmp->is_end = 1;
				vars->end_room = tmp;
				next_is_end = 0;
			}
			vars->rooms = addRoomToArray(tmp, vars);
		}
		else
			return (ft_printf("Error: Invalid line\n"), -1);
		i++;
	}
	if (!vars->start_room || !vars->end_room)
		return (ft_printf("Error: Lack of start or end\n"), -1);
	return (makeRoomsConns(input, i, vars));
}

int makeRoomsConns(char **input, int i, t_lemin *vars)
{
	char **line;

	while (input[i])
	{
		if (input[i][0] == '#')
		{
			i++;
			continue;
		}
		line = ft_split(input[i], '-');
		
		if (ft_dplen(line) != 2)
		{
			return (freedoublepointer(line), ft_printf("Error: Connection structure 1: line:%d, dplen:%i\n", i, ft_dplen(line)), -1);
		}
		
		if (!findRoomName(vars, line[0]))
		{
			return (freedoublepointer(line), ft_printf("Error: Connection structure 2: line:%d\n", i), -1);
		}
		
		if (!findRoomName(vars, line[1]))
		{
			return (freedoublepointer(line), ft_printf("Error: Connection structure 3: line:%d\n", i), -1);
		}
		
		roomAddConn(findRoomName(vars, line[0]), findRoomName(vars, line[1]));
		freedoublepointer(line);
		i++;
	}
	return 0;
}

int getRoomInfo(t_lemin *vars)
{
	char **input = extractData();
	int i = -1;
	
	// Imprimir el input original primero
	while (input[++i])
		printf("%s\n", input[i]);
	
	// Resetear el índice y procesar el input
	vars->room_count = 0;
	if(makeRoomsArray(input, vars) == -1) // <-----------ESTO NO FUNCIONA COMO DEBERIA
		exit(1);
	// while (count < vars->room_count)
	// {
	// 	printf("name: %s number: %d   start: %d end: %d   connections:\n", vars->rooms[count]->room_name, vars->rooms[count]->room_id, vars->rooms[count]->is_start, vars->rooms[count]->is_end);
	// 	if (*vars->rooms[count]->connections)
	// 	{
	// 		int j = 0;
	// 		while (vars->rooms[count]->connections[j])
	// 		{
	// 			printf("	to: %s\n", vars->rooms[count]->connections[j]->room_name);
	// 			j++;
	// 		}
	// 	}
	// 	count++;
	// }
	// printf("\n");
	t_path **res = findAllPaths(vars);
	distributeAnts(res, vars);
	if (!res)
		printf("Camino no encontrado\n");
	else
	{
		for (int j = 0; j < vars->path_count; j++)
		{
			if (!res[j])
				break;
			printf("path num: %d	ants assigned: %d	start: %s ", j, res[j]->ants_assigned, findRoomById(vars, res[j]->room_ids[0])->room_name);
			for (int i = 1; i < res[j]->length; i++)
			{
				printf("->");
				printf(" %s ", findRoomById(vars, res[j]->room_ids[i])->room_name);
			}
			printf("\n");
		}
		printf("\n=== SIMULATION ===\n");
		simulateAntMovement(res, vars);
		
		for (int i = 0; i < vars->path_count; i++)
		{
			free(res[i]->room_ids);
			free(res[i]);
		}
		free(res);
	}
	freedoublepointer(input);
	return 0;
}

int main()
{
	t_lemin *vars;

	vars = ft_calloc(1, sizeof(t_lemin));
	vars->room_capacity = 2;
	vars->rooms = ft_calloc(vars->room_capacity, sizeof(t_room *));
	getRoomInfo(vars);
	roomsClear(vars);
	free(vars);
	return (0);
}
