import {
  SESSION_SCOPED_STORAGE_KEYS,
  clearSessionScopedStorage,
  ensureSessionFingerprint,
} from "../sessionScopedStorage";

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  document.cookie = "EphapticOS_selected_tenant=abc;path=/";
});

describe("clearSessionScopedStorage", () => {
  it("removes every known session-scoped key from both storages", () => {
    for (const key of SESSION_SCOPED_STORAGE_KEYS) {
      localStorage.setItem(key, "stale");
      sessionStorage.setItem(key, "stale");
    }

    clearSessionScopedStorage();

    for (const key of SESSION_SCOPED_STORAGE_KEYS) {
      expect(localStorage.getItem(key)).toBeNull();
      expect(sessionStorage.getItem(key)).toBeNull();
    }
  });

  it("removes per-tenant keys matched by prefix", () => {
    localStorage.setItem("EphapticOS-connected-integrations-tenant-123", "stale");

    clearSessionScopedStorage();

    expect(localStorage.getItem("EphapticOS-connected-integrations-tenant-123")).toBeNull();
  });

  it("does not touch keys outside the session-scoped list", () => {
    localStorage.setItem("EphapticOS-pipeline-settings", "keep-me");
    sessionStorage.setItem("EphapticOS_anonymous_id", "keep-me");

    clearSessionScopedStorage();

    expect(localStorage.getItem("EphapticOS-pipeline-settings")).toBe("keep-me");
    expect(sessionStorage.getItem("EphapticOS_anonymous_id")).toBe("keep-me");
  });

  it("clears the tenant cookie", () => {
    clearSessionScopedStorage();

    expect(document.cookie).not.toContain("EphapticOS_selected_tenant=abc");
  });
});

describe("ensureSessionFingerprint", () => {
  it("wipes session-scoped storage when a different account is detected", () => {
    localStorage.setItem("EphapticOS_init_cache", "user-a-cache");
    ensureSessionFingerprint("auth0|user-a");

    ensureSessionFingerprint("auth0|user-b");

    expect(localStorage.getItem("EphapticOS_init_cache")).toBeNull();
  });

  it("does not wipe storage for the same account across calls", () => {
    ensureSessionFingerprint("auth0|user-a");
    localStorage.setItem("EphapticOS_init_cache", "user-a-cache");

    ensureSessionFingerprint("auth0|user-a");

    expect(localStorage.getItem("EphapticOS_init_cache")).toBe("user-a-cache");
  });

  it("does nothing when userId is null or undefined (identity not resolved yet)", () => {
    localStorage.setItem("EphapticOS_init_cache", "keep-me");

    ensureSessionFingerprint(null);
    ensureSessionFingerprint(undefined);

    expect(localStorage.getItem("EphapticOS_init_cache")).toBe("keep-me");
  });
});
