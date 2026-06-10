<script setup lang="ts">
import { computed } from "vue";

import SettingsCenterGrid from "@/modules/settings/components/SettingsCenterGrid.vue";
import SettingsPageShell from "@/modules/settings/components/SettingsPageShell.vue";

import { useSettingsPage } from "@/modules/settings/composables/useSettingsPage";
import { settingsCenterPageContent } from "@/modules/settings/data/appearance-page.data";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import { useLocaleStore } from "@/stores/locale.store";

const {
    pageModel,
    isLoading,
    errorMessage,
    loadSettings,
} = useSettingsPage();

const localeStore = useLocaleStore();
const content = computed(() => {
    return localizeSettingsContent(settingsCenterPageContent, localeStore.locale);
});
</script>

<template>
    <SettingsPageShell
        :model="pageModel?.scaffold"
        :hero="pageModel?.hero"
        :is-loading="isLoading"
        :error-message="errorMessage"
        :loading-text="content.loadingText"
        @reload="loadSettings"
    >
        <SettingsCenterGrid
            v-if="pageModel"
            :cards="pageModel.cards"
        />
    </SettingsPageShell>
</template>
