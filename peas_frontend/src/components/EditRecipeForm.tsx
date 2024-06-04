import React, {useState} from "react";
import {Button, Label, TextInput} from "flowbite-react";
import {Recipe} from "../dto/Recipe";
import {RecipeService} from "../services/recipe/RecipeService";

interface EditRecipeForm {
  recipe: Recipe;
  onClose: () => void;
}

const EditRecipeForm: React.FC<EditRecipeForm> = ({recipe, onClose}) => {
  const [id, setId] = useState(recipe.id);
  const [name, setRecipeName] = useState(recipe.name);
  const [description, setDescription] = useState(recipe.description);
  const [servings, setServings] = useState(recipe.servings);
  const [products, setProducts] = useState(recipe.products);
  const recipeService = new RecipeService();

  const handleDelete = async () => {
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const recipeData: Recipe = {
      id,
      name,
      description,
      servings,
      products,
    };

    let recipeResponse = await recipeService.updateRecipe(
        recipeData,
        recipe.id
    );
    onClose();
  };

  return (
      <div className="relative flex justify-center items-center min-h-screen">
        <form className="flex w-full max-w-lg flex-col gap-4" onSubmit={handleSubmit}>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="name" value="Recipe name"/>
            </div>
            <TextInput
                id="name"
                type="text"
                sizing="md"
                required
                value={name}
                onChange={(e) => setRecipeName(e.target.value)}
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="description" value="description"/>
            </div>
            <TextInput
                id="description"
                type="text"
                sizing="sm"
                required
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="servings" value="servings"/>
            </div>
            <TextInput
                id="servings"
                type="number"
                sizing="sm"
                required
                value={servings}
                onChange={(e) => setServings(Number(e.target.value))}
            />
          </div>
          <Button color="success" type="submit">
            Submit
          </Button>
          <Button color="failure" type="submit" onClick={handleDelete}>
            Delete
          </Button>
        </form>
      </div>
  );
};

export default EditRecipeForm;
