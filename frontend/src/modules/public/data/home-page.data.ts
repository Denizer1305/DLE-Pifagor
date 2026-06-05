import type { HomePageContent } from "@/modules/public/data/home-page.types";
import { homeHero } from "@/modules/public/data/home-page-hero.data";
import { homeFeatures } from "@/modules/public/data/home-page-features.data";
import { homeAi } from "@/modules/public/data/home-page-ai.data";
import {
    homeCta,
    homePartners,
    homeTestimonials,
} from "@/modules/public/data/home-page-community.data";

export type * from "@/modules/public/data/home-page.types";
export {
    homeHero,
    homeFeatures,
    homeAi,
    homePartners,
    homeTestimonials,
    homeCta,
};

export const homePageContent: HomePageContent = {
    hero: homeHero,
    features: homeFeatures,
    ai: homeAi,
    partners: homePartners,
    testimonials: homeTestimonials,
    cta: homeCta,
};
