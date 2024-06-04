import {Api} from "../../generated/Api";
import {
  mapAddProductToProductRequest,
  mapProductResponseToProduct,
  mapProductToProductRequest, mapToPaginatedProductResponse
} from "../../mappers/ProductMapper";
import {Product, AddProduct} from "../../dto/Product";
import {Pagination} from "../../dto/Recipe";


export class ProductService {
  private apiClient = new Api({baseUrl: "http://localhost:8000"});

  public async getAllProducts(): Promise<Pagination<Product>> {
    try {
      const response = await this.apiClient.api.getAllProductsApiV1ProductsGet();
      return mapToPaginatedProductResponse(response.data);
    } catch (error) {
      throw new Error(`Failed to fetch recipes: ${error}`);
    }
  }

  public async searchProductByName(name: string): Promise<Pagination<Product>> {
    try {
      const response = await this.apiClient.api.searchProductsApiV1ProductsSearchGet(
          {name: name, page: 1, size: 20}
      );
      return mapToPaginatedProductResponse(response.data);
    } catch (error) {
      throw new Error(`Failed to fetch recipes: ${error}`);
    }
  }

  public async getProductById(productId: string): Promise<Product> {
    try {
      const response = await this.apiClient.api.getProductByIdApiV1ProductsProductIdGet(productId);
      return mapProductResponseToProduct(response.data);
    } catch (error) {
      throw new Error(`Failed to fetch product: ${error}`)
    }
  }

  public async addProduct(addProduct: AddProduct): Promise<Product> {
    try {
      const productRequest = mapAddProductToProductRequest(addProduct);
      const response = await this.apiClient.api.createProductApiV1ProductsPost(productRequest);
      return mapProductResponseToProduct(response.data);
    } catch (error) {
      throw new Error(`Failed to add product: ${error}`)
    }
  }

  public async updateProduct(
      productId: string,
      product: Product
  ): Promise<Product> {
    try {
      const productRequest = mapProductToProductRequest(product);
      const response = await this.apiClient.api.updateProductApiV1ProductsProductIdPut(productId, productRequest);
      return mapProductResponseToProduct(response.data);
    } catch (error) {
      throw new Error(`Failed to add product: ${error}`)
    }
  }

  public async deleteProduct(productId: string): Promise<void> {
    try {
      await this.apiClient.api.deleteProductApiV1ProductsProductIdDelete(productId);
    } catch (error) {
      throw new Error(`Failed to delete product: ${error}`)
    }
  }
}