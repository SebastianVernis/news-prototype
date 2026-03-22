// src/routes/auth.js — Rutas de autenticación y gestión de usuarios

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';

const auth = new Hono();

// ── Crear nuevo usuario (solo admin) ────────────────────────
auth.post('/users', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const { username, email, role } = await c.req.json();
    if (!username) return c.json({ error: 'Nombre de usuario requerido' }, 400);

    const existing = await c.env.DB.prepare(
      'SELECT ID FROM USUARIOS WHERE NOMBRE = ?'
    ).bind(username).first();
    if (existing) return c.json({ error: 'El usuario ya existe' }, 409);

    const userId = crypto.randomUUID();
    await c.env.DB.prepare(
      'INSERT INTO USUARIOS (ID, NOMBRE, EMAIL, ROL, ACTIVO) VALUES (?, ?, ?, ?, 1)'
    ).bind(userId, username, email || '', role || 'editor').run();

    return c.json({ success: true, id: userId, username });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── Listar usuarios (solo admin) ─────────────────────────────
auth.get('/users', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const res = await c.env.DB.prepare(
      'SELECT ID, NOMBRE, EMAIL, ROL, ACTIVO FROM USUARIOS ORDER BY NOMBRE'
    ).all();
    return c.json(res.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── Generar token temporal para configuración de contraseña ──
auth.post('/generate-password-token', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Token de administrador inválido' }, 401);
  try {
    const { username } = await c.req.json();
    if (!username) return c.json({ error: 'Usuario requerido' }, 400);

    const user = await c.env.DB.prepare(
      'SELECT ID FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
    ).bind(username).first();
    if (!user) return c.json({ error: 'Usuario no encontrado o inactivo' }, 404);

    const tempToken  = crypto.randomUUID();
    const expiresAt  = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();

    // Crear tabla si no existe
    try {
      await c.env.DB.prepare(`
        CREATE TABLE IF NOT EXISTS PASSWORD_RESET_TOKENS (
          ID TEXT PRIMARY KEY,
          USER_ID TEXT NOT NULL,
          TOKEN TEXT UNIQUE NOT NULL,
          EXPIRES_AT TEXT NOT NULL,
          USED INTEGER DEFAULT 0,
          CREATED_AT TEXT NOT NULL
        )
      `).run();
    } catch (e) {
      // Tabla ya existe - esperado
    }

    await c.env.DB.prepare(`
      INSERT INTO PASSWORD_RESET_TOKENS (ID, USER_ID, TOKEN, EXPIRES_AT, CREATED_AT)
      VALUES (?, ?, ?, ?, ?)
    `).bind(crypto.randomUUID(), user.ID, tempToken, expiresAt, new Date().toISOString()).run();

    const baseUrl  = c.env.SITE_URL || 'https://cms-admin-nuevos.pages.dev';
    const setupUrl = `${baseUrl}/setup-password.html?user=${encodeURIComponent(username)}&t=${tempToken}`;

    return c.json({
      success: true,
      token: tempToken,
      expiresAt,
      setupUrl,
      message: 'Token generado exitosamente. Válido por 24 horas.',
    });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── Validar token de configuración de contraseña ─────────────
auth.get('/validate-password-token', async (c) => {
  try {
    const username = c.req.query('user');
    const token    = c.req.query('t');

    if (!username || !token) {
      return c.json({ valid: false, error: 'Parámetros requeridos' }, 400);
    }

    const user = await c.env.DB.prepare(
      'SELECT ID FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
    ).bind(username).first();
    if (!user) return c.json({ valid: false, error: 'Usuario no encontrado' }, 404);

    const tokenRecord = await c.env.DB.prepare(`
      SELECT * FROM PASSWORD_RESET_TOKENS
      WHERE TOKEN = ? AND USER_ID = ? AND USED = 0 AND EXPIRES_AT > ?
    `).bind(token, user.ID, new Date().toISOString()).first();

    if (!tokenRecord) {
      return c.json({ valid: false, error: 'Token inválido o expirado' }, 404);
    }

    return c.json({ valid: true, username });
  } catch (e) {
    return c.json({ valid: false, error: e.message }, 500);
  }
});

// ── Establecer contraseña para un usuario ────────────────────
auth.post('/setup-password', async (c) => {
  const token    = (c.req.header('Authorization') || '').replace('Bearer ', '').trim();
  const adminToken = c.env.ADMIN_TOKEN;

  let isAdmin  = false;
  let username = null;

  // 1. Verificar si es ADMIN_TOKEN
  if (adminToken && token === adminToken) {
    isAdmin  = true;
    const body = await c.req.json();
    username = body.username;
  } else {
    // 2. Verificar si es token temporal
    try {
      const body = await c.req.json();
      username = body.username;

      if (!username) return c.json({ error: 'Usuario requerido' }, 400);

      const user = await c.env.DB.prepare(
        'SELECT ID FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
      ).bind(username).first();

      if (!user) return c.json({ error: 'Usuario no encontrado o inactivo' }, 404);

      const tokenRecord = await c.env.DB.prepare(`
        SELECT * FROM PASSWORD_RESET_TOKENS
        WHERE TOKEN = ? AND USER_ID = ? AND USED = 0 AND EXPIRES_AT > ?
      `).bind(token, user.ID, new Date().toISOString()).first();

      if (!tokenRecord) return c.json({ error: 'Token temporal inválido o expirado' }, 401);

      await c.env.DB.prepare(
        'UPDATE PASSWORD_RESET_TOKENS SET USED = 1 WHERE TOKEN = ?'
      ).bind(token).run();

      isAdmin = true;
    } catch (_) {
      return c.json({ error: 'Token inválido' }, 401);
    }
  }

  if (!isAdmin) return c.json({ error: 'No autorizado' }, 401);

  try {
    const { username: bodyUsername, passwordHash } = await c.req.json();
    const finalUsername = username || bodyUsername;

    if (!finalUsername || !passwordHash) {
      return c.json({ error: 'Usuario y hash de contraseña requeridos' }, 400);
    }

    const user = await c.env.DB.prepare(
      'SELECT ID FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
    ).bind(finalUsername).first();
    if (!user) return c.json({ error: 'Usuario no encontrado o inactivo' }, 404);

    try {
      await c.env.DB.prepare('ALTER TABLE USUARIOS ADD COLUMN PASSWORD_HASH TEXT').run();
    } catch (e) {
      // Columna ya existe - esperado
    }

    await c.env.DB.prepare(
      'UPDATE USUARIOS SET PASSWORD_HASH = ? WHERE NOMBRE = ?'
    ).bind(passwordHash, finalUsername).run();

    return c.json({ success: true, message: 'Contraseña configurada correctamente' });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── Login de usuario ─────────────────────────────────────────
auth.post('/login', async (c) => {
  try {
    const { username, password } = await c.req.json();

    if (!username || !password) {
      return c.json({ error: 'Usuario y contraseña requeridos' }, 400);
    }

    const user = await c.env.DB.prepare(
      'SELECT * FROM USUARIOS WHERE (NOMBRE = ? OR EMAIL = ?) AND ACTIVO = 1'
    ).bind(username, username).first();

    if (!user) return c.json({ error: 'Usuario o contraseña incorrectos' }, 401);

    // Generar hash SHA-256 de la contraseña ingresada
    const inputHash = await crypto.subtle
      .digest('SHA-256', new TextEncoder().encode(password))
      .then((buf) =>
        Array.from(new Uint8Array(buf))
          .map((b) => b.toString(16).padStart(2, '0'))
          .join('')
      );

    let isValid = false;

    if (user.PASSWORD_HASH) {
      isValid = inputHash === user.PASSWORD_HASH;
    } else if (c.env.USER_PASSWORD_HASH) {
      isValid = inputHash === c.env.USER_PASSWORD_HASH;
    } else {
      isValid = true; // Sin hash configurado: acceso libre (solo desarrollo)
    }

    if (!isValid) return c.json({ error: 'Usuario o contraseña incorrectos' }, 401);

    const token = crypto.randomUUID();

    if (c.env.ARTICLES_KV) {
      await c.env.ARTICLES_KV.put(
        `session_${token}`,
        JSON.stringify({
          userId:    user.ID,
          name:      user.NOMBRE,
          role:      user.ROL,
          loginTime: new Date().toISOString(),
        }),
        { expirationTtl: 86400 } // 24 horas
      );
    }

    return c.json({
      success: true,
      token,
      user: {
        id:    user.ID,
        name:  user.NOMBRE,
        email: user.EMAIL,
        role:  user.ROL,
      },
    });
  } catch (e) {
    console.error('Error en login:', e);
    return c.json({ error: e.message }, 500);
  }
});

export default auth;
