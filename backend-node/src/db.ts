import { Pool } from 'pg';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Load .env from root directory
dotenv.config({ path: path.join(__dirname, '../../..', '.env') });

export const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
}); 