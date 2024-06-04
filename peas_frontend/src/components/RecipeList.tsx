import React, {useState, useEffect} from "react";
import {Table, Button, Modal, TextInput} from "flowbite-react";
import EditRecipeForm from "./EditRecipeForm";
import {Recipe} from "../dto/Recipe";
import {RecipeProduct} from "../dto/RecipeProduct";
import {RecipeService} from "../services/recipe/RecipeService";
import {NutrientsUtil} from "../util/NutrientsUtil";

const RecipeList: React.FC = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentRecipe, setCurrentRecipe] = useState<Recipe | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const recipeService = new RecipeService();

  useEffect(() => {
    fetchRecipes();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchTerm.trim() === "") {
        fetchRecipes();
      } else {
        searchRecipes(searchTerm);
      }
    }, 300);
    return () => clearTimeout(timer);

  }, [searchTerm]);

  const searchRecipes = async (searchTerm: string) => {
    try {
      let paginatedProducts = await recipeService.searchRecipeByName(searchTerm);
      setRecipes(paginatedProducts.items);
    } catch (error) {
      console.error("Error searching products: ", error);
    }
  }

  const openEditModal = (recipe: Recipe) => {
    setCurrentRecipe(recipe);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentRecipe(null);
    fetchRecipes();
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const fetchRecipes = async () => {
    const paginatedRecipes = await recipeService.getAllRecipes(1, 50);
    let recipes = paginatedRecipes.items;
    setRecipes(recipes);
  };

  const sumOfNutrients = (recipeProducts: RecipeProduct[]) => {
    return recipeProducts.reduce(
        (acc, recipeProduct) => {
          acc.proteins += recipeProduct.product.proteins;
          acc.carbohydrates += recipeProduct.product.carbohydrates;
          acc.fats += recipeProduct.product.fats;
          acc.calories += NutrientsUtil.countCalories(recipeProduct)
          return acc;
        },
        {proteins: 0, carbohydrates: 0, fats: 0, calories: 0}
    );
  };

  const formatNutrients = (nutrients: any) => {
    return {
      proteins: parseFloat(nutrients.proteins.toFixed(1)),
      carbohydrates: parseFloat(nutrients.carbohydrates.toFixed(1)),
      fats: parseFloat(nutrients.fats.toFixed(1)),
      calories: parseFloat(nutrients.calories.toFixed(1)),
    };
  };

  return (
      <div>
        <div className="flex flex-row justify-between">
          <div className="ml-2 mb-2">
            <TextInput
                id="search"
                type="text"
                placeholder="Search recipes..."
                sizing="md"
                value={searchTerm}
                onChange={handleSearchChange}
            />
          </div>
          <div className="mr-2 mb-2">
            <Button className="" href="/add-recipe">
              Add recipe
            </Button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <Table hoverable>
            <Table.Head>
              <Table.HeadCell>Recipe name</Table.HeadCell>
              <Table.HeadCell>Proteins</Table.HeadCell>
              <Table.HeadCell>Carbohydrates</Table.HeadCell>
              <Table.HeadCell>Fats</Table.HeadCell>
              <Table.HeadCell>Calories</Table.HeadCell>
            </Table.Head>
            <Table.Body className="divide-y">
              {recipes.map((recipe) => {
                const nutrients = formatNutrients(sumOfNutrients(recipe.products));

                return (
                    <Table.Row key={recipe.id}
                               onClick={() => openEditModal(recipe)}
                    >
                      <Table.Cell>{recipe.name}</Table.Cell>
                      <Table.Cell>{nutrients.proteins}</Table.Cell>
                      <Table.Cell>{nutrients.carbohydrates}</Table.Cell>
                      <Table.Cell>{nutrients.fats}</Table.Cell>
                      <Table.Cell>{nutrients.calories}</Table.Cell>
                    </Table.Row>
                );
              })}
            </Table.Body>
          </Table>
        </div>
        {isModalOpen && currentRecipe && (
            <>
              <Button onClick={() => setIsModalOpen(false)}>Toggle modal</Button>
              <Modal show={isModalOpen} onClose={closeModal} title="Edit Product">
                <Modal.Header>Edit recipe</Modal.Header>
                <Modal.Body>
                  <EditRecipeForm
                      onClose={closeModal}
                      recipe={{
                        id: currentRecipe.id,
                        name: currentRecipe.name,
                        description: String(currentRecipe.description),
                        servings: currentRecipe.servings,
                        products: currentRecipe.products,
                      }}
                  />
                </Modal.Body>
              </Modal>
            </>
        )}
      </div>
  );
};

export default RecipeList;
