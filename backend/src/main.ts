import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors({
    origin: true, // This allows all origins in development
    credentials: true,
  });
  app.setGlobalPrefix('api');
  await app.listen(3000, '0.0.0.0'); // Listen on all network interfaces
}
bootstrap();
