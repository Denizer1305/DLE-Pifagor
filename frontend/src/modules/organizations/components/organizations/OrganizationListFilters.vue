<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";

interface Props {
    isActive: boolean | null;
    isPublic: boolean | null;
    hasActiveFilters?: boolean;
}

interface Emits {
    (event: "set-active", value: boolean | null): void;
    (event: "set-public", value: boolean | null): void;
    (event: "reset"): void;
}

withDefaults(defineProps<Props>(), {
    hasActiveFilters: false,
});

defineEmits<Emits>();

const activeOptions = [
    {
        value: "",
        label: "Все статусы",
    },
    {
        value: "true",
        label: "Активные",
    },
    {
        value: "false",
        label: "Неактивные",
    },
];

const publicOptions = [
    {
        value: "",
        label: "Все типы",
    },
    {
        value: "true",
        label: "Публичные",
    },
    {
        value: "false",
        label: "Скрытые",
    },
];

function formatBooleanFilter(value: boolean | null): string {
    return value === null ? "" : String(value);
}

function parseBooleanFilter(value: string): boolean | null {
    if (value === "") {
        return null;
    }

    return value === "true";
}
</script>

<template>
    <div class="org-filters__field org-toolbar__filter-field">
        <BaseSelect
            :model-value="formatBooleanFilter(isActive)"
            :options="activeOptions"
            placeholder="Все статусы"
            aria-label="Фильтр активности"
            @update:model-value="$emit('set-active', parseBooleanFilter($event))"
        />
    </div>

    <div class="org-filters__field org-toolbar__filter-field">
        <BaseSelect
            :model-value="formatBooleanFilter(isPublic)"
            :options="publicOptions"
            placeholder="Все типы"
            aria-label="Фильтр публичности"
            @update:model-value="$emit('set-public', parseBooleanFilter($event))"
        />
    </div>

    <button
        v-if="hasActiveFilters"
        class="dashboard-course-btn"
        type="button"
        @click="$emit('reset')"
    >
        Сбросить
    </button>
</template>
