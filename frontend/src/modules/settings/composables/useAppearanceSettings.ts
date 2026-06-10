import { computed, onMounted, ref, watch } from "vue";

import { ROLE_LABELS } from "@/app/constants/roles.constants";
import {
    getAppearanceSettings,
    saveAppearanceSettings,
} from "@/modules/settings/services/settings.service";
import { mapAppearanceSettingsToPageState } from "@/modules/settings/mappers/settings.mapper";
import type {
    AppearanceSettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import { useAuthStore } from "@/stores/auth.store";
import { useLocaleStore } from "@/stores/locale.store";
import { useThemeStore } from "@/stores/theme.store";

export function useAppearanceSettings() {
    const authStore = useAuthStore();
    const localeStore = useLocaleStore();

    const settings = ref<AppearanceSettingsDto | null>(null);
    const pageState = ref<SettingsPageState<AppearanceSettingsDto> | null>(null);

    const isLoading = ref(false);
    const isSaving = ref(false);
    const errorMessage = ref("");

    const userContext = computed(() => {
        return {
            fullName: authStore.userFullName || "Пользователь",
            roleLabel: authStore.activeRole
                ? ROLE_LABELS[authStore.activeRole]
                : "Пользователь",
            roleCode: authStore.activeRole || "",
            avatarUrl: authStore.avatarUrl || "",
        };
    });

    async function loadAppearanceSettings(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getAppearanceSettings();
            const normalizedSettings = normalizeAppearanceSettings(result);

            setSettings(normalizedSettings);
            applyAppearanceSettings(normalizedSettings);

            if (normalizedSettings.color_mode !== result.color_mode) {
                void saveAppearanceSettings({
                    color_mode: normalizedSettings.color_mode,
                }).catch(() => undefined);
            }
        } catch (error) {
            errorMessage.value = getAppearanceErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    async function updateAppearance(
        payload: Partial<AppearanceSettingsDto>,
    ): Promise<void> {
        if (!settings.value) {
            return;
        }

        isSaving.value = true;
        errorMessage.value = "";

        const optimisticSettings = {
            ...settings.value,
            ...payload,
        };

        setSettings(optimisticSettings);
        applyAppearanceSettings(optimisticSettings);

        try {
            const result = await saveAppearanceSettings(payload);

            setSettings(result);
            applyAppearanceSettings(result);
        } catch (error) {
            errorMessage.value = getAppearanceErrorMessage(error);
            await loadAppearanceSettings();
        } finally {
            isSaving.value = false;
        }
    }

    function setSettings(nextSettings: AppearanceSettingsDto): void {
        settings.value = nextSettings;
        pageState.value = mapAppearanceSettingsToPageState(
            nextSettings,
            userContext.value,
            localeStore.locale,
        );
    }

    watch(
        () => localeStore.locale,
        () => {
            if (settings.value) {
                setSettings(settings.value);
            }
        },
    );

    onMounted(() => {
        void loadAppearanceSettings();
    });

    return {
        settings,
        pageState,
        isLoading,
        isSaving,
        errorMessage,
        loadAppearanceSettings,
        updateAppearance,
    };
}

export function applyAppearanceSettings(settings: AppearanceSettingsDto): void {
    const localeStore = useLocaleStore();
    const themeStore = useThemeStore();
    const root = document.documentElement;
    const colorMode = settings.theme === "dark"
        ? "dark"
        : settings.color_mode;
    const language = settings.language || "ru";

    root.dataset.brandTheme = settings.theme;
    root.dataset.colorMode = colorMode;
    root.dataset.density = settings.density;
    root.dataset.animations = String(settings.animations_enabled);
    root.dataset.glassPanels = String(settings.glass_panels_enabled);
    root.dataset.roundedCards = String(settings.rounded_cards_enabled);
    root.dataset.stickySidebar = String(settings.sticky_sidebar_enabled);
    root.dataset.largeCards = String(settings.large_cards_enabled);

    if (localeStore.locale !== language) {
        localeStore.setLocale(language);
    }

    if (themeStore.brandTheme !== settings.theme) {
        themeStore.setBrandTheme(settings.theme);
    }

    if (themeStore.mode !== colorMode) {
        themeStore.setThemeMode(colorMode);
    }
}

function normalizeAppearanceSettings(
    settings: AppearanceSettingsDto,
): AppearanceSettingsDto {
    return {
        ...settings,
        color_mode: settings.theme === "dark" ? "dark" : settings.color_mode,
        language: settings.language || "ru",
    };
}

function getAppearanceErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить настройки внешнего вида.";
}
