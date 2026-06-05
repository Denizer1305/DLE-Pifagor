<script setup lang="ts">
interface Props {
    badge?: string;
    icon?: string;
    title: string;
    text?: string;
}

defineProps<Props>();
</script>

<template>
    <div class="dashboard-section-head">
        <div>
            <span
                v-if="badge"
                class="dashboard-badge"
            >
                <i
                    v-if="icon"
                    :class="icon"
                ></i>

                {{ badge }}
            </span>

            <h2 class="dashboard-section-title">
                {{ title }}
            </h2>

            <p
                v-if="text"
                class="dashboard-section-text"
            >
                {{ text }}
            </p>
        </div>

        <slot name="actions"></slot>
    </div>
</template>
