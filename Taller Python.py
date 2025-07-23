# Modelo de libro con Pydantic
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str 
    paginas: int
    precio: float
    genero: str

# Base de datos simulada
libros_db = [
    Libro(id=1, titulo="Cien años de soledad", autor="Gabriel García Márquez", paginas=432, precio=15.99, genero="Ficción"),
    Libro(id=2, titulo="1984", autor="George Orwell", paginas=328, precio=12.50, genero="Ciencia Ficción"),
    Libro(id=3, titulo="El amor en los tiempos del cólera", autor="Gabriel García Márquez", paginas=368, precio=14.75, genero="Ficción")
]

# API con FastAPI
app = FastAPI()

@app.get("/libros", response_model=List[Libro])
def listar_libros():
    return libros_db

@app.post("/libros", response_model=Libro, status_code=201)
def crear_libro(libro: Libro):
    nuevo_id = len(libros_db) + 1
    libro.id = nuevo_id
    libros_db.append(libro)
    return libro

@app.delete("/libros/{libro_id}", status_code=204)
def eliminar_libro(libro_id: int):
    for i, libro in enumerate(libros_db):
        if libro.id == libro_id:
            libros_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.patch("/libros/{libro_id}/aplicar-descuento")
def aplicar_descuento(libro_id: int, descuento: float):
    for libro in libros_db:
        if libro.id == libro_id:
            if descuento < 1 or descuento > 90:
                raise HTTPException(status_code=400, detail="Porcentaje de descuento inválido")
            libro.precio = libro.precio * (1 - descuento/100)
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")
