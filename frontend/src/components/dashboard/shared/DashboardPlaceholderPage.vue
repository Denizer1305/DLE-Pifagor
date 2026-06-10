<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

import {
    dashboardPlaceholderContent,
    type DashboardPlaceholderRole,
} from "@/components/dashboard/data/dashboard-placeholder.data";
import ErrorPageView from "@/pages/errors/ErrorPageView.vue";
import type { ErrorPageContent } from "@/pages/errors/error-pages.data";

const route = useRoute();

const role = computed<DashboardPlaceholderRole>(() => {
    const routeNamespace = route.path.split("/")[1];

    if (
        routeNamespace === "admin" ||
        routeNamespace === "teacher" ||
        routeNamespace === "student" ||
        routeNamespace === "parent"
    ) {
        return routeNamespace;
    }

    return "student";
});

const content = computed(() => dashboardPlaceholderContent[role.value]);

const title = computed(() => {
    return route.meta.title?.toString() || content.value.defaultTitle;
});

const pageContent = computed<ErrorPageContent>(() => ({
    code: "",
    variant: "not-found",
    title: title.value,
    subtitle: content.value.subtitle,
    description: content.value.text,
    details: {
        title: content.value.detailsTitle,
        icon: content.value.icon,
        items: content.value.details,
    },
    quickLinks: [
        {
            title: content.value.dashboardLinkTitle,
            description: content.value.dashboardLinkText,
            icon: "fa-solid fa-house",
            to: { name: content.value.dashboardRouteName },
        },
        {
            title: "Настройки кабинета",
            description: "Проверьте профиль, уведомления и параметры платформы.",
            icon: "fa-solid fa-gear",
            to: { name: content.value.settingsRouteName },
        },
    ],
    notes: [
        {
            text: content.value.note,
            icon: "fa-solid fa-circle-info",
            tone: "info",
        },
    ],
    visualIcon: content.value.visualIcon,
    orbitIcon: content.value.orbitIcon,
    actions: [
        {
            label: content.value.homeLabel,
            icon: "fa-solid fa-house",
            to: { name: content.value.dashboardRouteName },
            variant: "primary",
        },
        {
            label: content.value.backLabel,
            icon: "fa-solid fa-arrow-left",
            action: "back",
            variant: "secondary",
        },
    ],
    footer: {
        text: "Цифровая образовательная среда «Пифагор»",
        email: "Pifagor-Platform33@yandex.ru",
        phone: "+7 (900) 000-00-00",
    },
}));
</script>

<template>
    <ErrorPageView :content="pageContent" />
</template>
