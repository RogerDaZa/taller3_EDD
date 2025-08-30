import csv
import os


CLIENTES_FILE = 'clientes.csv'
PEDIDOS_FILE = 'pedidos.csv'


def cargar_clientes():
    
    clientes = []
    if os.path.exists(CLIENTES_FILE):
        with open(CLIENTES_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['id_cliente'] = int(row['id_cliente'])
                row['activo'] = int(row['activo'])
                clientes.append(row)
    return clientes


def guardar_clientes(clientes):

    with open(CLIENTES_FILE, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id_cliente', 'nombre', 'apellido', 'telefono', 'activo']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for c in clientes:
            writer.writerow(c)


def registrar_cliente(clientes):
    
    nombre = input('Nombre: ').strip()
    apellido = input('Apellido: ').strip()
    telefono = input('Teléfono: ').strip()
    nuevo_id = obtener_nuevo_id(clientes, 'id_cliente')
    clientes.append({'id_cliente': nuevo_id, 'nombre': nombre, 'apellido': apellido,
                     'telefono': telefono, 'activo': 1})
    guardar_clientes(clientes)
    print("Cliente registrado con ID:", nuevo_id)


def listar_clientes(clientes):
    
    print("\nClientes activos:")
    for c in clientes:
        if c['activo'] == 1:
            print(c['id_cliente'], "-", c['nombre'], c['apellido'], "-", c['telefono'])


def eliminar_cliente(clientes): 

    id_elim = input('ID del cliente a eliminar: ').strip()
    if not id_elim.isdigit():
        print("ID inválido")
        return
    id_elim = int(id_elim)
    for c in clientes:
        if c['id_cliente'] == id_elim and c['activo'] == 1:
            c['activo'] = 0
            guardar_clientes(clientes)
            print("Cliente eliminado lógicamente")
            return
    print("Cliente no encontrado o ya estaba inactivo")


def cargar_pedidos():
    
    pedidos = []
    if os.path.exists(PEDIDOS_FILE):
        with open(PEDIDOS_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['id_pedido'] = int(row['id_pedido'])
                row['id_cliente'] = int(row['id_cliente'])
                row['precio'] = float(row['precio']) if row['precio'] else 0.0
                row['cantidad'] = int(row['cantidad']) if row['cantidad'] else 0
                row['activo'] = int(row['activo'])
                pedidos.append(row)
    return pedidos


def guardar_pedidos(pedidos):
    
    with open(PEDIDOS_FILE, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id_pedido', 'id_cliente', 'producto', 'precio', 'cantidad', 'activo']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for p in pedidos:
            writer.writerow(p)


def registrar_pedido(clientes, pedidos):
    
    id_cliente = input('ID del clientee: ').strip()
    if not id_cliente.isdigit():
        print("ID inválido")
        return
    id_cliente = int(id_cliente)
    cliente = next((c for c in clientes if c['id_cliente'] == id_cliente and c['activo'] == 1), None)
    if not cliente:
        print("Cliente no encontrado o inactivo")
        return

    producto = input("Producto: ").strip()
    precio = input("Precio (opcional): ").strip()
    cantidad = input("Cantidad (opcional): ").strip()
    precio = float(precio) if precio else 0.0
    cantidad = int(cantidad) if cantidad else 0

    nuevo_id = obtener_nuevo_id(pedidos, 'id_pedido')
    pedidos.append({'id_pedido': nuevo_id, 'id_cliente': id_cliente, 'producto': producto,
                    'precio': precio, 'cantidad': cantidad, 'activo': 1})
    guardar_pedidos(pedidos)
    print("Pedido registrado con ID:", nuevo_id)


def listar_pedidos_cliente(pedidos, clientes):
   
    id_cliente = input('ID del cliente: ').strip()
    if not id_cliente.isdigit():
        print("ID inválido")
        return
    id_cliente = int(id_cliente)
    cliente = next((c for c in clientes if c['id_cliente'] == id_cliente), None)
    if not cliente:
        print("Cliente no encontrado")
        return

    print("\nPedidos de", cliente['nombre'], cliente['apellido'])
    encontrado = False
    for p in pedidos:
        if p['id_cliente'] == id_cliente and p['activo'] == 1:
            encontrado = True
            print(p['id_pedido'], "-", p['producto'], "-", p['precio'], "-", p['cantidad'],p['activo'])
    if not encontrado:
        print("No tiene pedidos activos")


def guardar_venta(clientes, pedidos):
    """
    Registra una venta (similar a un pedido pero obligatorio con cantidad).
    """
    id_cliente = input("ID del cliente: ").strip()
    if not id_cliente.isdigit():
        print("ID inválido")
        return
    id_cliente = int(id_cliente)
    cliente = next((c for c in clientes if c['id_cliente'] == id_cliente and c['activo'] == 1), None)
    if not cliente:
        print("Cliente no encontrado o inactivo")
        return

    producto = input("Producto: ").strip()
    cantidad = input("Cantidad: ").strip()
    if not cantidad.isdigit():
        print("Cantidad inválida")
        return
    cantidad = int(cantidad)
    precio = input("Precio (opcional): ").strip()
    precio = float(precio) if precio else 0.0

    nuevo_id = obtener_nuevo_id(pedidos, 'id_pedido')
    pedidos.append({'id_pedido': nuevo_id, 'id_cliente': id_cliente, 'producto': producto,
                    'precio': precio, 'cantidad': cantidad, 'activo': 1})
    guardar_pedidos(pedidos)
    print("Venta registrada con ID:", nuevo_id)


def listar_ventas_por_cliente(clientes, pedidos):
    """
    Lista las ventas de un cliente y calcula el total.
    """
    nombre = input("Nombre del cliente: ").strip().lower()
    clientes_encontrados = [c for c in clientes if c['nombre'].lower() == nombre and c['activo'] == 1]

    if not clientes_encontrados:
        print("Cliente no encontrado o inactivo")
        return

    for cliente in clientes_encontrados:
        print("\nVentas de", cliente['nombre'], cliente['apellido'])
        ventas = [p for p in pedidos if p['id_cliente'] == cliente['id_cliente'] and p['activo'] == 1]
        if not ventas:
            print("No tiene ventas")
            continue
        total = 0
        for v in ventas:
            subtotal = v['precio'] * v['cantidad']
            total += subtotal
            print(v['producto'], "-", v['cantidad'], "x", v['precio'], "=", subtotal)
        print("TOTAL:", total)


# Utilidades 

def obtener_nuevo_id(items, id_field):
    
    if items:
        return max(item[id_field] for item in items) + 1
    else:
        return 1


def menu():
    clientes = cargar_clientes()
    pedidos = cargar_pedidos()

    while True:
        print("\nMENÚ PRINCIPAL")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Eliminar cliente ")
        print("4. Registrar pedido")
        print("5. Listar pedidos de cliente")
        print("6. Guardar venta")
        print("7. Listar ventas por cliente")
        print("8. eliminar pedido")
        print("9. Salir")

        opcion = input("Opción: ").strip()

        if opcion == '1':
            registrar_cliente(clientes)
        elif opcion == '2':
            listar_clientes(clientes)
        elif opcion == '3':
            eliminar_cliente(clientes)
        elif opcion == '4':
            registrar_pedido(clientes, pedidos)
        elif opcion == '5':
            listar_pedidos_cliente(pedidos, clientes)
        elif opcion == '6':
            guardar_venta(clientes, pedidos)
        elif opcion == '7':
            listar_ventas_por_cliente(clientes, pedidos)
        elif opcion == '9':
            print("Saliendo...")
            break
        elif opcion == '8':
            eliminar_pedido(pedidos)
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()