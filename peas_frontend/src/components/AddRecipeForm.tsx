import React, {useState, useEffect, useRef} from "react";
import {Button, Label, TextInput, Toast, Select} from "flowbite-react";
import {HiCheckCircle, HiX} from "react-icons/hi";
import {Unit} from "../dto/Unit";
import {RecipeProduct} from "../dto/RecipeProduct";
import {Product} from "../dto/Product";
import {Recipe} from "../dto/Recipe";
import {RecipeService} from "../services/recipe/RecipeService";
import {ProductService} from "../services/product/ProductService";


interface AddRecipeFormProps {
  recipe?: Recipe;
  onClose?: () => void;
}

const AddRecipeForm: React.FC<AddRecipeFormProps> = ({recipe, onClose}) => {
  const [id, setId] = useState(recipe?.id || "");
  const [name, setRecipeName] = useState(recipe?.name || "");
  const [description, setDescription] = useState(recipe?.description || "");
  const [servings, setServings] = useState(recipe?.servings || 1);
  const [products, setProducts] = useState<RecipeProduct[]>(recipe?.products || []);
  const [availableProducts, setAvailableProducts] = useState<Product[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<number | undefined>(undefined);
  const [quantity, setQuantity] = useState<number>(1);
  const [unit, setUnit] = useState<Unit>(Unit.Gram);
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const recipeService = new RecipeService();
  const productService = new ProductService();

  interface ListProduct {
    id: number;
    name: string;
    proteins: number;
    carbohydrates: number;
    fats: number;
    salt: number;
    calories: number;
  }

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    let paginatedProducts = await productService.getAllProducts();
    let products = paginatedProducts.items;
    setAvailableProducts(products);
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchTerm.trim() === "") {
        fetchProducts();
      } else {
        searchProducts(searchTerm);
      }
    }, 300);
    return () => clearTimeout(timer);

  }, [searchTerm]);

  const searchProducts = async (term: string) => {
    try {
      let paginatedProducts = await productService.searchProductByName(term);
      setAvailableProducts(paginatedProducts.items);
    } catch (error) {
      console.error("Error searching products: ", error);
    }
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    console.log({
          name: name,
          description: description,
          servings: servings,
          products: products
        }
    );

    try {
      await recipeService.addRecipe({
        name: name,
        description: description,
        servings: servings,
        products: products
      });
    } catch (error) {
      setShowError(true);
      setTimeout(() => setShowError(false), 2000);
      throw new Error("Something went wrong");
    }

    setRecipeName("");
    setDescription("");
    setServings(1);
    setProducts([]);

    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 2000);
  };


  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const filteredProducts = availableProducts.filter((product) =>
      product.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleProductSelect = (productId: number) => {
    const product = availableProducts.find((p) => p.id === productId);
    if (product) {
      setProducts([...products,
        {
          quantity, unit, product
        }
      ]);
      setSearchTerm("");
    }
  };

  const handleQuantityChange = (index: number, value: number) => {
    const updatedProducts = [...products];
    updatedProducts[index].quantity = value;
    setProducts(updatedProducts);
  };

  const handleUnitChange = (index: number, value: Unit) => {
    const updatedProducts = [...products];
    updatedProducts[index].unit = value;
    setProducts(updatedProducts);
  };

  return (
      <div className="flex justify-center items-center min-h-screen flex-col">
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
              <Label htmlFor="description" value="Description"/>
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
              <Label htmlFor="servings" value="Servings"/>
            </div>
            <TextInput
                id="servings"
                type="number"
                sizing="sm"
                required
                value={servings}
                onChange={(e) => setServings(parseInt(e.target.value))}
            />
          </div>
          <div className="mb-4 relative">
            {" "}
            {}
            <div className="mb-2 block">
              <Label htmlFor="product" value="Add Product"/>
            </div>
            <div className="flex items-center gap-2 mt-2">
              <TextInput
                  id="search"
                  type="text"
                  placeholder="Search products..."
                  sizing="md"
                  value={searchTerm}
                  onChange={handleSearchChange}
                  autoComplete="off"
              />
            </div>
            {}
            {searchTerm.length > 0 && filteredProducts.length > 0 && (
                <div
                    className="absolute z-10 w-full bg-white border border-gray-300 rounded-md shadow-md max-h-60 overflow-auto mt-1">
                  <ul>
                    {filteredProducts.slice(0, 5).map((product) => (
                        <li
                            key={product.id}
                            className={`cursor-pointer px-4 py-2 hover:bg-gray-100 ${
                                selectedProductId === product.id ? "bg-blue-100" : ""
                            }`} // If selected, apply blue background and disable hover effect
                            onClick={() => handleProductSelect(product.id)}
                        >
                          {product.name}
                        </li>
                    ))}
                  </ul>
                </div>
            )}
          </div>
          <div className="mt-4">
            <table className="w-full text-left border-collapse">
              <thead>
              <tr>
                <th className="border-b p-2">Product</th>
                <th className="border-b p-2">Quantity</th>
                <th className="border-b p-2">Unit</th>
              </tr>
              </thead>
              <tbody>
              {products.map((rp, index) => (
                  <tr key={index}>
                    <td className="border-b p-2">{rp.product.name}</td>
                    <td
                        className="border-b p-2 cursor-pointer"
                        onClick={() => setEditingIndex(index)}
                    >
                      {editingIndex === index ? (
                          <TextInput
                              type="number"
                              value={rp.quantity}
                              onChange={(e) => handleQuantityChange(index, parseInt(e.target.value))}
                          />
                      ) : (
                          rp.quantity
                      )}
                    </td>
                    <td
                        className="border-b p-2 cursor-pointer"
                        onClick={() => setEditingIndex(index)}
                    >
                      {editingIndex === index ? (
                          <Select
                              value={rp.unit}
                              onChange={(e) => handleUnitChange(index, e.target.value as Unit)}
                          >
                            <option value={Unit.Gram}>Grams</option>
                            <option value={Unit.Milliliter}>Milliliters</option>
                          </Select>
                      ) : (
                          rp.unit
                      )}
                    </td>
                  </tr>
              ))}
              </tbody>
              {/* <tbody>
              {products.map((rp, index) => (
                <tr key={index}>
                  <td className="border-b p-2">{rp.product.name}</td>
                  <td className="border-b p-2">{rp.quantity}</td>
                  <td className="border-b p-2">{rp.unit}</td>
                </tr>
              ))}
            </tbody> */}
            </table>
          </div>
          <Button type="submit" className="mt-4">
            Submit
          </Button>
        </form>
        {showSuccess && (
            <div className="pt-2">
              <Toast>
                <div
                    className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-green-100 text-green-500">
                  <HiCheckCircle className="h-5 w-5"/>
                </div>
                <div className="ml-3 text-sm font-normal">Recipe added successfully!</div>
              </Toast>
            </div>
        )}
        {showError && (
            <div className="pt-2">
              <Toast>
                <div
                    className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-red-100 text-red-500">
                  <HiX className="h-5 w-5"/>
                </div>
                <div className="ml-3 text-sm font-normal">{errorMsg}</div>
              </Toast>
            </div>
        )}
      </div>
  );
};

export default AddRecipeForm;
