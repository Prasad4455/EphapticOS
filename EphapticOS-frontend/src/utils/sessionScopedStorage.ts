// Storage tied to a specific Auth0 account, not to the browser/device. If a
// second account logs in on the same tab (or a stale tab never ran the
// signout script), these keys must not leak into the new session — they
// carry tenant selection, cached credentials, and workspace state.
//
// Deliberately excludes: analytics/attribution keys (EphapticOS_anonymous_id,
// EphapticOS_first_touch, etc. — track the device, not the account) and cosmetic
// UI preferences (EphapticOS-pipeline-settings, EphapticOS-credits-banner-dismissed,
// EphapticOS-terminal-demo-shown — losing these on account switch is not a
// correctness or security issue).
export const SESSION_SCOPED_STORAGE_KEYS = [
  "EphapticOS_selected_tenant",
  "EphapticOS_selected_tenant_name",
  "EphapticOS_init_cache",
  "EphapticOS_plan_type",
  "EphapticOS_stripe_ensured",
  "EphapticOS_pending_workspace_name",
  "EphapticOS_pre_checkout_tenants",
  "EphapticOS_user_email",
  "EphapticOS_user_id",
  "EphapticOS-awaiting-dataset",
  "EphapticOS-graph-nodes",
] as const;

// Per-tenant keys — the tenant id suffix varies, so these are matched by prefix.
export const SESSION_SCOPED_STORAGE_PREFIXES = ["EphapticOS-connected-integrations-"] as const;

export function clearSessionScopedStorage(): void {
  for (const key of SESSION_SCOPED_STORAGE_KEYS) {
    localStorage.removeItem(key);
    sessionStorage.removeItem(key);
  }
  for (const store of [localStorage, sessionStorage]) {
    for (let i = store.length - 1; i >= 0; i--) {
      const key = store.key(i);
      if (key && SESSION_SCOPED_STORAGE_PREFIXES.some((prefix) => key.startsWith(prefix))) {
        store.removeItem(key);
      }
    }
  }
  document.cookie = "EphapticOS_selected_tenant=;Max-Age=0;path=/";
}

// sessionStorage, not localStorage: the fingerprint only needs to catch an
// account switch within the same tab's lifetime — a stale localStorage
// fingerprint from days ago would false-positive on legitimate re-logins.
const SESSION_FINGERPRINT_KEY = "EphapticOS_session_user_id";

// Wipes session-scoped storage the moment a DIFFERENT account is detected in
// this tab, and is safe to call redundantly from every consumer of that
// storage (UserProvider, useTenantInit, ...) rather than only once in a
// single effect. Calling it inline, synchronously, at the point of use closes
// the ordering race a single top-level effect can't guarantee: React commits
// child effects before parent effects, so a child reading EphapticOS_init_cache
// before the parent's own fingerprint effect fires would otherwise hydrate
// the previous account's apiKey first.
export function ensureSessionFingerprint(userId: string | null | undefined): void {
  if (!userId) return;
  const previousUserId = sessionStorage.getItem(SESSION_FINGERPRINT_KEY);
  if (previousUserId && previousUserId !== userId) {
    clearSessionScopedStorage();
  }
  sessionStorage.setItem(SESSION_FINGERPRINT_KEY, userId);
}
