import {RecipeProduct} from "./RecipeProduct";

export interface Pagination<T> {
  page: number;
  page_size: number;
  pages: number;
  total: number;
  items: T[]
}

export interface Recipe {
  id: string;
  name: string;
  description: string;
  servings: number;
  products: RecipeProduct[];
}

export interface AddRecipe {
  name: string;
  description: string;
  servings: number;
  products: RecipeProduct[];
}

