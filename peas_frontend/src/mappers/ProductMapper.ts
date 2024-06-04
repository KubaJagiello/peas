import {AddProduct, Product} from "../dto/Product";
import {ProductRequest, ProductResponse, PaginationProductResponse} from "../generated/Api";
import {Pagination} from "../dto/Recipe";


export function mapToPaginatedProductResponse(paginatedProductResponse: PaginationProductResponse): Pagination<Product> {
  return {
    page: paginatedProductResponse.page,
    page_size: paginatedProductResponse.page_size,
    pages: paginatedProductResponse.pages,
    total: paginatedProductResponse.total,
    items: paginatedProductResponse.items.map((productResponse) => mapProductResponseToProduct(productResponse)),
  };
}


export function mapProductResponseToProduct(productResponse: ProductResponse): Product {
  return {
    id: productResponse.id,
    name: productResponse.name,
    proteins: productResponse.proteins,
    fats: productResponse.fats,
    carbohydrates: productResponse.carbohydrates,
    sodium: productResponse.sodium,
  }
}

export function mapProductToProductRequest(product: Product): ProductRequest {
  return {
    name: product.name,
    proteins: product.proteins,
    fats: product.fats,
    carbohydrates: product.carbohydrates,
    sodium: product.sodium
  }
}

export function mapAddProductToProductRequest(addProduct: AddProduct): ProductRequest {
  return {
    name: addProduct.name,
    proteins: addProduct.proteins,
    fats: addProduct.fats,
    carbohydrates: addProduct.carbohydrates,
    sodium: addProduct.sodium
  }
}
