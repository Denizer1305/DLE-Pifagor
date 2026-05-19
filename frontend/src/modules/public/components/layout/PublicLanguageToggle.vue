<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";

const {
    isEnglish,
    t,
    toggleLocale,
} = useI18n();

const label = computed(() => {
    return isEnglish.value ? "RU" : "EN";
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
