"use server";

import EphapticOSUser from "./EphapticOSUser";

export default async function getLocalUser(): Promise<EphapticOSUser | null> {
  // In local mode, we can't use Auth0 session.
  // Return a placeholder user — the actual auth is handled by
  // the backend cookie, not a server-side session.
  // The LocalProvider already verified auth via /api/v1/users/me.
  return {
    id: "local",
    name: "Local User",
    email: "local@EphapticOS.local",
    picture: "",
  };
}
