from requests import get, post

r = post(url="http://127.0.0.1:8080/login", data={"email": "dolores@gmail.com", "password": "Password1"})
productoTest1 = {
    'id': 0,
    'nombre': 'Producto 1 modificado',
    'cantidad': 999,
    "precio": 100,
    'fecha_inicio_venta': '2021-01-09',
    'fecha_fin_venta': '2021-01-09',
    'etiquetas': ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3'],
    'descripcion': 'No hay mucho que poner en un producto ficticio'
}

if r.status_code == 200:
    print(r.cookies)
    post(url="http://127.0.0.1:8080/igresar_datos_producto", data=productoTest1, cookies=r.cookies)
    r = post(url="http://127.0.0.1:8080/get_datos_producto", data={"id": 0, "a": "adas"}, cookies=r.cookies)
    if r.status_code == 200:
        print(r.text)
