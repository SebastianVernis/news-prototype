// src/middleware/auth.js — Autenticación y verificación de sesiones

// ============================================================
// checkAuth — Valida el token Bearer contra ADMIN_TOKEN o sesión KV
// ============================================================
export const checkAuth = async (c) => {
  const authHeader = c.req.header('Authorization') || '';
  const token = authHeader.replace('Bearer ', '').trim();
  const adminToken = c.env.ADMIN_TOKEN;

  if (!token) return false;

  // 1. Validar contra ADMIN_TOKEN maestro
  if (adminToken && token === adminToken) {
    return true;
  }

  // 2. Validar contra Sesiones en KV
  if (c.env.ARTICLES_KV) {
    try {
      const sessionData = await c.env.ARTICLES_KV.get(`session_${token}`);
      if (sessionData) {
        return true;
      }
    } catch (kvErr) {
      console.error(`[Auth] Error accediendo a KV: ${kvErr.message}`);
    }
  }

  // 3. Fallback de emergencia (si no hay secreto configurado)
  if (!adminToken) {
    return true;
  }

  console.warn(`[Auth] 401 - Token no reconocido: ${token.substring(0, 10)}...`);
  return false;
};

// ============================================================
// verifyPassword — Verifica contraseña contra hash almacenado
// En producción usar bcrypt o argon2
// ============================================================
export const verifyPassword = async (password, storedHash) => {
  const simpleHash = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(16);
  };
  return simpleHash(password) === storedHash;
};
