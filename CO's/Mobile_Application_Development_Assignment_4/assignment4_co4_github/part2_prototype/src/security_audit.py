"""Rule-based security audit demonstration; not an OS penetration test."""
ASSETS = [
 {"asset":"Auth token","vector":"Other app reads shared file","control":"UID sandbox + Keystore-backed encryption","status":"PARTIALLY_BLOCKED","reason":"Sandbox blocks ordinary apps; rooted/compromised OS remains residual risk."},
 {"asset":"Patient database","vector":"Device theft / filesystem extraction","control":"Encrypted database with hardware-backed key","status":"PARTIALLY_BLOCKED","reason":"At-rest protection depends on key access policy and device lock state."},
 {"asset":"API traffic","vector":"Network interception","control":"TLS with certificate validation","status":"BLOCKED","reason":"Assuming correct hostname validation and no user-installed interception CA."},
 {"asset":"Exported component","vector":"Malicious app sends crafted intent","control":"Non-exported component + input validation","status":"BLOCKED","reason":"Public entry points still require authentication and validation."},
 {"asset":"Update package","vector":"Tampered update","control":"Package signature verification","status":"BLOCKED","reason":"Signing-key compromise or supply-chain compromise remains residual risk."},
 {"asset":"Location permission","vector":"Over-collection / user surprise","control":"Runtime permission + purpose limitation","status":"PARTIALLY_BLOCKED","reason":"Permission grant does not prevent misuse after access is granted."},
]
def audit(): return ASSETS
if __name__=="__main__":
    for a in audit(): print(" | ".join(str(a[k]) for k in ("asset","status","control","reason")))
