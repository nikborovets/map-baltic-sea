# Карта Балтийского моря

Интерактивная карта береговых мареографов Балтийского моря. Цвет маркера показывает корреляцию наблюдений с Baltic Sea Physics Reanalysis. По нажатию на маркер открываются графики уровня моря, когерентности, BIAS и RMSE.

Рабочая версия: [https://nikborovets.github.io/map-baltic-sea/](https://nikborovets.github.io/map-baltic-sea/)

Проект связан с работой «Валидация массивов изменений уровня Балтийского моря из Baltic Sea Physics Reanalysis по данным наблюдений на береговых мареографах», конференция MARESEDU (Москва). [PDF](https://nikborovets.github.io/data/Borovets_theses_maresedu.pdf)

## Что внутри

- `baltic_sea_map_with_colorbar.html` — карта на Leaflet
- `processed_graphs/` — графики по станциям
- `index.html` — входная страница для GitHub Pages

Сайт публикуется встроенным GitHub Pages из ветки `main`. После пуша в `main` страница обновляется сама, отдельный сервер не нужен.
