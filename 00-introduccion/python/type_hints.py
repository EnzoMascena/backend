my_string_variable = "Hello, World!"
print(my_string_variable)
print(type(my_string_variable))  # Output: <class 'str'>

my_integer_variable = 42
print(my_integer_variable)
print(type(my_integer_variable))  # Output: <class 'int'>

my_string_variable = 5
print(my_string_variable)
print(type(my_string_variable))  # Output: <class 'int'>

my_type_variable: str = "Esta es una cadena de texto tipada"
print(my_type_variable)
print(type(my_type_variable))  # Output: <class 'str'>

my_type_variable = 10
print(my_type_variable)
print(type(my_type_variable))  # Output: <class 'int'>

# Recomendaciones de FastAPI para el uso de type hints:
def get_full_name(first_name: str, last_name: str) -> str:
    full_name = f"{first_name} {last_name} {"Alumno de FastAPI"}" 
    return full_name

print(get_full_name("Juan", "Pérez"))  # Output: Juan Pérez Alumno de FastAPI

#Recomendaciones de FastAPI para el uso de type hints:
# 1. Usa tipos de datos explícitos para los parámetros de las funciones y los valores de retorno.
# 2. Utiliza tipos de datos estándar de Python, como str, int, float
# 3. Define tipos personalizados para representar estructuras de datos complejas.
