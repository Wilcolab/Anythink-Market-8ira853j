import { DataSource } from 'typeorm';
import { User } from '../entities/user.entity';
import { hash } from 'bcrypt';

const createUserSeedData = async () => {
  const defaultPassword = await hash('password123', 10);
  
  return [
    {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
      password: defaultPassword,
    },
    {
      firstName: 'Jane',
      lastName: 'Smith',
      email: 'jane.smith@example.com',
      password: defaultPassword,
    },
    {
      firstName: 'Admin',
      lastName: 'User',
      email: 'admin@example.com',
      password: defaultPassword,
    }
  ];
};

export async function seedUsers(dataSource: DataSource) {
  const userRepository = dataSource.getRepository(User);
  
  try {
    // Clear existing users
    await userRepository.clear();
    
    // Create and save seed users
    const seedData = await createUserSeedData();
    await userRepository.save(seedData);
    
    console.log('Successfully seeded users!');
  } catch (error) {
    console.error('Error seeding users:', error);
  }
}
