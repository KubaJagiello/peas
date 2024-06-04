import {Api} from "../../generated/Api";
import {
  mapAddRecipeToRecipeRequest,
  mapRecipeResponseToRecipe,
  mapRecipeToRecipeRequest, mapToPaginatedRecipeResponse
} from "../../mappers/RecipeMapper";
import {Recipe, AddRecipe, Pagination} from "../../dto/Recipe";
import {Product} from "../../dto/Product";
import {mapToPaginatedProductResponse} from "../../mappers/ProductMapper";

export class RecipeService {
  private apiClient = new Api({baseUrl: "http://localhost:8000"});

  public async getAllRecipes(pageNumber: number, pageSize: number): Promise<Pagination<Recipe>> {
    try {
      const response = await this.apiClient.api.getAllRecipesApiV1RecipesGet(
          {page: pageNumber, size: pageSize}
      );
      return mapToPaginatedRecipeResponse(response.data)
    } catch (error) {
      throw new Error(`Failed to fetch recipes: ${error}`);
    }
  }
  public async searchRecipeByName(name: string): Promise<Pagination<Recipe>> {
    try {
      const response = await this.apiClient.api.searchRecipesApiV1RecipesSearchGet(
          {name: name, page: 1, size: 20}
      );
      return mapToPaginatedRecipeResponse(response.data);
    } catch (error) {
      throw new Error(`Failed to fetch recipes: ${error}`);
    }
  }

  public async getRecipeById(recipeId: string): Promise<Recipe> {
    try {
      const response = await this.apiClient.api.getRecipeByIdApiV1RecipesRecipeIdGet(recipeId);
      return mapRecipeResponseToRecipe(response.data);
    } catch (error) {
      throw new Error(`Failed to fetch recipe: ${error}`);
    }
  }

  public async addRecipe(addRecipe: AddRecipe): Promise<Recipe> {
    try {
      const recipeRequest = mapAddRecipeToRecipeRequest(addRecipe);
      const recipeResponse = await this.apiClient.api.createRecipeApiV1RecipesPost(recipeRequest);
      return mapRecipeResponseToRecipe(recipeResponse.data);
    } catch (error) {
      throw new Error(`Failed to add recipe: ${error}`);
    }
  }

  public async updateRecipe(
      recipe: Recipe,
      recipeId: string
  ): Promise<Recipe> {
    try {
      const recipeRequest = mapRecipeToRecipeRequest(recipe);
      const response = await this.apiClient.api.updateRecipeApiV1RecipesRecipeIdPut(
          recipeId,
          recipeRequest
      );
      return mapRecipeResponseToRecipe(response.data);
    } catch (error) {
      throw new Error(`Failed to update recipe: ${error}`);
    }
  }

  public async deleteRecipe(recipeId: string): Promise<void> {
    try {
      await this.apiClient.api.deleteRecipeApiV1RecipesRecipeIdDelete(recipeId);
    } catch (error) {
      throw new Error(`Failed to delete recipe: ${error}`);
    }
  }
}
