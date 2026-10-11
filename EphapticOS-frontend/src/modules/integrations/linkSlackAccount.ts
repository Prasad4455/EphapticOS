"use server";

export interface LinkSlackResult {
  success: boolean;
  error?: string;
}

const UNAVAILABLE =
  "Linking a Slack account to a EphapticOS login is handled by EphapticOS Cloud, which issues and redeems the /EphapticOS-link code.";

/** Open-source stub — see startConnection.ts. */
export default async function linkSlackAccount(
  _tenantId: string,
  _code: string,
): Promise<LinkSlackResult> {
  return { success: false, error: UNAVAILABLE };
}
