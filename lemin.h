/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lem-in.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jainavas <jainavas@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/10/17 17:06:47 by jainavas          #+#    #+#             */
/*   Updated: 2025/01/24 17:40:09 by jainavas         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef LEMIN_H
# define LEMIN_H

# include <unistd.h>
# include <sys/types.h>
# include <sys/wait.h>
# include <stdio.h>
# include <fcntl.h>
# include <stdlib.h>
# include <string.h>
# include <errno.h>
# include "libft_ext/libft.h"
# include "libft_ext/ft_printf.h"

typedef struct s_path
{
    int *room_ids;      // [start_id, room1_id, room2_id, end_id]
    int length;         // Longitud
    int ants_assigned;  // Cuántas hormigas van por este camino
}	t_path;

typedef struct room
{
	int				room_id;        // Mejor que roomNumber
	char			*room_name;     // Consistencia en naming
	int				is_start;       // Consistencia con naming
	int				is_end;
	int				conn_count;     // Mejor que roomConn
	int				conn_capacity;  // Para realloc dinámico
	struct room		**connections;
	int				current_ant;    // ID de hormiga actual (-1 si vacía)
}	t_room;

typedef struct lemin
{
	int		ant_count;          // Consistencia
	int		room_count;         // Consistencia  
	int		room_capacity;      // Para realloc dinámico
	int		path_count;
	t_room	**rooms;            // Mejor que map
	t_room	*start_room;        // Puntero directo para eficiencia
	t_room	*end_room;          // Puntero directo para eficiencia
}	t_lemin;

// Function declarations
t_room	*roomNew(char *name, int isStart, int roomNum);
void	roomsClear(t_lemin *vars);
void	roomAddConn(t_room *room, t_room *new_connection);
t_room	*findRoomName(t_lemin *vars, char *name);
t_room	**addRoomToArray(t_room *room, t_lemin *vars);
int		makeRoomsConns(char **input, int i, t_lemin *vars);
t_path	**findAllPaths(t_lemin *vars);
void	distributeAnts(t_path **paths, t_lemin *vars);
void	simulateAntMovement(t_path **paths, t_lemin *vars);
#endif