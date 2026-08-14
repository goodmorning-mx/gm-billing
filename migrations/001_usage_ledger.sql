CREATE TABLE IF NOT EXISTS gm_usage (
  id uuid PRIMARY KEY,
  product_id text NOT NULL,
  organization_id text NOT NULL,
  user_id text NOT NULL,
  provider text NOT NULL,
  model text NOT NULL,
  input_tokens integer NOT NULL CHECK (input_tokens >= 0),
  output_tokens integer NOT NULL CHECK (output_tokens >= 0),
  cached_tokens integer NOT NULL DEFAULT 0 CHECK (cached_tokens >= 0),
  request_id text,
  created_at timestamptz NOT NULL DEFAULT now(),
  provider_cost numeric(18,8) NOT NULL,
  goodmorning_charge numeric(18,8) NOT NULL
);
CREATE INDEX IF NOT EXISTS gm_usage_org_created_idx ON gm_usage (organization_id, created_at);
CREATE TABLE IF NOT EXISTS gm_billing_ledger (
  id uuid PRIMARY KEY,
  product_id text NOT NULL,
  organization_id text NOT NULL,
  user_id text NOT NULL,
  usage_id uuid NOT NULL REFERENCES gm_usage(id),
  amount numeric(18,8) NOT NULL,
  currency char(3) NOT NULL DEFAULT 'USD',
  entry_type text NOT NULL DEFAULT 'usage_charge',
  created_at timestamptz NOT NULL DEFAULT now()
);
