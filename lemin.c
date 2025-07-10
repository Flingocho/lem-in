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
	char **temp;

	i = 0;
	capacity = 2;
	res = ft_calloc(capacity, sizeof(char *));
	if (!res)
		return NULL;
	line = get_next_line(0);
	while (line)
	{
		if (i >= capacity - 1)
		{
			capacity *= 2;
			temp = ft_realloc(res, (capacity / 2) * sizeof(char *), capacity * sizeof(char *));
			if (!temp)
				return NULL;
			res = temp;
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
	if (!parts)
		return 0;
	count = 0;
	while (parts[count])
		count++;
	if (count == 3)
	{
		if (checkoverflow(parts[1]) == -1 || checkoverflow(parts[2]) == -1)
			return (freedoublepointer(parts), 0);
		freedoublepointer(parts);
		return (1);
	}
	freedoublepointer(parts);
	return (0);
}

t_room *parse_room_from_line(char *line, int room_id, t_lemin *vars)
{
	char **parts = ft_split(line, ' ');
	if (!parts)
		return NULL;
	t_room *room;

	if (findRoomName(vars, parts[0]) || findRoomCoord(vars, ft_atoi(parts[1]), ft_atoi(parts[2])))
		return NULL;
	room = ft_calloc(1, sizeof(t_room));
	if (!room)
		return NULL;
	room->room_name = ft_strdup(parts[0]);
	room->room_id = room_id;
	room->conn_capacity = 4;
	room->connections = ft_calloc(room->conn_capacity, sizeof(t_room *));
	room->current_ant = -1;
	room->is_start = 0;
	room->is_end = 0;
	room->x = ft_atoi(parts[1]);
	room->y = ft_atoi(parts[2]);
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
	{
		char **spl = ft_split(input[0], ' ');
		if (!spl)
			return (ft_printf("Error: Number of ants\n"), -1);
		if (!spl[0] || ft_dplen(spl) != 1 || checkoverflow(spl[0]) == -1)
			return (freedoublepointer(spl), ft_printf("Error: Number of ants\n"), -1);
		vars->ant_count = ft_atoi(spl[0]);
		freedoublepointer(spl);
	}
	if (vars->ant_count < 1)
		return (ft_printf("Error: Number of ants\n"), -1);
	i = 1;
	while (input[i] && ft_strcount(input[i], '-') != 1)
	{
		if (ft_strncmp("##start", input[i], 8) == 0)
		{
			if (vars->start_room)
				return (ft_printf("Error: Too many ##start\n"), -1);
			next_is_start = 1;
		}
		else if (ft_strncmp("##end", input[i], 6) == 0)
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
			tmp = parse_room_from_line(input[i], vars->room_count, vars);
			if (!tmp)
				return (ft_printf("Error: Invalid line %d\n", i + 1), -1);
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
	char	**line;
	t_room	*a;
	t_room	*b;

	while (input[i])
	{
		if (input[i][0] == '#')
		{
			i++;
			continue;
		}
		line = ft_split(input[i], '-');
		
		if (ft_dplen(line) != 2 || ft_strcount(input[i], '-') != 1)
		{
			return (freedoublepointer(line), ft_printf("Error: Connection structure 1: line:%d\n", i), -1);
		}
		a = findRoomName(vars, line[0]);
		b = findRoomName(vars, line[1]);
		if (!a)
			return (freedoublepointer(line), ft_printf("Error: Connection structure 2: line:%d\n", i), -1);
		
		if (!b)
			return (freedoublepointer(line), ft_printf("Error: Connection structure 3: line:%d\n", i), -1);
		
		if (a == b)
			return (freedoublepointer(line), ft_printf("Error: Connection structure 4: line:%d\n", i), -1);
		
		roomAddConn(a, b);
		freedoublepointer(line);
		i++;
	}
	return 0;
}

int getRoomInfo(t_lemin *vars)
{
	char **input = extractData();
	int i = -1;
	
	if (!input)
		exit(1);
	// Imprimir el input original primero
	while (input[++i])
		ft_printf("%s\n", input[i]);
	
	// Resetear el índice y procesar el input
	vars->room_count = 0;
	if(makeRoomsArray(input, vars) == -1)
		exit(1);
	t_path **res = findAllPaths(vars);
	if (!res)
		ft_printf("Camino no encontrado\n");
	else
	{
		distributeAnts(res, vars);
		for (int j = 0; j < vars->path_count; j++)
		{
			if (!res[j])
				break;
			ft_printf("path num: %d	ants assigned: %d	start: %s ", j, res[j]->ants_assigned, findRoomById(vars, res[j]->room_ids[0])->room_name);
			for (int i = 1; i < res[j]->length; i++)
			{
				ft_printf("->");
				ft_printf(" %s ", findRoomById(vars, res[j]->room_ids[i])->room_name);
			}
			ft_printf("\n");
		}
		ft_printf("\n=== SIMULATION ===\n");
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
