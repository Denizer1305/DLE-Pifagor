<script setup lang="ts">
import type { StatusBadgeView } from "../../types";

interface Props {
    status: StatusBadgeView;
}

defineProps<Props>();
</script>

<template>
    <span
        class="org-table__status"
        :class="status.className"
    >
        {{ status.label }}
    </span>
</template>
