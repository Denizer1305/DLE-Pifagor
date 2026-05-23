import { computed } from "vue";

import heroLogoDark from "@/assets/brand/logo/themes/dark/hero-logo.svg";
import heroLogo from "@/assets/brand/logo/themes/light/hero-logo.svg";
import logoDark from "@/assets/brand/logo/themes/dark/logo.svg";
import logoPrimary from "@/assets/brand/logo/themes/light/logo.svg";
import logoAIPrimary from "@/assets/brand/logo/themes/light/Anastasia.svg";
import logoAIDark from "@/assets/brand/logo/themes/dark/Anastasia.svg";
import { useThemeStore } from "@/stores/theme.store";

export function useThemedLogo() {
    const themeStore = useThemeStore();

    const logoSrc = computed(() => {
        return themeStore.isDark ? logoDark : logoPrimary;
    });

    const heroLogoSrc = computed(() => {
        return themeStore.isDark ? heroLogoDark : heroLogo;
    });

    const logoAISrc = computed(() => {
        return themeStore.isDark ? logoAIDark : logoAIPrimary;
    });

    function getThemedLogoSrc(src: string): string {
        if (!themeStore.isDark) {
            return src;
        }

        if (src === logoPrimary) {
            return logoDark;
        }

        if (src === heroLogo) {
            return heroLogoDark;
        }

        if (src === logoAIPrimary) {
            return logoAIDark;
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
