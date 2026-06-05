import type { AppearanceThemeModel } from "@/modules/settings/types/settings.types";

export const appearanceThemes: AppearanceThemeModel[] = [
    {
        key: "light",
        title: "Классическая",
        text: "Светлая исходная тема платформы для спокойной ежедневной работы.",
        previewClass: "is-light",
        tokens: [
            "#394458",
            "#4a6fa5",
            "#eef1f6",
        ],
    },
    {
        key: "blue",
        title: "Синий",
        text: "Классическая тема Пифагора для ежедневной работы.",
        previewClass: "is-blue",
        tokens: [
            "#2f6bff",
            "#8ec5ff",
            "#eef5ff",
        ],
    },
    {
        key: "light-blue",
        title: "Голубой",
        text: "Воздушная цветовая схема с мягким голубым акцентом.",
        previewClass: "is-light-blue",
        tokens: [
            "#4f94d4",
            "#b9d7f7",
            "#f3f9ff",
        ],
    },
    {
        key: "green",
        title: "Зелёный",
        text: "Спокойная тема для длительной работы с материалами.",
        previewClass: "is-green",
        tokens: [
            "#27ae60",
            "#9be7bd",
            "#edfdf4",
        ],
    },
    {
        key: "orange",
        title: "Оранжевый",
        text: "Тёплая тема для активного рабочего пространства.",
        previewClass: "is-orange",
        tokens: [
            "#f2994a",
            "#ffd6a8",
            "#fff6ed",
        ],
    },
    {
        key: "pinki",
        title: "Розовый",
        text: "Мягкая выразительная тема с аккуратным ягодным акцентом.",
        previewClass: "is-pinki",
        tokens: [
            "#d96aa0",
            "#f2a8ca",
            "#fff4fa",
        ],
    },
    {
        key: "violet",
        title: "Фиолетовый",
        text: "Акцентная тема для творческих и методических задач.",
        previewClass: "is-violet",
        tokens: [
            "#7c3aed",
            "#c4b5fd",
            "#f5f3ff",
        ],
    },
    {
        key: "red",
        title: "Красный",
        text: "Контрастная тема для заметных акцентов и контроля.",
        previewClass: "is-red",
        tokens: [
            "#ef4444",
            "#fecaca",
            "#fff1f2",
        ],
    },
    {
        key: "yellow",
        title: "Жёлтый",
        text: "Светлая и живая тема для мягкого визуального акцента.",
        previewClass: "is-yellow",
        tokens: [
            "#facc15",
            "#fde68a",
            "#fffbeb",
        ],
    },
    {
        key: "dark",
        title: "Тёмный",
        text: "Глубокая тема для работы вечером и снижения нагрузки на глаза.",
        previewClass: "is-dark",
        tokens: [
            "#111827",
            "#374151",
            "#f9fafb",
        ],
    },
];
