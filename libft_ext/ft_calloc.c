/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jainavas <jainavas@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/08/12 15:21:19 by jainavas          #+#    #+#             */
/*   Updated: 2024/08/12 15:21:19 by jainavas         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	void	*res;

	res = malloc(nmemb * size);
	if (res == NULL)
		return (NULL);
	ft_bzero(res, nmemb * size);
	return (res);
}

void	*ft_realloc(void *actual, size_t old_size, size_t new_size)
{
	void	*new_ptr;
	size_t	copy_size;

	if (new_size == 0)
	{
		free(actual);
		return (NULL);
	}
	if (actual == NULL)
		return (malloc(new_size));
	new_ptr = malloc(new_size);
	if (new_ptr == NULL)
		return (NULL);
	copy_size = (old_size < new_size) ? old_size : new_size;
	ft_memcpy(new_ptr, actual, copy_size);
	if (new_size > old_size)
		ft_bzero((char *)new_ptr + old_size, new_size - old_size);
	free(actual);
	return (new_ptr);
}

void	**ft_realloc_rm_idx(void **array, size_t size, size_t idx)
{
	void	**new_array;
	size_t	i;
	size_t	j;

	if (!array || idx >= size || size == 0)
		return (NULL);
	if (size == 1)
		return (free(array), NULL);
	new_array = malloc(sizeof(void *) * (size - 1));
	if (!new_array)
		return (NULL);
	i = 0;
	j = 0;
	while (i < size)
	{
		if (i != idx)
		{
			new_array[j] = array[i];
			j++;
		}
		i++;
	}
	free(array);
	return (new_array);
}
