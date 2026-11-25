import 'reflect-metadata';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { configureApp } from './configure';

export async function bootstrap(port = Number(process.env.PORT ?? 3000)) {
  // rawBody: needed to verify webhook signatures over the exact bytes received
  const app = await NestFactory.create(AppModule, { rawBody: true, logger: ['error', 'warn', 'log'] });
  configureApp(app);
  await app.listen(port);
  return app;
}

if (process.argv[1] && /main\.ts$/.test(process.argv[1])) void bootstrap();
