import { useVideoConfig } from "remotion";

// Échelle commune pour 16:9 (1920x1080) et 9:16 (1080x1920).
export const useLayout = () => {
  const { width, height } = useVideoConfig();
  const vertical = height > width;
  return {
    vertical,
    s: vertical ? 0.95 : width / 1920,
    padX: vertical ? 70 : 140,
    padY: vertical ? 220 : 110,
  };
};
