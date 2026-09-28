# Analizador Sintáctico LR(1) usando Objetos y Polimorfismo

Proyecto académico en **Python** que implementa un analizador sintáctico basado en tablas **LR(1)** utilizando programación orientada a objetos, herencia y polimorfismo.

El programa incluye una implementación de una **pila polimórfica**, un analizador léxico básico y dos ejercicios de análisis sintáctico con diferentes gramáticas. Además, contiene un ejemplo independiente que demuestra el polimorfismo mediante objetos de tipo `Alumno`, `Bachillerato` y `Licenciatura`.

## Descripción

El proyecto simula el funcionamiento de un analizador LR mediante una tabla de acciones y transiciones. La pila del analizador no almacena únicamente valores simples, sino objetos que representan los distintos elementos del proceso sintáctico:

* **Terminal**: representa símbolos de entrada como identificadores, `+` y `$`.
* **NoTerminal**: representa símbolos gramaticales como `E`.
* **Estado**: representa los estados de la máquina LR.
* **Pila**: administra los objetos anteriores mediante operaciones `push`, `pop` y `top`.

La implementación aprovecha el **polimorfismo** porque las diferentes clases heredan de una clase base común y pueden ser almacenadas y manipuladas desde referencias del tipo `ElementoPila`.

## Tecnologías

* Python 3
* Programación Orientada a Objetos (POO)
* Herencia
* Polimorfismo
* Análisis léxico
* Análisis sintáctico LR(1)
* Tablas de acciones y transiciones

No se utilizan librerías externas.

## Estructura del proyecto

```text
.
├── SintactObjetos.py
└── README.md
```

Todo el funcionamiento principal del proyecto se encuentra actualmente en `SintactObjetos.py`.

## Clases principales

### `Alumno`

Clase base utilizada para demostrar herencia y polimorfismo.

### `Bachillerato`

Hereda de `Alumno` y agrega el atributo `preparatoria`.

### `Licenciatura`

Hereda de `Alumno` y agrega los atributos `carrera` y `creditos`.

Cada subclase redefine el método `muestra()`, demostrando **polimorfismo por sobrescritura de métodos**.

### `ElementoPila`

Clase base para los elementos que pueden almacenarse en la pila LR.

### `Terminal`

Representa un símbolo terminal y almacena:

* `tipo`
* `simbolo`

### `NoTerminal`

Representa un símbolo no terminal de la gramática.

### `Estado`

Representa un estado del autómata LR y almacena su número de estado.

### `Pila`

Implementa la pila utilizada por el analizador sintáctico.

Métodos principales:

```python
push(elem)
pop()
top()
is_empty()
muestra()
```

La pila acepta objetos de tipo `ElementoPila`, por lo que puede contener terminales, no terminales y estados.

### `Lexico`

Realiza un análisis léxico básico de la cadena de entrada.

La clasificación utilizada por el programa es:

| Tipo | Símbolo                                      |
| ---: | -------------------------------------------- |
|  `0` | Identificador: cualquier carácter alfabético |
|  `1` | `+`                                          |
|  `2` | `$`                                          |
| `-1` | Carácter no reconocido                       |

Los espacios son eliminados antes de iniciar el análisis.

## Funcionamiento del analizador LR

El analizador comienza colocando en la pila:

```text
$ 0
```

Posteriormente obtiene el primer símbolo de entrada y consulta la tabla LR utilizando:

```python
tablaLR[estado_actual][columna]
```

Las acciones utilizadas por el programa son:

| Acción | Significado                                             |
| -----: | ------------------------------------------------------- |
|  `> 0` | Desplazamiento (`shift`) al estado indicado             |
| `< -1` | Reducción (`reduce`) mediante una regla de la gramática |
|   `-1` | Aceptación                                              |
|    `0` | Error                                                   |

Durante un **desplazamiento**, el analizador agrega a la pila el terminal actual y el nuevo estado.

Durante una **reducción**, elimina de la pila los símbolos correspondientes al lado derecho de la producción, consulta la transición hacia el no terminal resultante y vuelve a introducir el no terminal junto con su nuevo estado.

El programa imprime cada paso para poder observar la evolución de la pila y la decisión tomada por el analizador.

## Ejercicio 1

### Gramática

```text
E -> <id> + <id>
```

La implementación utiliza una tabla LR predefinida y una única regla de reducción.

Ejemplo:

```text
a+b
```

Este ejemplo es aceptado por el analizador.

Una ejecución muestra una secuencia similar a:

```text
Paso 1:
  Pila: [ $ 0 ]
  Entrada actual: 'a' (tipo 0)
  Acción: 2 (Desplazamiento al estado 2)

Paso 2:
  Pila: [ $ 0 a 2 ]
  Entrada actual: '+' (tipo 1)
  Acción: 3 (Desplazamiento al estado 3)

Paso 3:
  Pila: [ $ 0 a 2 + 3 ]
  Entrada actual: 'b' (tipo 0)
  Acción: 4 (Desplazamiento al estado 4)

Paso 4:
  Acción: -2 (Reducción por Regla 1)

Paso 5:
  Pila: [ $ 0 E 1 ]
  Acción: -1 (Aceptación)
```

## Ejercicio 2

### Gramática

```text
E -> <id> + E
E -> <id>
```

Esta gramática permite reconocer expresiones formadas por identificadores separados por `+`.

Ejemplos ejecutados por el programa:

```text
a
a+b
a+b+c
```

Los tres ejemplos son aceptados.

En este caso existen dos reglas de reducción:

```text
Regla 1: E -> <id> + E
Regla 2: E -> <id>
```

La tabla LR y los arreglos:

```python
id_reglas
nombre_reglas
lon_reglas
```

se utilizan para determinar qué producción aplicar durante una reducción.

## Ejemplo de polimorfismo con `Alumno`

El programa también incluye una demostración independiente del uso de objetos:

```python
pila_alumnos.append(Licenciatura("345678", "Computacion", 200))
pila_alumnos.append(Bachillerato("456789", "Preparatoria 12"))
pila_alumnos.append(Licenciatura("987654", "Informatica", 50))
```

Aunque los objetos pertenecen a clases diferentes, todos pueden almacenarse en la misma lista porque comparten la clase base `Alumno`.

Al recorrer la lista y llamar:

```python
al.muestra()
```

cada objeto ejecuta su propia implementación del método `muestra()`.

Esto permite observar directamente el concepto de **polimorfismo**.

## Ejemplo de pila LR

También se incluye una demostración básica de la clase `Pila`:

```python
pila = Pila()

pila.push(Terminal(2, "$"))
pila.push(Estado(0))
pila.push(Terminal(0, "a"))
pila.push(Estado(2))
```

La pila resultante se visualiza como:

```text
Pila: [ $ 0 a 2 ]
```

Y es posible consultar el elemento superior:

```python
pila.top()
```

o eliminarlo:

```python
pila.pop()
```

## Cómo ejecutar el proyecto

Requiere **Python 3**.

Desde la terminal:

```bash
python SintactObjetos.py
```

En algunos sistemas también puede utilizarse:

```bash
python3 SintactObjetos.py
```

La función `main()` ejecuta automáticamente las demostraciones y los ejercicios incluidos:

```python
ejemplo_alumnos()
ejemplo1()

ejercicio1("a+b")

ejercicio2("a")
ejercicio2("a+b")
ejercicio2("a+b+c")
```

## Conceptos de POO utilizados

### Herencia

```text
Alumno
├── Bachillerato
└── Licenciatura
```

y:

```text
ElementoPila
├── Terminal
├── NoTerminal
└── Estado
```

### Polimorfismo

Las clases derivadas implementan su propia versión de `muestra()`.

### Abstracción

`ElementoPila` define la interfaz común de los elementos que pueden formar parte de la pila.

### Encapsulamiento

Cada objeto administra sus propios atributos, como `estado`, `tipo`, `simbolo`, `codigo`, `carrera` o `creditos`.

## Objetivo académico

El objetivo principal del proyecto es relacionar los conceptos de **análisis sintáctico LR**, **tablas de parsing** y **programación orientada a objetos**, mostrando cómo una estructura de datos puede trabajar con distintos tipos de objetos mediante herencia y polimorfismo.

## Estado del proyecto

Proyecto de carácter académico y demostrativo. La implementación utiliza tablas LR ya definidas para los ejercicios incluidos y no construye automáticamente el autómata LR a partir de una gramática.

---

### Autor
De la Paz Mendoza Ian Alexandro.

Proyecto desarrollado en Python como ejercicio de **Análisis Sintáctico y Programación Orientada a Objetos**.
