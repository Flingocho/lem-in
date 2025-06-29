/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lemin_algorithm.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jainavas <jainavas@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/06/29 22:09:06 by jainavas          #+#    #+#             */
/*   Updated: 2025/06/29 23:56:55 by jainavas         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "lemin.h"

t_path *findPath(t_lemin *vars, int *permanent_visited)
{
	int *queue = ft_calloc(vars->room_count, sizeof(int));
	int *visited = ft_calloc(vars->room_count, sizeof(int));
	int *parent = ft_calloc(vars->room_count, sizeof(int));
	int front = 0, rear = 0;

	for (int i = 0; i < vars->room_count; i++)
		visited[i] = permanent_visited[i];

	queue[rear++] = vars->start_room->room_id;
	visited[vars->start_room->room_id] = 1;
	parent[vars->start_room->room_id] = -1;

	while (front < rear)
	{
		int current_id = queue[front++];
		t_room *current = vars->rooms[current_id];

		if (current->is_end)
		{
			int length = 0;
			int temp_id = current_id;
			while (temp_id != -1)
			{
				length++;
				temp_id = parent[temp_id];
			}

			t_path *result = ft_calloc(1, sizeof(t_path));
			result->length = length;
			result->room_ids = malloc(length * sizeof(int));

			temp_id = current_id;
			for (int i = length - 1; i >= 0; i--)
			{
				result->room_ids[i] = temp_id;
				temp_id = parent[temp_id];
			}

			free(queue);
			free(visited);
			free(parent);
			return (result);
		}
		for (int i = 0; i < current->conn_count; i++)
		{
			int neighbor_id = current->connections[i]->room_id;
			if (!visited[neighbor_id])
			{
				visited[neighbor_id] = 1;
				parent[neighbor_id] = current_id;
				queue[rear++] = neighbor_id;
			}
		}
	}
	free(queue);
	free(visited);
	free(parent);
	return (NULL);
}

void markUsedPath(t_path *path, int *permanent_visited)
{
    for (int i = 1; i < path->length - 1; i++)
    {
        int room_id = path->room_ids[i];
        permanent_visited[room_id] = 1;
    }
}

int calculate_finish_time(t_path *path)
{
    return (path->length - 1) + path->ants_assigned;
}

t_path **findAllPaths(t_lemin *vars)
{
	t_path	**res = NULL;
	int	i = 0;
	int	*perm_visited = ft_calloc(vars->room_count, sizeof(int));

	while (1)
	{
		t_path *path = findPath(vars, perm_visited);
		if (!path)
			break;
		res = ft_realloc(res, i * sizeof(t_path *), (i + 1) * sizeof(t_path *));
		res[i] = path;
		i++;
		markUsedPath(path, perm_visited);
	}
	free(perm_visited);
	vars->path_count = i;
	return (res);
}

int		bestPathIndx(t_path **paths, int path_count)
{
	int best_path = 0;
	int min_time = calculate_finish_time(paths[0]);
	
	for (int i = 1; i < path_count; i++)
	{
		int finishTime = calculate_finish_time(paths[i]);
		if (finishTime < min_time)
		{
			best_path = i;
			min_time = finishTime;
		}
	}
	return best_path;
}

void	distributeAnts(t_path **paths, t_lemin *vars)
{
	for (int i = 0; i < vars->path_count; i++)
		paths[i]->ants_assigned = 0;
	for (int i = 0; i < vars->ant_count; i++)
		paths[bestPathIndx(paths, vars->path_count)]->ants_assigned++;
}
