<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";

type StatusType = "info" | "success" | "warning" | "error";

interface Props {
    type?: StatusType;
    icon?: string;
    title: string;
    text: string;
}

const props = withDefaults(defineProps<Props>(), {
    type: "info",
    icon: "",
});

const { tr } = useI18n();

function getDefaultIcon(): string {
    if (props.icon) {
        return props.icon;
    }

    if (props.type === "success") {
        return "fa-solid fa-circle-check";
    }

    if (props.type === "warning") {
        return "fa-solid fa-triangle-exclamation";
    }

    if (props.type === "error") {
        return "fa-solid fa-circle-xmark";
    }

    return "fa-solid fa-circle-info";
}
</script>

<template>
    <div :class="['auth-status-card', `auth-status-card--${type}`]">
        <div class="auth-status-card__icon">
            <i :class="getDefaultIcon()"></i>
        </div>

        <div class="auth-status-card__content">
            <h3 class="auth-status-card__title">
                {{ tr(title) }}
            </h3>

            <p class="auth-status-card__text">
                {{ tr(text) }}
            </p>
        </div>
    </div>
</template>
