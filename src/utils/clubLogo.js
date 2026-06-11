import logos from "../data/club_logos.json";

/**
 * Returns the public URL for a club's crest image, or null if we don't
 * have one. Tries the exact name, then a couple of trivial variants
 * ("Liverpool" vs "Liverpool FC", trailing whitespace, case) so that
 * the same logo can be reused for slightly differing names in
 * world_cups[].club vs career_clubs[].club.
 */
export function clubLogoUrl(name) {
  if (!name) return null;
  const direct = logos[name];
  if (direct) return direct;

  const trimmed = name.trim();
  if (trimmed !== name && logos[trimmed]) return logos[trimmed];

  // Try stripping common suffixes
  const stripped = trimmed
    .replace(/\s+(F\.?C\.?|FC|CF|SC|AC|AFC)$/i, "")
    .trim();
  if (stripped && logos[stripped]) return logos[stripped];

  // Try adding " FC"
  const withFc = `${trimmed} FC`;
  if (logos[withFc]) return logos[withFc];

  return null;
}
