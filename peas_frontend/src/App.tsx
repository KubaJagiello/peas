import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ProductList from "./components/ProductList";
import Menu from "./components/Menu";
import AddProductForm from "./components/AddProductForm";
import AddRecipeForm from "./components/AddRecipeForm";
import RecipeList from "./components/RecipeList";

const App: React.FC = () => {
  return (
    <Router>
      <Menu></Menu>
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/products" element={<ProductList />} />
        <Route path="/add-product" element={<AddProductForm />} />
        <Route path="/recipes" element={<RecipeList />} />
        <Route path="/add-recipe" element={<AddRecipeForm />} />
      </Routes>
    </Router>
  );
};

export default App;
