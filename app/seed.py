"""Crea las tablas (solo si usas SQLite) y carga datos de prueba.

Uso:  python -m app.seed
"""
from .database import Base, SessionLocal, engine
from .models import Masa, Pizza, PizzaTamano, Tamano

MENU = [
    # sabor, descripción, imagen, etiqueta, destacado, (chica, mediana, familiar)
    ("La Clásica (Pepperoni)", "Queso mozzarella derretido y generosas rodajas de pepperoni tradicional.", "/img/pepperoni.jpg", "MÁS VENDIDA", True, (110, 160, 220)),
    ("Hawaiana", "Jamón selecto, piña dulce en trozos y extra queso mozzarella fundido.", "/img/hawaiana.jpg", "TROPICAL", True, (120, 170, 230)),
    ("La Mexicana", "Chorizo, jalapeño en rodajas, cebolla morada y deliciosa base de frijoles.", "/img/mexicana.jpg", "LOCAL", True, (135, 185, 250)),
    ("Carnes Frías", "Salami, pepperoni, jamón, salchicha y crujiente tocino ahumado.", "/img/carnes.jpg", "ESPECIAL", False, (145, 195, 270)),
    ("Vegetariana", "Champiñones, pimiento verde, cebolla, aceitunas negras y jitomate fresco.", "/img/vegetariana.jpg", "VEGETARIANA", False, (130, 180, 240)),
]
MASAS = [("Tradicional", 0), ("Fina y Crujiente", 0), ("Orilla Rellena de Queso", 30), ("Orilla Queso + Pepperoni", 45)]


def main() -> None:
    if engine.dialect.name == "sqlite":
        Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.query(Pizza).first():
            print("Ya hay datos, no se insertó nada.")
            return
        tamanos = [Tamano(nombre=n, orden=i) for i, n in enumerate(["Chica", "Mediana", "Familiar"], 1)]
        db.add_all(tamanos)
        db.add_all(Masa(nombre=n, precio_extra=p) for n, p in MASAS)
        db.flush()
        for sabor, desc, img, etiqueta, dest, precios in MENU:
            p = Pizza(sabor=sabor, descripcion=desc, imagen_url=img, etiqueta=etiqueta, destacado=dest)
            db.add(p)
            db.flush()
            for t, precio in zip(tamanos, precios):
                db.add(PizzaTamano(id_pizza=p.id_pizza, id_tamano=t.id_tamano, precio=precio, stock=20))
        db.commit()
        print("Datos de prueba cargados.")


if __name__ == "__main__":
    main()
