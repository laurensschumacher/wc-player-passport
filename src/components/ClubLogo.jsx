import { useState } from "react";
import { clubLogoUrl } from "../utils/clubLogo";

/**
 * Renders a club crest if we have one for this name, otherwise a
 * stadium emoji as a graceful fallback. Sized 24x24 with object-contain
 * so non-square logos don't distort.
 */
export default function ClubLogo({ name, size = 24, className = "" }) {
  const [errored, setErrored] = useState(false);
  const url = name ? clubLogoUrl(name) : null;

  if (!url || errored) {
    return (
      <span
        aria-hidden
        className={`inline-flex items-center justify-center text-base ${className}`}
        style={{ width: size, height: size }}
      >
        🏟️
      </span>
    );
  }

  return (
    <img
      src={url}
      alt=""
      width={size}
      height={size}
      onError={() => setErrored(true)}
      className={`object-contain shrink-0 ${className}`}
      style={{ width: size, height: size }}
      loading="lazy"
    />
  );
}
