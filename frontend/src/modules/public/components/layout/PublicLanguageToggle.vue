<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from "vue";

import { useI18n } from "@/composables/useI18n";
import type { LocaleCode } from "@/stores/locale.store";

const {
    locale,
    setLocale,
    t,
} = useI18n();

type LanguageOption = {
    value: LocaleCode;
    label: string;
    title: string;
};

const languageOptions: [LanguageOption, ...LanguageOption[]] = [
    { value: "ru", label: "RU", title: "Russian" },
    { value: "en", label: "EN", title: "English" },
    { value: "de", label: "DE", title: "Deutsch" },
    { value: "fr", label: "FR", title: "French" },
];

const isOpen = ref(false);
const rootElement = ref<HTMLElement | null>(null);

const activeOption = computed<LanguageOption>(() => {
    return languageOptions.find((option) => option.value === locale.value)
        || languageOptions[0];
});

function closeMenu(): void {
    isOpen.value = false;
}

function toggleMenu(): void {
    isOpen.value = !isOpen.value;
}

function selectLocale(value: LocaleCode): void {
    setLocale(value);
    closeMenu();
}

function handleDocumentPointerDown(event: PointerEvent): void {
    if (!isOpen.value || !rootElement.value) {
        return;
    }

    if (rootElement.value.contains(event.target as Node)) {
        return;
    }

    closeMenu();
}

function handleKeydown(event: KeyboardEvent): void {
    if (event.key === "Escape") {
        closeMenu();
    }
}

document.addEventListener("pointerdown", handleDocumentPointerDown);
document.addEventListener("keydown", handleKeydown);

onBeforeUnmount(() => {
    document.removeEventListener("pointerdown", handleDocumentPointerDown);
    document.removeEventListener("keydown", handleKeydown);
});
</script>

<template>
    <div
        ref="rootElement"
        class="language-toggle language-select"
        :class="{ 'is-open': isOpen }"
        :title="t('common.switchLanguage')"
    >
        <button
            class="language-select__button"
            type="button"
            :aria-label="t('common.switchLanguage')"
            :aria-expanded="isOpen"
            aria-haspopup="listbox"
            @click="toggleMenu"
        >
            <i
                class="fa-solid fa-language"
                aria-hidden="true"
            ></i>

            <span>{{ activeOption.label }}</span>

            <i
                class="fa-solid fa-chevron-down language-select__arrow"
                aria-hidden="true"
            ></i>
        </button>

        <div
            v-if="isOpen"
            class="language-select__menu"
            role="listbox"
            :aria-label="t('common.switchLanguage')"
        >
            <button
                v-for="option in languageOptions"
                :key="option.value"
                class="language-select__option"
                :class="{ 'is-active': option.value === locale }"
                type="button"
                role="option"
                :aria-selected="option.value === locale"
                @click="selectLocale(option.value)"
            >
                <span class="language-select__code">{{ option.label }}</span>
                <span class="language-select__name">{{ option.title }}</span>
            </button>
        </div>
    </div>
</template>
