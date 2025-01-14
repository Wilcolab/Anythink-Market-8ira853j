import { z } from 'zod';

export const ProductCategorySchema = z.enum([
  'Electronics', 
  'Clothing', 
  'Books', 
  'Home & Kitchen', 
  'Sports & Outdoors'
]);

export const CreateProductSchema = z.object({
  name: z.string().min(1, { message: "Product name is required" }),
  description: z.string().optional(),
  price: z.number().positive({ message: "Price must be a positive number" }),
  category: ProductCategorySchema,
  stockQuantity: z.number().int().nonnegative({ message: "Stock quantity must be a non-negative number" }),
  imageUrl: z.string().url().optional(),
});

export const UpdateProductSchema = CreateProductSchema.partial();

export type CreateProductDto = z.infer<typeof CreateProductSchema>;
export type UpdateProductDto = z.infer<typeof UpdateProductSchema>;
export type ProductCategoryDto = z.infer<typeof ProductCategorySchema>;
