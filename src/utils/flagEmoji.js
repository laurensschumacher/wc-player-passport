// ISO-3166-1 alpha-3 -> alpha-2 mapping for the nationality codes used in the
// dataset. Only the codes that actually appear are included; everything else
// falls back to a globe emoji.
const ALPHA3_TO_ALPHA2 = {
  ARG: "AR", AUS: "AU", BEL: "BE", BIH: "BA", BRA: "BR", CAN: "CA",
  CHL: "CL", CIV: "CI", CMR: "CM", COL: "CO", CRC: "CR", CRO: "HR",
  CZE: "CZ", DEN: "DK", ECU: "EC", EGY: "EG", ENG: "GB-ENG", ESP: "ES",
  FRA: "FR", GER: "DE", GHA: "GH", GRE: "GR", HON: "HN", HRV: "HR",
  ISL: "IS", IRN: "IR", ITA: "IT", JAM: "JM", JPN: "JP", KOR: "KR",
  KSA: "SA", MAR: "MA", MEX: "MX", NED: "NL", NGA: "NG", NIR: "GB-NIR",
  NOR: "NO", NZL: "NZ", PAN: "PA", PAR: "PY", PER: "PE", POL: "PL",
  POR: "PT", QAT: "QA", ROU: "RO", RSA: "ZA", RUS: "RU", SCO: "GB-SCT",
  SEN: "SN", SRB: "RS", SUI: "CH", SVK: "SK", SVN: "SI", SWE: "SE",
  TUN: "TN", TUR: "TR", UKR: "UA", URU: "UY", USA: "US", UZB: "UZ",
  WAL: "GB-WLS",
};

const REGIONAL_INDICATOR_OFFSET = 0x1f1a5; // 'A' (0x41) + 0x1f1e6 - 0x41

function alpha2ToFlagEmoji(alpha2) {
  if (!alpha2) return "🏳️";
  // Special UK home-nation flags (England, Scotland, Wales) use tag sequences.
  if (alpha2 === "GB-ENG") return "🏴󠁧󠁢󠁥󠁮󠁧󠁿";
  if (alpha2 === "GB-SCT") return "🏴󠁧󠁢󠁳󠁣󠁴󠁿";
  if (alpha2 === "GB-WLS") return "🏴󠁧󠁢󠁷󠁬󠁳󠁿";
  if (alpha2 === "GB-NIR") return "🇬🇧"; // no standard tag flag, use UK
  if (alpha2.length !== 2) return "🏳️";
  const codePoints = [...alpha2.toUpperCase()].map(
    (c) => c.charCodeAt(0) + REGIONAL_INDICATOR_OFFSET,
  );
  return String.fromCodePoint(...codePoints);
}

export function flagFromCode(alpha3) {
  if (!alpha3) return "🏳️";
  const a2 = ALPHA3_TO_ALPHA2[alpha3.toUpperCase()];
  return alpha2ToFlagEmoji(a2);
}
