from sqlalchemy.orm import Session

from peas_app.database.models.models import Product
from peas_app.database.repositories.product_repository import ProductRepository


def test_update_product(
    product_repository: ProductRepository, product_1: Product
) -> None:
    product_repository.add(product_1)
    product_1.fats = 3.0
    product_1.name = "different name"
    product_1.sodium = 1.0
    product_repository.update(product_1)

    retrieved_product = product_repository.get_by_id(_id=123)

    assert _products_are_equal(retrieved_product, product_1)


def test_delete_product(
    product_repository: ProductRepository, product_1: Product
) -> None:
    product_repository.add(product_1)
    product_repository.delete(product_1)

    retrieved_product = product_repository.get_by_id(_id=123)

    assert retrieved_product is None


def test_add_product(
    product_repository: ProductRepository, product_1: Product
) -> None:
    product_repository.add(product_1)
    retrieved_product = product_repository.get_by_id(_id=123)

    assert _products_are_equal(retrieved_product, product_1)


def test_get_all_products(
    product_repository: ProductRepository, product_1: Product
) -> None:
    product_repository.add(product_1)

    retrieved_products = product_repository.get_all(page_number=0, page_size=10)

    assert len(retrieved_products) == 1
    assert _products_are_equal(retrieved_products[0], product_1)


def test_get_products_by_ids(
    session: Session,
    product_1: Product,
    product_2: Product,
    product_3: Product,
) -> None:
    product_repo = ProductRepository(session)

    product_repo.add(product_1)
    product_repo.add(product_2)
    product_repo.add(product_3)

    retrieved_products = product_repo.get_by_ids([123, 456])

    assert len(retrieved_products) == 2
    assert [retrieved_products[0].id, retrieved_products[1].id] == [
        product_1.id,
        product_2.id,
    ]


def test_get_by_id(
    product_repository: ProductRepository, product_1: Product
) -> None:
    product_repository.add(product_1)

    retrieved_product = product_repository.get_by_id(_id=123)

    assert _products_are_equal(retrieved_product, product_1)


def _products_are_equal(product_a: Product, product_b: Product) -> bool:
    return (
        product_a is not None
        and product_b is not None
        and product_a.id == product_b.id
        and product_a.name == product_b.name
        and product_a.proteins == product_b.proteins
        and product_a.fats == product_b.fats
        and product_a.carbohydrates == product_b.carbohydrates
        and product_a.sodium == product_b.sodium
        and product_a.calories == product_b.calories
    )
