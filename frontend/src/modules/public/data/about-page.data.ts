import type { AboutPageContent } from "@/modules/public/data/about-page.types";
import {
    aboutHero,
    aboutStory,
} from "@/modules/public/data/about-page-intro.data";
import {
    aboutMission,
    aboutRoadmap,
} from "@/modules/public/data/about-page-direction.data";
import { aboutTeam } from "@/modules/public/data/about-page-team.data";
import {
    aboutCta,
    aboutGratitude,
} from "@/modules/public/data/about-page-gratitude.data";

export type * from "@/modules/public/data/about-page.types";
export {
    aboutHero,
    aboutStory,
    aboutMission,
    aboutRoadmap,
    aboutTeam,
    aboutGratitude,
    aboutCta,
};

export const aboutPageContent: AboutPageContent = {
    hero: aboutHero,
    story: aboutStory,
    mission: aboutMission,
    roadmap: aboutRoadmap,
    team: aboutTeam,
    gratitude: aboutGratitude,
    cta: aboutCta,
};
