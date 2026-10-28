import type { NextConfig } from "next";

// Static export for GitHub Pages. The repo is served from /<repo-name>/.
const basePath = process.env.PAGES_BASE_PATH ?? "";

const config: NextConfig = {
  output: "export",
  basePath,
  images: { unoptimized: true },
  trailingSlash: true,
};

export default config;
