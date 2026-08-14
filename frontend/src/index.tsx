import type { ReactNode } from 'react'

export type UsageSummary = {
  requests: number
  input_tokens: number
  output_tokens: number
  cached_tokens: number
  provider_cost: string
  goodmorning_charge: string
}

export function UsageSummaryCard({ summary, title = 'Usage', children }: { summary: UsageSummary; title?: string; children?: ReactNode }) {
  return <section aria-label={title}><h2>{title}</h2><dl>
    <div><dt>Requests</dt><dd>{summary.requests}</dd></div>
    <div><dt>Tokens</dt><dd>{summary.input_tokens + summary.output_tokens}</dd></div>
    <div><dt>GoodMorning charge</dt><dd>{summary.goodmorning_charge}</dd></div>
  </dl>{children}</section>
}

export function AdminUsageTable({ rows }: { rows: Array<UsageSummary & { organization_id?: string; product_id?: string }> }) {
  return <table><thead><tr><th>Organization</th><th>Product</th><th>Requests</th><th>Charge</th></tr></thead><tbody>{rows.map((row, index) => <tr key={`${row.organization_id ?? ''}-${row.product_id ?? ''}-${index}`}><td>{row.organization_id ?? '—'}</td><td>{row.product_id ?? '—'}</td><td>{row.requests}</td><td>{row.goodmorning_charge}</td></tr>)}</tbody></table>
}
