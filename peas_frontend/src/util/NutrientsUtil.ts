import {RecipeProduct} from "../dto/RecipeProduct";
import {Product} from "../dto/Product";

export class NutrientsUtil {
  public static countCalories(recipeProduct: RecipeProduct): number;
  public static countCalories(product: Product): number;

  public static countCalories(item: RecipeProduct | Product): number {
    const product = "product" in item ? item.product : item;
    return Math.ceil(product.proteins * 4.0 + product.carbohydrates * 4.0 + product.fats * 9.0);
  }
}