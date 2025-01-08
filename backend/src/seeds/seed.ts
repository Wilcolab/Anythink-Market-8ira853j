import 'reflect-metadata';
import { DataSource } from 'typeorm';
import * as dotenv from 'dotenv';
import { User } from '../entities/user.entity';
import { Product } from '../entities/product.entity';
import { seedProducts } from './product-seed';
import { seedUsers } from './user-seed';

dotenv.config();

const dataSource = new DataSource({
  type: 'postgres',
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  username: process.env.DB_USERNAME || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
  database: process.env.DB_NAME || 'riskistore',
  entities: [User, Product],
  synchronize: false,
  logging: true,
});

async function runSeed() {
  try {
    await dataSource.initialize();
    await seedProducts(dataSource);
    await seedUsers(dataSource);
    await dataSource.destroy();
  } catch (error) {
    console.error('Error during seeding:', error);
    process.exit(1);
  }
}

runSeed();
