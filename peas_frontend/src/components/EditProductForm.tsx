import React, {useState} from "react";
import {Button, Label, TextInput} from "flowbite-react";
import {Product} from "../dto/Product";
import {ProductService} from "../services/product/ProductService";

interface EditProductFormProps {
  product: Product;
  onClose: () => void;
}

const EditProductForm: React.FC<EditProductFormProps> = ({product, onClose}) => {
  const [id, setId] = useState(product.id);
  const [name, setProductName] = useState(product.name);
  const [proteins, setProtein] = useState(product.proteins);
  const [carbohydrates, setCarbs] = useState(product.carbohydrates);
  const [sodium, setSodium] = useState(product.sodium);
  const [fats, setFats] = useState(product.fats);
  const productService = new ProductService();

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this product?")) {
      return;
    }

    try {
      await productService.deleteProduct(String(product.id));
      onClose();
    } catch (error) {
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const productData = {
      id,
      name,
      proteins: proteins,
      carbohydrates: carbohydrates,
      fats: fats,
      sodium: sodium
    };

    try {
      await productService.updateProduct(String(id), productData);
      onClose();
    } catch (error) {
      console.error("Failed to update product:", error);
    }
  };

  return (
      <div className="relative flex justify-center items-center min-h-screen">
        <form className="flex w-full max-w-lg flex-col gap-4" onSubmit={handleSubmit}>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="name" value="Product name"/>
            </div>
            <TextInput
                id="name"
                type="text"
                sizing="md"
                required
                value={name}
                onChange={(e) => setProductName(e.target.value)}
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="protein" value="Proteins per 100g"/>
            </div>
            <TextInput
                id="protein"
                type="text"
                sizing="sm"
                required
                value={proteins}
                onChange={(e) => setProtein(parseFloat(e.target.value))}
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="carbohydrates" value="Carbohydrates per 100g"/>
            </div>
            <TextInput
                id="carbohydrates"
                type="text"
                sizing="sm"
                required
                value={carbohydrates}
                onChange={(e) => setCarbs(parseFloat(e.target.value))}
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="fats" value="Fats per 100g"/>
            </div>
            <TextInput
                id="fats"
                type="text"
                sizing="sm"
                required
                value={fats}
                onChange={(e) => setFats(parseFloat(e.target.value))}
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

export default EditProductForm;
