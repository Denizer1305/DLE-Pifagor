import { computed } from "vue";

import { messages, type MessageLocale } from "@/i18n/messages";
import { publicContentTranslations } from "@/i18n/public-content.translations";
import { useLocaleStore } from "@/stores/locale.store";

type JsonLike =
    | string
    | number
    | boolean
    | null
    | JsonLike[]
    | {
        [key: string]: JsonLike;
    };

function getNestedMessage(
    locale: MessageLocale,
    path: string,
): string | undefined {
    const parts = path.split(".");
    let current: unknown = messages[locale];

    for (const part of parts) {
        if (!current || typeof current !== "object" || !(part in current)) {
            return undefined;
        }

        current = (current as Record<string, unknown>)[part];
    }

    return typeof current === "string" ? current : undefined;
}

function interpolate(
    message: string,
    params?: Record<string, string | number>,
): string {
    if (!params) {
        return message;
    }

    return Object.entries(params).reduce((result, [key, value]) => {
        return result.replaceAll(`{${key}}`, String(value));
    }, message);
}

function localizeValue<T>(value: T, isEnglish: boolean): T {
    if (!isEnglish) {
        return value;
    }

    if (typeof value === "string") {
        return (publicContentTranslations[value] || value) as T;
    }

    if (Array.isArray(value)) {
        return value.map((item) => {
            return localizeValue(item, isEnglish);
        }) as T;
    }

    if (value && typeof value === "object") {
        return Object.fromEntries(
            Object.entries(value).map(([key, item]) => {
                return [
                    key,
                    localizeValue(item as JsonLike, isEnglish),
                ];
            }),
        ) as T;
    }

    return value;
}

export function useI18n() {
    const localeStore = useLocaleStore();
    const messageLocale = computed<MessageLocale>(() => {
        return localeStore.locale === "en" ? "en" : "ru";
    });

    const locale = computed(() => {
        return localeStore.locale;
    });

    const isEnglish = computed(() => {
        return localeStore.isEnglish;
    });

    function t(
        path: string,
        params?: Record<string, string | number>,
    ): string {
        const message = getNestedMessage(messageLocale.value, path)
            || getNestedMessage("ru", path)
            || path;

        return interpolate(message, params);
    }

    function localizePublicContent<T>(content: T): T {
        return localizeValue(content, localeStore.isEnglish);
    }

    function tr(value: string): string {
        return localizeValue(value, localeStore.isEnglish);
    }

    return {
        isEnglish,
        locale,
        localizePublicContent,
        setLocale: localeStore.setLocale,
        t,
        tr,
        toggleLocale: localeStore.toggleLocale,
    };
}
