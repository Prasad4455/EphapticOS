"use client";

import React from "react";
import type { SessionRow } from "@/modules/sessions/getSessions";
import type { TenantHourlyCosts } from "@/modules/billing/getTenantHourlyCosts";
import type { PipelineRun } from "@/ui/elements/AgentActivityTerminal";
import { AsciiFrame } from "./AsciiFrame";
import { FONT, T } from "./mono";
import type { DashRange } from "./RangeToggle";

/** Open-source stub — the spend/savings chart is priced off the tenant's real
 *  billing data and is a EphapticOS Cloud feature. Renders a text-only notice
 *  instead of syncing the real chart. */

interface CostPanelProps {
  sessions: SessionRow[];
  runs: PipelineRun[];
  balanceUsd: number | null;
  range: DashRange;
  onRangeChange: (range: DashRange) => void;
  hourlyCosts?: TenantHourlyCosts | null;
  onViewBreakdown?: () => void;
}

export function CostPanel(_props: CostPanelProps): React.ReactElement {
  return (
    <AsciiFrame label="Cost Savings" minHeight={260}>
      <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 10, textAlign: "center", padding: 20 }}>
        <span style={{ ...FONT, fontSize: 14, fontWeight: 500, color: T.text }}>
          Cost Savings is a EphapticOS Cloud feature
        </span>
        <span style={{ ...FONT, fontSize: 13, color: T.muted, maxWidth: 320 }}>
          Build your own dashboard from the API, or use the hosted one in EphapticOS Cloud.
        </span>
        <a
          href="https://www.EphapticOS.ai"
          target="_blank"
          rel="noopener noreferrer"
          style={{ ...FONT, marginTop: 4, background: T.lavender, color: "#000000", borderRadius: 8, padding: "8px 20px", fontSize: 13, fontWeight: 600, textDecoration: "none" }}
        >
          Open EphapticOS Cloud
        </a>
      </div>
    </AsciiFrame>
  );
}
