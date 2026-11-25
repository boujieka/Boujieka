import { Module } from '@nestjs/common';
import { AdminController, DemoController, PublicController, TransferController, WebhookController } from './controllers';
import { AdminGuard, UserGuard } from './guards';
import { CONFIG, SIMULATOR, createSimulator, loadConfig, type ApiConfig } from './simulator.provider';

@Module({
  controllers: [PublicController, TransferController, WebhookController, AdminController, DemoController],
  providers: [
    { provide: CONFIG, useFactory: () => loadConfig() },
    { provide: SIMULATOR, useFactory: (cfg: ApiConfig) => createSimulator(cfg), inject: [CONFIG] },
    AdminGuard, UserGuard,
  ],
})
export class AppModule {}
