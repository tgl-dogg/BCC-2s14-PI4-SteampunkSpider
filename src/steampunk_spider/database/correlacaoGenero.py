# pegar a quantidade de horas totais em cada gênero
SELECT genre.name, SUM(hours) AS soma 
FROM rel_player_software 
INNER JOIN rel_software_genre ON rel_player_software.fk_software = rel_software_genre.fk_software
INNER JOIN genre ON rel_software_genre.fk_genre = genre.id_genre
GROUP BY rel_software_genre.fk_genre
ORDER BY soma DESC
LIMIT 5

#teste
SELECT genre.name AS genero, SUM(rel_player_software.hours) AS horas
FROM rel_player_software
INNER JOIN player ON rel_player_software.fk_player = player.id_player
INNER JOIN software ON rel_player_software.fk_software = software.id_software
INNER JOIN genre ON rel_software_genre = genre.id_genre
LIMIT 1

#teste
SELECT player.name AS jogador, genre.name AS genre, SUM(rel_player_software.hours) AS horas
FROM rel_player_software
INNER JOIN player ON rel_player_software.fk_player = player.id_player
INNER JOIN software ON rel_player_software.fk_software = software.id_software
INNER JOIN rel_software_genre ON rel_software_genre.fk_software = software.id_software
INNER JOIN genre ON rel_software_genre.fk_genre = genre.id_genre
GROUP BY jogador
ORDER BY horas DESC
LIMIT 3

#teste
(SELECT player.username AS jogador, genre.name AS genero, SUM(rel_player_software.hours) AS horas
FROM rel_player_software
INNER JOIN player ON rel_player_software.fk_player = player.id_player
INNER JOIN rel_software_genre ON rel_software_genre.fk_software = rel_player_software.fk_software
INNER JOIN genre ON rel_software_genre.fk_genre = genre.id_genre
WHERE player.id_player <= 3
GROUP BY jogador, genero
ORDER BY jogador, horas DESC)

# pegar o gênero mais jogado de cada jogador
SELECT jogador, genero, MAX(horas) FROM
(SELECT player.username AS jogador, genre.name AS genero, SUM(rel_player_software.hours) AS horas
FROM (rel_player_software 
INNER JOIN player ON rel_player_software.fk_player = player.id_player
INNER JOIN rel_software_genre ON rel_software_genre.fk_software = rel_player_software.fk_software
INNER JOIN genre ON rel_software_genre.fk_genre = genre.id_genre) 
GROUP BY jogador, genero
ORDER BY jogador, horas DESC) p
GROUP BY jogador