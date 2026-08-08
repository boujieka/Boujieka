import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import Home from "@/app/page";

describe("Home page", () => {
  it("renders the project name", () => {
    render(<Home />);
    expect(screen.getByText("Mon Répétiteur")).toBeInTheDocument();
  });
});
