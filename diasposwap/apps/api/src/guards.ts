import { type CanActivate, type ExecutionContext, ForbiddenException, Inject, Injectable, SetMetadata, UnauthorizedException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import type { Request } from 'express';
import { hmacHex } from '@diasposwap/settlement-engine';
import { type ApiConfig, CONFIG } from './simulator.provider';

export const ROLES = 'roles';
export const Roles = (...roles: ('ops' | 'compliance')[]) => SetMetadata(ROLES, roles);

/**
 * DEMO authentication only. Users are identified by the X-Demo-User header; admins by X-Admin-Key.
 * Production needs real authentication (OIDC/password + MFA, short-lived tokens, device binding).
 */
@Injectable()
export class AdminGuard implements CanActivate {
  constructor(@Inject(CONFIG) private readonly cfg: ApiConfig, @Inject(Reflector) private readonly reflector: Reflector) {}
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest<Request & { adminRole?: string; adminKeyId?: string }>();
    const key = req.header('x-admin-key');
    const role = key ? this.cfg.adminKeys[key] : undefined;
    if (!role) throw new UnauthorizedException('Admin key required');
    const allowed = this.reflector.get<string[] | undefined>(ROLES, ctx.getHandler());
    if (allowed && !allowed.includes(role)) throw new ForbiddenException(`Role ${role} not allowed`);
    req.adminRole = role;
    // stable, non-reversible officer identity derived from the FULL key (never a key prefix)
    req.adminKeyId = `${role}:${hmacHex('officer-id', key!).slice(0, 12)}`;
    return true;
  }
}

@Injectable()
export class UserGuard implements CanActivate {
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest<Request>();
    if (!req.header('x-demo-user')) throw new UnauthorizedException('X-Demo-User header required (demo auth)');
    return true;
  }
}
