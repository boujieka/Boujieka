import React from "react";
import { ColdOpen, StatFlip, TitleCard } from "./scenes/Openers";
import { Funnel, StageLadder, TwoTests } from "./scenes/Framework";
import { ActorTable, Layers, TwoExits } from "./scenes/Analysis";
import { CaseCard, Quote } from "./scenes/Evidence";
import { AskCard, CostList, KeyMessage, RemedyList } from "./scenes/Action";
import type { SceneCopy } from "./types";

/**
 * Maps a scene's copy to its component. The copy is a discriminated union, so
 * adding a scene kind without handling it here is a type error, not a blank
 * frame discovered at render time.
 */
export const SceneRenderer: React.FC<{ copy: SceneCopy }> = ({ copy }) => {
  switch (copy.kind) {
    case "title-card":
      return <TitleCard copy={copy} />;
    case "cold-open":
      return <ColdOpen copy={copy} />;
    case "stat-flip":
      return <StatFlip copy={copy} />;
    case "two-tests":
      return <TwoTests copy={copy} />;
    case "stage-ladder":
      return <StageLadder copy={copy} />;
    case "funnel":
      return <Funnel copy={copy} />;
    case "layers":
      return <Layers copy={copy} />;
    case "actor-table":
      return <ActorTable copy={copy} />;
    case "two-exits":
      return <TwoExits copy={copy} />;
    case "case-card":
      return <CaseCard copy={copy} />;
    case "quote":
      return <Quote copy={copy} />;
    case "cost-list":
      return <CostList copy={copy} />;
    case "remedy-list":
      return <RemedyList copy={copy} />;
    case "ask-card":
      return <AskCard copy={copy} />;
    case "key-message":
      return <KeyMessage copy={copy} />;
    default: {
      // Exhaustiveness guard.
      const never: never = copy;
      throw new Error(`Unhandled scene kind: ${JSON.stringify(never)}`);
    }
  }
};
