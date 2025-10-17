-- Create supabase_admin role if not exists (safe even if it exists)
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'supabase_admin') THEN
      CREATE ROLE supabase_admin WITH SUPERUSER LOGIN CREATEDB CREATEROLE INHERIT REPLICATION BYPASSRLS;
   END IF;
END
$$;

-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
  doc_id SERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  embedding VECTOR(384),
  source_name TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
