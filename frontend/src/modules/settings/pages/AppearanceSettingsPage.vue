<script setup lang="ts">
import { computed } from "vue";

import SettingsAppearanceThemeGrid from "@/modules/settings/components/SettingsAppearanceThemeGrid.vue";
import SettingsPageShell from "@/modules/settings/components/SettingsPageShell.vue";
import SettingsSectionCard from "@/modules/settings/components/SettingsSectionCard.vue";
import SettingsSelectRow from "@/modules/settings/components/SettingsSelectRow.vue";
import SettingsToggleRow from "@/modules/settings/components/SettingsToggleRow.vue";

import { appearancePageContent } from "@/modules/settings/data/appearance-page.data";
import { appearanceThemes } from "@/modules/settings/data/appearance-themes.data";
import {
    colorModeOptions,
    densityOptions,
    languageOptions,
} from "@/modules/settings/data/settings-options.data";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import { useAppearanceSettings } from "@/modules/settings/composables/useAppearanceSettings";
import type {
    SettingsColorMode,
    SettingsDensity,
    SettingsLanguage,
    SettingsTheme,
} from "@/modules/settings/types/settings.types";
import { useLocaleStore } from "@/stores/locale.store";

const {
    settings,
    pageState,
    isLoading,
    isSaving,
    errorMessage,
    loadAppearanceSettings,
    updateAppearance,
} = useAppearanceSettings();

const localeStore = useLocaleStore();

const content = computed(() => {
    return localizeSettingsContent(appearancePageContent, localeStore.locale);
});

const localizedThemes = computed(() => {
    return localizeSettingsContent(appearanceThemes, localeStore.locale);
});

const localizedColorModeOptions = computed(() => {
    return localizeSettingsContent(colorModeOptions, localeStore.locale);
});

const localizedDensityOptions = computed(() => {
    return localizeSettingsContent(densityOptions, localeStore.locale);
});

const localizedLanguageOptions = computed(() => {
    return localizeSettingsContent(languageOptions, localeStore.locale);
});

const activeTheme = computed(() => {
    return settings.value?.theme || "light";
});

async function selectTheme(theme: SettingsTheme): Promise<void> {
    await updateAppearance({
        theme,
        color_mode: theme === "dark" ? "dark" : "light",
    });
}

async function updateColorMode(value: string): Promise<void> {
    await updateAppearance({
        color_mode: value as SettingsColorMode,
    });
}

async function updateDensity(value: string): Promise<void> {
    await updateAppearance({
        density: value as SettingsDensity,
    });
}

async function updateLanguage(value: string): Promise<void> {
    await updateAppearance({
        language: value as SettingsLanguage,
    });
}

</script>

<template>
    <SettingsPageShell
        :model="pageState?.scaffold"
        :hero="pageState?.hero"
        :is-ready="Boolean(pageState && settings)"
        :is-loading="isLoading"
        :error-message="errorMessage"
        :loading-text="content.loadingText"
        @reload="loadAppearanceSettings"
    >
        <template v-if="settings">
        <SettingsSectionCard
            icon="fas fa-swatchbook"
            :topline="content.themeSection.topline"
            :title="content.themeSection.title"
            :text="content.themeSection.text"
        >
            <SettingsAppearanceThemeGrid
                :themes="localizedThemes"
                :active-theme="activeTheme"
                :disabled="isSaving"
                @select="selectTheme"
            />
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-circle-half-stroke"
            :topline="content.displaySection.topline"
            :title="content.displaySection.title"
            :text="content.displaySection.text"
        >
            <div class="settings-form-grid">
                <SettingsSelectRow
                    :label="content.displaySection.colorMode.label"
                    :text="content.displaySection.colorMode.text"
                    :model-value="settings.color_mode"
                    :options="localizedColorModeOptions"
                    :disabled="isSaving || activeTheme === 'dark'"
                    @update:model-value="updateColorMode"
                />

                <SettingsSelectRow
                    :label="content.displaySection.density.label"
                    :text="content.displaySection.density.text"
                    :model-value="settings.density"
                    :options="localizedDensityOptions"
                    :disabled="isSaving"
                    @update:model-value="updateDensity"
                />

                <SettingsSelectRow
                    :label="content.displaySection.language.label"
                    :text="content.displaySection.language.text"
                    :model-value="settings.language"
                    :options="localizedLanguageOptions"
                    :disabled="isSaving"
                    @update:model-value="updateLanguage"
                />
            </div>
        </SettingsSectionCard>

        <SettingsSectionCard
            icon="fas fa-sliders"
            :topline="content.visualSection.topline"
            :title="content.visualSection.title"
            :text="content.visualSection.text"
        >
            <div class="settings-toggle-list">
                <SettingsToggleRow
                    :label="content.visualSection.animations.label"
                    :text="content.visualSection.animations.text"
                    :model-value="settings.animations_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateAppearance({ animations_enabled: $event })"
                />

                <SettingsToggleRow
                    :label="content.visualSection.glassPanels.label"
                    :text="content.visualSection.glassPanels.text"
                    :model-value="settings.glass_panels_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateAppearance({ glass_panels_enabled: $event })"
                />

                <SettingsToggleRow
                    :label="content.visualSection.roundedCards.label"
                    :text="content.visualSection.roundedCards.text"
                    :model-value="settings.rounded_cards_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateAppearance({ rounded_cards_enabled: $event })"
                />

                <SettingsToggleRow
                    :label="content.visualSection.stickySidebar.label"
                    :text="content.visualSection.stickySidebar.text"
                    :model-value="settings.sticky_sidebar_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateAppearance({ sticky_sidebar_enabled: $event })"
                />

                <SettingsToggleRow
                    :label="content.visualSection.largeCards.label"
                    :text="content.visualSection.largeCards.text"
                    :model-value="settings.large_cards_enabled"
                    :disabled="isSaving"
                    @update:model-value="updateAppearance({ large_cards_enabled: $event })"
                />
            </div>
        </SettingsSectionCard>
        </template>
    </SettingsPageShell>
</template>
