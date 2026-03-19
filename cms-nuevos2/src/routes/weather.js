// src/routes/weather.js — Datos del clima (OpenWeatherMap)

import { Hono } from 'hono';

const weather = new Hono();

// ── GET /weather — Temperatura y condición actual ────────────
weather.get('/', async (c) => {
  try {
    const apiKey = c.env.OPENWEATHER_API_KEY;

    if (!apiKey) {
      // Sin API key: valores por defecto realistas para CDMX
      return c.json({
        city:        'CDMX',
        temp:        24,
        icon:        '01d',
        condition:   'Despejado',
        description: 'cielo despejado',
        humidity:    30,
        wind:        12,
      });
    }

    // Parámetros opcionales de ubicación (por defecto: Ciudad de México)
    const lat   = c.req.query('lat') || '19.4326';
    const lon   = c.req.query('lon') || '-99.1332';
    const units = 'metric'; // Celsius

    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=${units}&appid=${apiKey}&lang=es`;
    const res = await fetch(url);

    if (!res.ok) {
      console.error(`OpenWeather HTTP ${res.status}`);
      return c.json({ city: 'CDMX', temp: 22, icon: '01d', condition: 'Clear' });
    }

    const data = await res.json();
    return c.json({
      city:        data.name                       || 'CDMX',
      temp:        Math.round(data.main?.temp ?? 22),
      icon:        data.weather?.[0]?.icon         || '01d',
      condition:   data.weather?.[0]?.main         || 'Clear',
      description: data.weather?.[0]?.description  || '',
      humidity:    data.main?.humidity             || null,
      wind:        data.wind?.speed                || null,
    });
  } catch (e) {
    console.error('Weather API error:', e.message);
    return c.json({ city: 'CDMX', temp: 22, icon: '01d', condition: 'Clear' });
  }
});

export default weather;
