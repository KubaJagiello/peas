import { Product } from "./Product";
import { Unit } from "./Unit";

export interface RecipeProduct {
    quantity: number;
    unit: Unit;
    product: Product;
}