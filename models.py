@dataclass(kw_only = True)
class Product:

    id: Optional[int] = None
    name: str
    price: float
    category: str
    description: str