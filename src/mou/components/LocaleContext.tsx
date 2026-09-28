import React, { createContext, useContext } from "react";
import { en } from "../content/en";
import type { LocaleBundle } from "../types";

const ChromeContext = createContext<LocaleBundle["chrome"]>(en.chrome);

export const ChromeProvider: React.FC<{
  chrome: LocaleBundle["chrome"];
  children: React.ReactNode;
}> = ({ chrome, children }) => <ChromeContext.Provider value={chrome}>{children}</ChromeContext.Provider>;

/** Labels that belong to the interface rather than to a scene's copy. */
export const useChrome = (): LocaleBundle["chrome"] => useContext(ChromeContext);
