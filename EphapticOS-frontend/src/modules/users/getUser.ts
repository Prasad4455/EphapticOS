"use server";

import EphapticOSUser from "./EphapticOSUser";
import getLocalUser from "./getLocalUser";

/**
 * Open-source version — delegates to getLocalUser.
 * The SaaS version uses Auth0 session to resolve the authenticated user.
 */
export default async function getUser(): Promise<EphapticOSUser> {
  return await getLocalUser() ?? {
    id: "local",
    name: "Local User",
    email: "local@EphapticOS.local",
    picture: "",
  };
}
