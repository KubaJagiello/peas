import React, {useState, useEffect} from "react";
import {Table, Button, Modal, TextInput} from "flowbite-react";
import EditProductForm from "./EditProductForm";
import {ProductService} from "../services/product/ProductService";
import {NutrientsUtil} from "../util/NutrientsUtil";
import {Product} from "../dto/Product";

interface ListProduct {
  id: number;
  name: string;
  proteins: number;
  carbohydrates: number;
  fats: number;
  salt: number;
  calories: number;
}

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<ListProduct[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentProduct, setCurrentProduct] = useState<ListProduct | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const productService = new ProductService();

  useEffect(() => {
    fetchProducts();
  }, []);

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

  const fetchProducts = async () => {
    try {
      const paginatedProducts = await productService.getAllProducts();
      let products = paginatedProducts.items;

      let listProducts = products.map((product) => ({
        ...product,
        calories: NutrientsUtil.countCalories(product)
      }));
      setProducts(listProducts);

    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const searchProducts = async (term: string) => {
    try {
      let paginatedProducts = await productService.searchProductByName(term);
      setProducts(convertToListProducts(paginatedProducts.items));
    } catch (error) {
      console.error("Error searching products: ", error);
    }
  }

  const openEditModal = (product: ListProduct) => {
    setCurrentProduct(product);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentProduct(null);
    fetchProducts();
  };

  const handleSearchChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  function convertToListProducts(products: Product[]): ListProduct[] {
    return products.map((product) => ({
      ...product, calories: NutrientsUtil.countCalories(product)
    }));
  }

  return (
      <div>
        <div className="flex flex-row justify-between">
          <div className="ml-2 mb-2">
            <TextInput
                id="search"
                type="text"
                placeholder="Search products..."
                sizing="md"
                value={searchTerm}
                onChange={handleSearchChange}
            />
          </div>
          <div className="mr-2 mb-2">
            <Button className="" href="/add-product">
              Add product
            </Button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <Table hoverable>
            <Table.Head>
              <Table.HeadCell>Product name</Table.HeadCell>
              <Table.HeadCell>Proteins</Table.HeadCell>
              <Table.HeadCell>Carbohydrates</Table.HeadCell>
              <Table.HeadCell>Fats</Table.HeadCell>
              <Table.HeadCell>Salt</Table.HeadCell>
              <Table.HeadCell>Calories</Table.HeadCell>
            </Table.Head>
            <Table.Body className="divide-y">
              {products.map((product) => (
                  <Table.Row
                      className="bg-white dark:border-gray-700 dark:bg-gray-800 cursor-pointer"
                      key={product.id}
                      onClick={() => openEditModal(product)}
                  >
                    <Table.Cell>{product.name}</Table.Cell>
                    <Table.Cell>{product.proteins}</Table.Cell>
                    <Table.Cell>{product.carbohydrates}</Table.Cell>
                    <Table.Cell>{product.fats}</Table.Cell>
                    <Table.Cell>{product.salt}</Table.Cell>
                    <Table.Cell>{NutrientsUtil.countCalories(product)}</Table.Cell>
                  </Table.Row>
              ))}
            </Table.Body>
          </Table>
        </div>

        {isModalOpen && currentProduct && (
            <>
              <Button onClick={() => setIsModalOpen(false)}>Toggle modal</Button>
              <Modal show={isModalOpen} onClose={closeModal} title="Edit Product">
                <Modal.Header>Edit product</Modal.Header>
                <Modal.Body>
                  <EditProductForm
                      onClose={closeModal}
                      product={{
                        id: currentProduct.id,
                        name: currentProduct.name,
                        proteins: currentProduct.proteins,
                        fats: currentProduct.fats,
                        carbohydrates: currentProduct.carbohydrates,
                        salt: currentProduct.salt
                      }}
                  />
                </Modal.Body>
              </Modal>
            </>
        )}
      </div>
  );
};

export default ProductList;
