import { computed, ref, watch } from "vue";
import { defineStore } from "pinia";

import { runDocumentTransition } from "@/utils/document-transition.utils";

type ThemeMode = "light" | "dark" | "system";

const THEME_STORAGE_KEY = "pifagor-theme-mode";

function getSystemPrefersDark(): boolean {
    if (typeof window === "undefined") {
        return false;
    }

    return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function getStoredThemeMode(): ThemeMode {
    if (typeof localStorage === "undefined") {
        return "light";
    }

    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);

    if (savedTheme === "light" || savedTheme === "dark" || savedTheme === "system") {
        return savedTheme;
    }

    return "light";
}

function saveThemeMode(mode: ThemeMode): void {
    if (typeof localStorage === "undefined") {
        return;
    }

    localStorage.setItem(THEME_STORAGE_KEY, mode);
}

function applyThemeToDocument(isDark: boolean): void {
    if (typeof document === "undefined") {
        return;
    }

    const root = document.documentElement;
    const body = document.body;

    root.classList.toggle("theme-dark", isDark);
    root.classList.toggle("theme-light", !isDark);
    root.classList.toggle("dark-theme", isDark);

    body.classList.toggle("theme-dark", isDark);
    body.classList.toggle("theme-light", !isDark);
    body.classList.toggle("dark-theme", isDark);

    root.dataset.theme = isDark ? "dark" : "light";
    body.dataset.theme = isDark ? "dark" : "light";
}

export const useThemeStore = defineStore("theme", () => {
    const mode = ref<ThemeMode>(getStoredThemeMode());
    const systemPrefersDark = ref(getSystemPrefersDark());

    const isSystemMode = computed(() => mode.value === "system");

    const isDark = computed(() => {
        if (mode.value === "system") {
            return systemPrefersDark.value;
        }

        return mode.value === "dark";
    });

    const currentTheme = computed<"light" | "dark">(() => {
        return isDark.value ? "dark" : "light";
    });

    function setThemeMode(nextMode: ThemeMode): void {
        if (nextMode !== mode.value || nextMode === "system") {
            runDocumentTransition("is-theme-switching");
        }

        mode.value = nextMode;
        saveThemeMode(nextMode);
        applyThemeToDocument(isDark.value);
    }

    function setLightTheme(): void {
        setThemeMode("light");
    }

    function setDarkTheme(): void {
        setThemeMode("dark");
    }

    function setSystemTheme(): void {
        setThemeMode("system");
    }

    function toggleTheme(): void {
        if (isDark.value) {
            setThemeMode("light");
            return;
        }

        setThemeMode("dark");
    }

    function initTheme(): void {
        systemPrefersDark.value = getSystemPrefersDark();
        applyThemeToDocument(isDark.value);

        if (typeof window === "undefined") {
            return;
        }

        const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

        const handleSystemThemeChange = (event: MediaQueryListEvent): void => {
            systemPrefersDark.value = event.matches;

            if (mode.value === "system") {
                applyThemeToDocument(isDark.value);
            }
        };

        mediaQuery.addEventListener("change", handleSystemThemeChange);
    }

    watch(
        isDark,
        (value) => {
            applyThemeToDocument(value);
        },
        {
            immediate: true,
        },
    );

    return {
        mode,
        isDark,
        isSystemMode,
        currentTheme,

        initTheme,
        setThemeMode,
        setLightTheme,
        setDarkTheme,
        setSystemTheme,
        toggleTheme,
    };
});
