import {AddRecipe, Pagination, Recipe} from "../dto/Recipe";
import {RecipeProduct} from "../dto/RecipeProduct";
import {
  RecipeResponse,
  RecipeProductResponse,
  RecipeRequest,
  ProductDetail,
  PaginationRecipeResponse
} from "../generated/Api";
import {mapProductResponseToProduct} from "./ProductMapper";
import {mapToProductUnit, mapToUnit} from "./UnitMapper";

export function mapToPaginatedRecipeResponse(paginationRecipeResponse: PaginationRecipeResponse): Pagination<Recipe> {
  return {
    page: paginationRecipeResponse.page,
    page_size: paginationRecipeResponse.page_size,
    pages: paginationRecipeResponse.pages,
    total: paginationRecipeResponse.total,
    items: paginationRecipeResponse.items.map((recipeResponse) => mapRecipeResponseToRecipe(recipeResponse)),
  };
}


export function mapRecipeResponseToRecipe(recipeResponse: RecipeResponse): Recipe {
  return {
    id: String(recipeResponse.id),
    name: recipeResponse.name,
    description: recipeResponse.description,
    servings: recipeResponse.servings,
    products: recipeResponse.products.map((product) => mapRecipeProductResponseToRecipeProduct(product)),
  };
}

export function mapRecipeProductResponseToRecipeProduct(recipeProductResponse: RecipeProductResponse): RecipeProduct {
  return {
    product: mapProductResponseToProduct(recipeProductResponse.product),
    quantity: recipeProductResponse.quantity,
    unit: mapToProductUnit(recipeProductResponse.unit),
  };
}

export function mapRecipeProductToProductDetail(recipeProduct: RecipeProduct): ProductDetail {
  return {
    id: recipeProduct.product.id,
    quantity: recipeProduct.quantity,
    unit: mapToUnit(recipeProduct.unit),
  };
}

export function mapRecipeToRecipeRequest(recipe: Recipe): RecipeRequest {
  return {
    name: recipe.name,
    description: recipe.description,
    servings: recipe.servings,
    products: recipe.products.map((product) => mapRecipeProductToProductDetail(product)),
  };
}

export function mapAddRecipeToRecipeRequest(addRecipe: AddRecipe): RecipeRequest {
  return {
    name: addRecipe.name,
    description: addRecipe.description,
    servings: addRecipe.servings,
    products: addRecipe.products.map((product) => mapRecipeProductToProductDetail(product)),
  }
}
