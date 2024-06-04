import React, {useState} from "react";
import {Button, Label, TextInput, Toast} from "flowbite-react";
import {HiCheckCircle, HiX} from "react-icons/hi";
import {ProductService} from "../services/product/ProductService";


interface AddProductFormProps {
  product?: {
    name?: string;
    proteins?: string;
    carbohydrates?: string;
    fats?: string;
    sodium?: string;
  };
}

const AddProductForm: React.FC<AddProductFormProps> = ({product}) => {
  const [name, setProductName] = useState(product?.name || '');
  const [proteins, setProtein] = useState(product?.proteins || '');
  const [carbohydrates, setCarbs] = useState(product?.carbohydrates || '');
  const [fats, setFats] = useState(product?.fats || '');
  const [sodium, setSodium] = useState(product?.sodium || '');
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const productService = new ProductService();


  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const productData = {
      name,
      proteins: parseFloat(proteins),
      carbohydrates: parseFloat(carbohydrates),
      fats: parseFloat(fats),
      sodium: parseFloat(sodium),
    };

    try {
      await productService.addProduct(productData);
    } catch (error) {
      setShowError(true);
      setTimeout(() => setShowError(false), 2000);
    }

    setProductName('');
    setProtein('');
    setCarbs('');
    setFats('');
    setSodium('');

    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 2000);
  };

  return (
      <div className="flex justify-center items-center min-h-screen flex-col">
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
                onChange={(e) => setProtein(e.target.value)}
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
                onChange={(e) => setCarbs(e.target.value)}
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
                onChange={(e) => setFats(e.target.value)}
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="sodium" value="Salt per 100g"/>
            </div>
            <TextInput
                id="sodium"
                type="text"
                sizing="sm"
                required
                value={sodium}
                onChange={(e) => setSodium(e.target.value)}
            />
          </div>
          <Button type="submit">Submit</Button>
        </form>
        {showSuccess && (
            <div className="pt-2">
              <Toast>
                <div
                    className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-green-100 text-green-500">
                  <HiCheckCircle className="h-5 w-5"/>
                </div>
                <div className="ml-3 text-sm font-normal">Product added successfully!</div>
              </Toast>
            </div>
        )}
        {showError && (
            <div className="pt-2">
              <Toast>
                <div
                    className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-green-100 text-green-500">
                  <HiCheckCircle className="h-5 w-5"/>
                </div>
                <div className="ml-3 text-sm font-normal">{errorMsg}</div>
              </Toast>
            </div>
        )}
      </div>
  );
};

export default AddProductForm;
