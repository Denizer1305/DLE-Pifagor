<script setup lang="ts">
interface Props {
    label?: string;
    value: number;
}

const props = withDefaults(defineProps<Props>(), {
    label: "",
});

function normalizedValue(): number {
    return Math.min(100, Math.max(0, props.value));
}
</script>

<template>
    <div class="dashboard-progress">
        <div class="dashboard-progress-head">
            <span class="dashboard-progress-label">{{ label }}</span>
            <span class="dashboard-progress-label">{{ normalizedValue() }}%</span>
        </div>

        <div class="dashboard-progress-track">
            <div
                class="dashboard-progress-bar"
                :style="{ width: `${normalizedValue()}%` }"
            ></div>
        </div>
    </div>
</template>
