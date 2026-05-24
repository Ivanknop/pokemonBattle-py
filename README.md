# Pokémon Battle

Pokémon Battle es una aplicación web de combate entre Pokémon. El objetivo principal del proyecto es permitir que un usuario elija un Pokémon, enfrente a un rival aleatorio y observe el desarrollo de una batalla por turnos.

La aplicación incluye una lógica básica de combate basada en estadísticas como ataque, defensa, ataque especial, defensa especial, velocidad, puntos de vida y tipos Pokémon. También incorpora una tabla de tipos para calcular ventajas, resistencias e inmunidades entre Pokémon.

## Objetivo del proyecto

El proyecto fue desarrollado como una práctica de programación orientada a objetos, desarrollo web y modelado de reglas de juego.

La aplicación busca combinar:

- selección de personajes;
- generación aleatoria de rivales;
- combate por turnos;
- cálculo de daño según estadísticas;
- modificadores por tipo;
- sistema de suerte por turno;
- visualización del historial de batalla;
- detección automática del ganador.

El foco principal no es replicar exactamente el sistema oficial de combate Pokémon, sino construir una versión propia, sencilla y extensible, útil para experimentar con lógica de juego, interfaces web y organización de código.

## Tecnologías utilizadas

La primera versión fue realizada en Python utilizando Flask.

El backend actual incluye:

- Python;
- Flask;
- Jinja2;
- SQLAlchemy;
- SQLite;
- Pytest para pruebas automatizadas.

La aplicación fue organizada separando la lógica de dominio en clases propias, como `Pokemon`, `Fight`, `CombatRules` y `TypeChart`.

## Estado del proyecto

Actualmente la aplicación funciona como una app Flask renderizada con templates HTML.

Sin embargo, el proyecto será migrado o reimplementado en React para facilitar su publicación libre en plataformas de hosting estático o servicios gratuitos de despliegue.

La decisión de llevar la interfaz a React responde principalmente a una cuestión práctica: React permite publicar más fácilmente una versión accesible online, sin depender necesariamente de un servidor Flask activo para la interfaz.

## Funcionalidades principales

- Elección de un Pokémon por parte del jugador.
- Selección aleatoria del rival.
- Combate por turnos.
- Ataque del primer Pokémon según iniciativa.
- Contraataque del segundo Pokémon si sigue con vida.
- Cálculo de daño según estadísticas y tipos.
- Sistema de suerte que puede modificar el turno.
- Historial de eventos de batalla.
- Pantalla de ganador.
- Tabla de tipos consultable desde la navegación.

## Estructura general

```text
api/
├── app.py
├── model/
│   ├── pokemon.py
│   ├── fight.py
│   ├── combat_rules.py
│   ├── type_chart.py
│   ├── handler_db.py
│   └── model.py
├── templates/
│   ├── choose_character.html
│   ├── fight.html
│   ├── type_chart.html
│   ├── header.html
│   └── footer.html
├── static/
│   └── style.css
└── files/
    └── pokemon.db