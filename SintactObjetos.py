#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador Sintáctico LR(1) usando Objetos y Polimorfismo
"""

class Alumno:
    def __init__(self, codigo: str):
        self.codigo = codigo

    def muestra(self):
        pass


class Bachillerato(Alumno):
    def __init__(self, codigo: str, preparatoria: str):
        super().__init__(codigo)
        self.preparatoria = preparatoria

    def muestra(self):
        print(f"  [Alumno Bachillerato] Código: {self.codigo} | Preparatoria: {self.preparatoria}")


class Licenciatura(Alumno):
    def __init__(self, codigo: str, carrera: str, creditos: int):
        super().__init__(codigo)
        self.carrera = carrera
        self.creditos = creditos

    def muestra(self):
        print(f"  [Alumno Licenciatura] Código: {self.codigo} | Carrera: {self.carrera} | Créditos: {self.creditos}")



class ElementoPila:
    """Clase base para todos los elementos almacenados en la pila LR."""
    def muestra(self):
        pass

    def __str__(self):
        return ""


class Terminal(ElementoPila):
    """Representa un símbolo terminal en la pila (ej: 'a', '+', '$')."""
    def __init__(self, tipo: int, simbolo: str):
        self.tipo = tipo
        self.simbolo = simbolo

    def muestra(self):
        print(f"Terminal('{self.simbolo}', tipo={self.tipo})", end=" ")

    def __str__(self):
        return str(self.simbolo)


class NoTerminal(ElementoPila):
    """Representa un símbolo no terminal en la pila (ej: 'E')."""
    def __init__(self, tipo: int, simbolo: str):
        self.tipo = tipo
        self.simbolo = simbolo

    def muestra(self):
        print(f"NoTerminal('{self.simbolo}', tipo={self.tipo})", end=" ")

    def __str__(self):
        return str(self.simbolo)


class Estado(ElementoPila):
    """Representa un número de estado en la pila LR (ej: 0, 1, 2, ...)."""
    def __init__(self, estado: int):
        self.estado = estado

    def muestra(self):
        print(f"Estado({self.estado})", end=" ")

    def __str__(self):
        return str(self.estado)


class Pila:
    """Pila polimórfica que maneja objetos ElementoPila."""
    def __init__(self):
        self.items = []

    def push(self, elem: ElementoPila):
        self.items.append(elem)

    def pop(self) -> ElementoPila:
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Intento de pop en una pila vacía.")

    def top(self) -> ElementoPila:
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("Intento de top en una pila vacía.")

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def muestra(self):
        cadena = " ".join(str(elem) for elem in self.items)
        print(f"  Pila: [ {cadena} ]")



class Lexico:
    """Analizador léxico básico para la entrada."""
    def __init__(self, cadena: str):
        self.cadena = cadena.replace(" ", "")
        self.pos = 0
        self.simbolo = ""
        self.tipo = -1 

    def sigSimbolo(self):
        if self.pos >= len(self.cadena):
            self.simbolo = "$"
            self.tipo = 2
            return

        c = self.cadena[self.pos]
        self.pos += 1

        if c.isalpha():
            self.simbolo = c
            self.tipo = 0
        elif c == '+':
            self.simbolo = '+'
            self.tipo = 1
        elif c == '$':
            self.simbolo = '$'
            self.tipo = 2
        else:
            self.simbolo = c
            self.tipo = -1


def ejemplo_alumnos():
    print("=" * 60)
    print("EJEMPLO DE DEMOSTRACIÓN: Pila de Objetos Alumno (Polimorfismo)")
    print("=" * 60)

    pila_alumnos = []
    pila_alumnos.append(Licenciatura("345678", "Computacion", 200))
    pila_alumnos.append(Bachillerato("456789", "Preparatoria 12"))
    pila_alumnos.append(Licenciatura("987654", "Informatica", 50))

    print("Contenido de la pila de Alumnos:")
    for al in reversed(pila_alumnos):
        al.muestra()

    print("\nHaciendo POP...")
    removido = pila_alumnos.pop()
    print("Elemento desapilado:")
    removido.muestra()
    print()


def ejemplo1():
    print("=" * 60)
    print("EJEMPLO 1: Demostración de Pila con Objetos ElementoPila")
    print("=" * 60)

    pila = Pila()
    pila.push(Terminal(2, "$"))
    pila.push(Estado(0))
    pila.push(Terminal(0, "a"))
    pila.push(Estado(2))

    pila.muestra()
    print(f"Top element: {pila.top()}")
    pila.pop()
    pila.muestra()
    print()


def ejercicio1(cadena="a+b"):
    print("=" * 60)
    print(f"EJERCICIO 1 (con Objetos): Gramática E -> <id> + <id>")
    print(f"Cadena a analizar: '{cadena}'")
    print("=" * 60)

    tablaLR = [
        [2, 0,  0, 1],  
        [0, 0, -1, 0],  
        [0, 3,  0, 0],  
        [4, 0,  0, 0],  
        [0, 0, -2, 0]  
    ]

    id_reglas = [3]       
    nombre_reglas = ["E"]  
    lon_reglas = [3]  

    pila = Pila()
    pila.push(Terminal(2, "$"))
    pila.push(Estado(0))

    lexico = Lexico(cadena)
    lexico.sigSimbolo()

    paso = 1
    while True:
        top_elem = pila.top()
        if not isinstance(top_elem, Estado):
            print("Error Sintáctico: Se esperaba un Estado en el tope de la pila.")
            break

        estado_actual = top_elem.estado
        columna = lexico.tipo

        if columna == -1:
            print(f"Error Léxico: Carácter no reconocido '{lexico.simbolo}'")
            break

        accion = tablaLR[estado_actual][columna]

        print(f"Paso {paso}:")
        pila.muestra()
        print(f"  Entrada actual: '{lexico.simbolo}' (tipo {lexico.tipo})")

        if accion == -1:
            print(f"  Acción: {accion} (Aceptación)")
            print("\n>>> ¡CADENA ACEPTADA EXITOSAMENTE! <<<\n")
            break

        elif accion > 0:
            print(f"  Acción: {accion} (Desplazamiento al estado {accion})")
            pila.push(Terminal(lexico.tipo, lexico.simbolo))
            pila.push(Estado(accion))
            lexico.sigSimbolo()

        elif accion < 0:
            num_regla = abs(accion) - 2
            longitud = lon_reglas[num_regla]
            nt_id = id_reglas[num_regla]
            nt_nombre = nombre_reglas[num_regla]

            print(f"  Acción: {accion} (Reducción por Regla {num_regla + 1}, sacar {longitud} símbolo(s))")

            for _ in range(longitud * 2):
                pila.pop()

            estado_anterior = pila.top().estado
            transicion = tablaLR[estado_anterior][nt_id]

            pila.push(NoTerminal(nt_id, nt_nombre))
            pila.push(Estado(transicion))

        else:
            print(f"  Acción: 0 (Error)")
            print("\n>>> ERROR SINTÁCTICO: La cadena no pertenece al lenguaje <<<\n")
            break

        paso += 1


def ejercicio2(cadena="a+b"):
    print("=" * 60)
    print(f"EJERCICIO 2 (con Objetos): Gramática E -> <id> + E | <id>")
    print(f"Cadena a analizar: '{cadena}'")
    print("=" * 60)

   
    tablaLR = [
        [2, 0,  0, 1],  
        [0, 0, -1, 0],  
        [0, 3, -3, 0],  
        [2, 0,  0, 4],  
        [0, 0, -2, 0]  
    ]

    id_reglas = [3, 3]
    nombre_reglas = ["E", "E"]
    lon_reglas = [3, 1]  

    pila = Pila()
    pila.push(Terminal(2, "$"))
    pila.push(Estado(0))

    lexico = Lexico(cadena)
    lexico.sigSimbolo()

    paso = 1
    while True:
        top_elem = pila.top()
        if not isinstance(top_elem, Estado):
            print("Error Sintáctico: Se esperaba un Estado en el tope de la pila.")
            break

        estado_actual = top_elem.estado
        columna = lexico.tipo

        if columna == -1:
            print(f"Error Léxico: Carácter no reconocido '{lexico.simbolo}'")
            break

        accion = tablaLR[estado_actual][columna]

        print(f"Paso {paso}:")
        pila.muestra()
        print(f"  Entrada actual: '{lexico.simbolo}' (tipo {lexico.tipo})")

        if accion == -1:
            print(f"  Acción: {accion} (Aceptación)")
            print("\n>>> ¡CADENA ACEPTADA EXITOSAMENTE! <<<\n")
            break

        elif accion > 0:
            print(f"  Acción: {accion} (Desplazamiento al estado {accion})")
            pila.push(Terminal(lexico.tipo, lexico.simbolo))
            pila.push(Estado(accion))
            lexico.sigSimbolo()

        elif accion < 0:
            num_regla = abs(accion) - 2
            longitud = lon_reglas[num_regla]
            nt_id = id_reglas[num_regla]
            nt_nombre = nombre_reglas[num_regla]

            print(f"  Acción: {accion} (Reducción por Regla {num_regla + 1}, sacar {longitud} símbolo(s))")

            for _ in range(longitud * 2):
                pila.pop()

            estado_anterior = pila.top().estado
            transicion = tablaLR[estado_anterior][nt_id]

            pila.push(NoTerminal(nt_id, nt_nombre))
            pila.push(Estado(transicion))

        else:
            print(f"  Acción: 0 (Error)")
            print("\n>>> ERROR SINTÁCTICO: La cadena no pertenece al lenguaje <<<\n")
            break

        paso += 1


def main():
    ejemplo_alumnos()
    ejemplo1()
    
    ejercicio1("a+b")
    
    ejercicio2("a")
    ejercicio2("a+b")
    ejercicio2("a+b+c")


if __name__ == "__main__":
    main()