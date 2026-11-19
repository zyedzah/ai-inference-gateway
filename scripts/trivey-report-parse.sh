!#/usr/bin/env bash

jq -r '
  [.Results[].Vulnerabilities[]?] as $findings
  | (["SEVERITY", "PACKAGE", "CVE", "INSTALLED", "FIXED"] | @tsv),
    ($findings[] | [.Severity, .PkgName, .VulnerabilityID,
                    .InstalledVersion, (.FixedVersion // "—")] | @tsv),
    "Total findings: \($findings | length)",
    "Unique vulnerability IDs: \($findings | map(.VulnerabilityID) | unique | length)"
' /tmp/gateway-image-reports/trivy-report.json
