import { curlBin, exportEnvVar, homePath, installUv, whichCommand, writeSkillFile } from "../osCommands";

describe("osCommands", () => {
  it("exportEnvVar uses export on mac and $env: assignment on windows", () => {
    expect(exportEnvVar("mac", "EphapticOS_API_KEY", "abc")).toBe(`export EphapticOS_API_KEY="abc"`);
    expect(exportEnvVar("windows", "EphapticOS_API_KEY", "abc")).toBe(`$env:EphapticOS_API_KEY = "abc"`);
  });

  it("homePath expands to a PowerShell-native path on windows, not %USERPROFILE%", () => {
    expect(homePath("mac", "/.claude/skills/EphapticOS/SKILL.md")).toBe("~/.claude/skills/EphapticOS/SKILL.md");
    expect(homePath("windows", "/.claude/skills/EphapticOS/SKILL.md")).toBe(
      "$env:USERPROFILE\\.claude\\skills\\EphapticOS\\SKILL.md",
    );
  });

  it("curlBin uses curl.exe only on windows", () => {
    expect(curlBin("mac")).toBe("curl");
    expect(curlBin("windows")).toBe("curl.exe");
  });

  it("installUv uses the PowerShell installer only on windows", () => {
    expect(installUv("mac")).toBe("curl -LsSf https://astral.sh/uv/install.sh | sh");
    expect(installUv("windows")).toBe("irm https://astral.sh/uv/install.ps1 | iex");
  });

  it("whichCommand uses Get-Command only on windows", () => {
    expect(whichCommand("mac", "uvx")).toBe("which uvx");
    expect(whichCommand("windows", "uvx")).toBe("Get-Command uvx");
  });

  it("writeSkillFile emits a PowerShell here-string on windows and a bash heredoc on mac", () => {
    const mac = writeSkillFile("mac", "/.claude/skills/EphapticOS", "SKILL.md", "content");
    expect(mac).toBe(
      "mkdir -p ~/.claude/skills/EphapticOS && cat > ~/.claude/skills/EphapticOS/SKILL.md << 'EphapticOS_EOF'\ncontent\nEphapticOS_EOF",
    );

    const windows = writeSkillFile("windows", "/.claude/skills/EphapticOS", "SKILL.md", "content");
    expect(windows).toBe(
      'New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\\.claude\\skills\\EphapticOS" | Out-Null\n' +
      'Set-Content -Path "$env:USERPROFILE\\.claude\\skills\\EphapticOS\\SKILL.md" -Value @\'\ncontent\n\'@',
    );
  });
});
