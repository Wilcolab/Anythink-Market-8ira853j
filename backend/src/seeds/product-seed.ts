import { DataSource } from 'typeorm';
import { Product } from '../entities/product.entity';

const productSeedData = [
  // Electronics
  {
    name: 'Wireless Noise-Canceling Headphones',
    price: Number(249.99),
    description: 'Premium over-ear headphones with advanced noise-canceling technology, 40-hour battery life, and crystal-clear sound quality.',
    imageUrl: 'https://images.pexels.com/photos/1037992/pexels-photo-1037992.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: '4K Smart LED Television',
    price: Number(599.99),
    description: '65-inch Ultra HD Smart TV with HDR, Dolby Vision, and built-in streaming apps for an immersive viewing experience.',
    imageUrl: 'https://images.pexels.com/photos/1040160/pexels-photo-1040160.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Smartphone Pro Max',
    price: Number(1099.99),
    description: 'Latest flagship smartphone with triple-lens camera, 5G connectivity, and 256GB storage.',
    imageUrl: 'https://images.pexels.com/photos/5234774/pexels-photo-5234774.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Portable Bluetooth Speaker',
    price: Number(129.99),
    description: 'Waterproof wireless speaker with 360-degree sound, 12-hour battery life, and multiple color options.',
    imageUrl: 'https://images.pexels.com/photos/157534/pexels-photo-157534.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Wireless Charging Pad',
    price: Number(49.99),
    description: 'Fast-charging wireless pad compatible with multiple devices, with LED indicators and non-slip surface.',
    imageUrl: 'https://images.pexels.com/photos/1028674/pexels-photo-1028674.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },

  // Home & Kitchen
  {
    name: 'Stainless Steel Air Fryer',
    price: Number(129.99),
    description: '5.8-quart digital air fryer with touchscreen controls, multiple cooking presets, and dishwasher-safe parts.',
    imageUrl: 'https://images.pexels.com/photos/6378164/pexels-photo-6378164.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Coffee Maker with Grinder',
    price: Number(199.99),
    description: 'Integrated burr grinder, programmable timer, and brew strength control for the perfect morning coffee.',
    imageUrl: 'https://images.pexels.com/photos/4993062/pexels-photo-4993062.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Robot Vacuum Cleaner',
    price: Number(279.99),
    description: 'Smart robotic vacuum with mapping technology, app control, and automatic charging dock.',
    imageUrl: 'https://images.pexels.com/photos/38325/vacuum-cleaner-carpet-cleaner-housework-housekeeping-38325.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Instant Pot Multi-Cooker',
    price: Number(99.99),
    description: '7-in-1 programmable pressure cooker, slow cooker, rice cooker, steamer, sauté pan, yogurt maker, and warmer.',
    imageUrl: 'https://images.pexels.com/photos/30034091/pexels-photo-30034091.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Electric Kettle',
    price: Number(59.99),
    description: 'Quick-boil electric kettle with temperature control, auto-shutoff, and sleek stainless steel design.',
    imageUrl: 'https://images.pexels.com/photos/792615/pexels-photo-792615.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },

  // Fashion & Accessories
  {
    name: 'Leather Messenger Bag',
    price: Number(189.99),
    description: 'Genuine leather messenger bag with padded laptop compartment, multiple pockets, and adjustable strap.',
    imageUrl: 'https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Smartwatch Fitness Tracker',
    price: Number(179.99),
    description: 'Advanced fitness smartwatch with heart rate monitor, GPS tracking, sleep analysis, and smartphone notifications.',
    imageUrl: 'https://images.pexels.com/photos/267391/pexels-photo-267391.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Wireless Noise-Canceling Earbuds',
    price: Number(199.99),
    description: 'True wireless earbuds with active noise cancellation, touch controls, and 8-hour battery life.',
    imageUrl: 'https://images.pexels.com/photos/3780681/pexels-photo-3780681.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Designer Sunglasses',
    price: Number(249.99),
    description: 'Polarized sunglasses with UV protection, lightweight frame, and classic design.',
    imageUrl: 'https://images.pexels.com/photos/2651394/pexels-photo-2651394.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Leather Wallet',
    price: Number(89.99),
    description: 'Slim RFID-blocking leather wallet with multiple card slots and minimalist design.',
    imageUrl: 'https://images.pexels.com/photos/915915/pexels-photo-915915.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },

  // Sports & Outdoors
  {
    name: 'Yoga Mat Set',
    price: Number(69.99),
    description: 'Premium eco-friendly yoga mat with carrying strap, alignment markers, and extra thick cushioning.',
    imageUrl: 'https://images.pexels.com/photos/2394051/pexels-photo-2394051.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Fitness Resistance Bands',
    price: Number(29.99),
    description: 'Set of 5 resistance bands with different tension levels, ideal for home and gym workouts.',
    imageUrl: 'https://images.pexels.com/photos/863977/pexels-photo-863977.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Hiking Backpack',
    price: Number(129.99),
    description: 'Waterproof 40L hiking backpack with multiple compartments, hydration bladder compatibility, and ergonomic design.',
    imageUrl: 'https://images.pexels.com/photos/3731256/pexels-photo-3731256.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Wireless Bluetooth Earphones',
    price: Number(79.99),
    description: 'Sports wireless earphones with secure ear hooks, sweatproof design, and 10-hour battery life.',
    imageUrl: 'https://images.pexels.com/photos/583843/pexels-photo-583843.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  },
  {
    name: 'Foam Roller',
    price: Number(39.99),
    description: 'High-density foam roller for muscle recovery, deep tissue massage, and physical therapy.',
    imageUrl: 'https://images.pexels.com/photos/4587697/pexels-photo-4587697.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
  }
];

export async function seedProducts(dataSource: DataSource) {
  const productRepository = dataSource.getRepository(Product);
  
  try {
    // Clear existing products
    await productRepository.clear();
    await productRepository.save(productSeedData);
    console.log('Successfully seeded products!');
  } catch (error) {
    console.error('Error seeding products:', error);
  }
}
