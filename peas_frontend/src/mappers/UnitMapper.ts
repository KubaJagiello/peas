import { Unit as ProductUnit } from "../dto/Unit";
import { Unit } from "../generated/Api";

export function mapToProductUnit(unit: Unit): ProductUnit {
    switch (unit) {
        case Unit.Gram:
            return ProductUnit.Gram;
        case Unit.Milliliter:
            return ProductUnit.Milliliter;
        default:
            throw new Error(`Unsupported unit: ${unit}`);
    }
}

export function mapToUnit(productUnit: ProductUnit): Unit {
    switch (productUnit) {
        case ProductUnit.Gram:
            return Unit.Gram;
        case ProductUnit.Milliliter:
            return Unit.Milliliter;
        default:
            throw new Error(`Unsupported unit: ${productUnit}`);
    }
}