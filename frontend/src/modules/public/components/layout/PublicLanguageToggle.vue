<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";
import type { LocaleCode } from "@/stores/locale.store";

const {
    locale,
    t,
    toggleLocale,
} = useI18n();

const nextLocaleLabel: Record<LocaleCode, string> = {
    ru: "EN",
    en: "DE",
    de: "FR",
    fr: "RU",
};

const label = computed(() => {
    return nextLocaleLabel[locale.value] || "RU";
});
</script>

<template>
    <button
        class="language-toggle"
        type="button"
        :aria-label="t('common.switchLanguage')"
        @click="toggleLocale"
    >
        <i class="fa-solid fa-language"></i>
        <span>{{ label }}</span>
    </button>
</template>
