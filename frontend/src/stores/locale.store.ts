import { computed, ref, watch } from "vue";
import { defineStore } from "pinia";

import { runDocumentTransition } from "@/utils/document-transition.utils";

export type LocaleCode = "ru" | "en";

const LOCALE_STORAGE_KEY = "pifagor-locale";
const SUPPORTED_LOCALES: LocaleCode[] = ["ru", "en"];

function getStoredLocale(): LocaleCode {
    if (typeof localStorage === "undefined") {
        return "ru";
    }

    const savedLocale = localStorage.getItem(LOCALE_STORAGE_KEY);

    return SUPPORTED_LOCALES.includes(savedLocale as LocaleCode)
        ? savedLocale as LocaleCode
        : "ru";
}

function saveLocale(locale: LocaleCode): void {
    if (typeof localStorage === "undefined") {
        return;
    }

    localStorage.setItem(LOCALE_STORAGE_KEY, locale);
}

function applyLocaleToDocument(locale: LocaleCode): void {
    if (typeof document === "undefined") {
        return;
    }

    document.documentElement.lang = locale;
    document.documentElement.dataset.locale = locale;

    if (document.body) {
        document.body.dataset.locale = locale;
    }
}

export const useLocaleStore = defineStore("locale", () => {
    const locale = ref<LocaleCode>(getStoredLocale());

    const isEnglish = computed(() => locale.value === "en");
    const nextLocale = computed<LocaleCode>(() => locale.value === "en" ? "ru" : "en");

    function setLocale(nextValue: LocaleCode): void {
        if (nextValue !== locale.value) {
            runDocumentTransition("is-locale-switching");
        }

        locale.value = nextValue;
        saveLocale(nextValue);
        applyLocaleToDocument(nextValue);
    }

    function toggleLocale(): void {
        setLocale(nextLocale.value);
    }

    watch(
        locale,
        (value) => {
            applyLocaleToDocument(value);
        },
        {
            immediate: true,
        },
    );

    return {
        isEnglish,
        locale,
        nextLocale,
        setLocale,
        toggleLocale,
    };
});
