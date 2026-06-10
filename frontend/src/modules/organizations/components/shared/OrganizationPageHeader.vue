<script setup lang="ts">
import type { OrganizationPageHeaderView } from "../../types";

interface Props {
    header: OrganizationPageHeaderView;
    isPrimaryActionVisible?: boolean;
    isSecondaryActionVisible?: boolean;
}

interface Emits {
    (event: "primary-action"): void;
    (event: "secondary-action"): void;
}

withDefaults(defineProps<Props>(), {
    isPrimaryActionVisible: true,
    isSecondaryActionVisible: false,
});

defineEmits<Emits>();
</script>

<template>
    <header class="org-page__header">
        <div>
            <span
                v-if="header.eyebrow"
                class="org-page__eyebrow"
            >
                {{ header.eyebrow }}
            </span>

            <h1 class="org-page__title">
                {{ header.title }}
            </h1>

            <p
                v-if="header.description"
                class="org-page__description"
            >
                {{ header.description }}
            </p>
        </div>

        <div
            v-if="
                (isPrimaryActionVisible && header.primaryActionLabel)
                || (isSecondaryActionVisible && header.secondaryActionLabel)
                || $slots.actions
            "
            class="org-page__actions"
        >
            <slot name="actions">
                <button
                    v-if="isSecondaryActionVisible && header.secondaryActionLabel"
                    class="org-toolbar__button"
                    type="button"
                    @click="$emit('secondary-action')"
                >
                    {{ header.secondaryActionLabel }}
                </button>

                <button
                    v-if="isPrimaryActionVisible && header.primaryActionLabel"
                    class="org-toolbar__button org-toolbar__button--primary"
                    type="button"
                    @click="$emit('primary-action')"
                >
                    {{ header.primaryActionLabel }}
                </button>
            </slot>
        </div>
    </header>
</template>