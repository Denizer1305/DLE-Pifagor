import { computed } from "vue";

import aiBlue from "@/assets/brand/logo/themes/blue/Anastasia.svg";
import aiDark from "@/assets/brand/logo/themes/dark/Anastasia.svg";
import aiGreen from "@/assets/brand/logo/themes/green/Anastasia.svg";
import aiLight from "@/assets/brand/logo/themes/light/Anastasia.svg";
import aiLightBlue from "@/assets/brand/logo/themes/light-blue/Anastasia.svg";
import aiOrange from "@/assets/brand/logo/themes/orange/Anastasia.svg";
import aiPinki from "@/assets/brand/logo/themes/pinki/Anastasia.svg";
import aiRed from "@/assets/brand/logo/themes/red/Anastasia.svg";
import aiViolet from "@/assets/brand/logo/themes/violett/Anastasia.svg";
import aiYellow from "@/assets/brand/logo/themes/yellow/Anastasia.svg";
import aiLegacy from "@/assets/image/logo/Anastasia.svg";
import heroBlue from "@/assets/brand/logo/themes/blue/hero-logo.svg";
import heroDark from "@/assets/brand/logo/themes/dark/hero-logo.svg";
import heroGreen from "@/assets/brand/logo/themes/green/hero-logo.svg";
import heroLight from "@/assets/brand/logo/themes/light/hero-logo.svg";
import heroLightBlue from "@/assets/brand/logo/themes/light-blue/hero-logo.svg";
import heroOrange from "@/assets/brand/logo/themes/orange/hero-logo.svg";
import heroPinki from "@/assets/brand/logo/themes/pinki/hero-logo.svg";
import heroRed from "@/assets/brand/logo/themes/red/hero-logo.svg";
import heroViolet from "@/assets/brand/logo/themes/violett/hero-logo.svg";
import heroYellow from "@/assets/brand/logo/themes/yellow/hero-logo.svg";
import logoBlue from "@/assets/brand/logo/themes/blue/logo.svg";
import logoDark from "@/assets/brand/logo/themes/dark/logo.svg";
import logoGreen from "@/assets/brand/logo/themes/green/logo.svg";
import logoLight from "@/assets/brand/logo/themes/light/logo.svg";
import logoLightBlue from "@/assets/brand/logo/themes/light-blue/logo.svg";
import logoOrange from "@/assets/brand/logo/themes/orange/logo.svg";
import logoPinki from "@/assets/brand/logo/themes/pinki/logo.svg";
import logoRed from "@/assets/brand/logo/themes/red/logo.svg";
import logoViolet from "@/assets/brand/logo/themes/violett/logo.svg";
import logoYellow from "@/assets/brand/logo/themes/yellow/logo.svg";
import logoLegacy from "@/assets/image/logo/logo.svg";
import { useThemeStore, type BrandTheme } from "@/stores/theme.store";

const logos: Record<BrandTheme, string> = {
    light: logoLight,
    blue: logoBlue,
    "light-blue": logoLightBlue,
    dark: logoDark,
    green: logoGreen,
    orange: logoOrange,
    pinki: logoPinki,
    red: logoRed,
    violet: logoViolet,
    yellow: logoYellow,
};

const heroLogos: Record<BrandTheme, string> = {
    light: heroLight,
    blue: heroBlue,
    "light-blue": heroLightBlue,
    dark: heroDark,
    green: heroGreen,
    orange: heroOrange,
    pinki: heroPinki,
    red: heroRed,
    violet: heroViolet,
    yellow: heroYellow,
};

const aiLogos: Record<BrandTheme, string> = {
    light: aiLight,
    blue: aiBlue,
    "light-blue": aiLightBlue,
    dark: aiDark,
    green: aiGreen,
    orange: aiOrange,
    pinki: aiPinki,
    red: aiRed,
    violet: aiViolet,
    yellow: aiYellow,
};

const knownLogos = new Set([logoLegacy, logoLight, ...Object.values(logos)]);
const knownHeroLogos = new Set([heroLight, ...Object.values(heroLogos)]);
const knownAiLogos = new Set([aiLegacy, ...Object.values(aiLogos)]);

export function useThemedLogo() {
    const themeStore = useThemeStore();

    const resolvedLogoTheme = computed<BrandTheme>(() => {
        if (themeStore.isDark) {
            return "dark";
        }

        if (themeStore.brandTheme === "dark") {
            return "light";
        }

        return themeStore.brandTheme;
    });

    const logoSrc = computed(() => logos[resolvedLogoTheme.value]);

    const heroLogoSrc = computed(() => heroLogos[resolvedLogoTheme.value]);

    const logoAISrc = computed(() => aiLogos[resolvedLogoTheme.value]);

    function getThemedLogoSrc(src: string): string {
        if (knownLogos.has(src)) {
            return logoSrc.value;
        }

        if (knownHeroLogos.has(src)) {
            return heroLogoSrc.value;
        }

        if (knownAiLogos.has(src)) {
            return logoAISrc.value;
        }

        return src;
    }

    return {
        getThemedLogoSrc,
        heroLogoSrc,
        logoSrc,
        logoAISrc,
    };
}
