export interface Product {
    id: number;
    name: string;
    proteins: number;
    fats: number;
    carbohydrates: number;
    sodium: number;
}

export interface AddProduct {
    name: string;
    proteins: number;
    fats: number;
    carbohydrates: number;
    sodium: number;
}
