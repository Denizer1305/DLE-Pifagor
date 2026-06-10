<script setup lang="ts">
interface Props {
    searchValue: string;
    searchPlaceholder?: string;
    isLoading?: boolean;
    createLabel?: string;
    refreshLabel?: string;
    filtersLabel?: string;
}

interface Emits {
    (event: "update:searchValue", value: string): void;
    (event: "search"): void;
    (event: "create"): void;
    (event: "refresh"): void;
}

withDefaults(defineProps<Props>(), {
    searchPlaceholder: "",
    isLoading: false,
    createLabel: "",
    refreshLabel: "",
    filtersLabel: "",
});

defineEmits<Emits>();
</script>

<template>
    <form
        class="org-toolbar admin-users-filters"
        @submit.prevent="$emit('search')"
    >
        <div class="org-toolbar__main admin-users-search">
            <label class="org-toolbar__search">
                <span class="org-toolbar__search-icon">
                    <slot name="search-icon">
                        <i class="fas fa-magnifying-glass"></i>
                    </slot>
                </span>

                <input
                    class="org-toolbar__search-input"
                    type="search"
                    :value="searchValue"
                    :placeholder="searchPlaceholder"
                    @input="
                        $emit(
                            'update:searchValue',
                            ($event.target as HTMLInputElement).value,
                        )
                    "
                    @keyup.enter="$emit('search')"
                />
            </label>
        </div>

        <slot name="filters" />

        <div class="org-toolbar__actions">
            <slot name="before-actions" />

            <button
                v-if="filtersLabel"
                class="dashboard-course-btn primary"
                type="submit"
            >
                <span class="org-toolbar__button-icon">
                    <slot name="filters-icon">
                        <i class="fas fa-sliders"></i>
                    </slot>
                </span>
                {{ filtersLabel }}
            </button>

            <button
                v-if="refreshLabel"
                class="dashboard-course-btn org-toolbar__refresh"
                :class="{ 'is-loading': isLoading }"
                type="button"
                :disabled="isLoading"
                :title="refreshLabel"
                @click="$emit('refresh')"
            >
                <span class="org-toolbar__button-icon">
                    <slot name="refresh-icon">
                        <i class="fas fa-rotate-right"></i>
                    </slot>
                </span>
            </button>

            <button
                v-if="createLabel"
                class="dashboard-course-btn primary"
                type="button"
                @click="$emit('create')"
            >
                <span class="org-toolbar__button-icon">
                    <slot name="create-icon">
                        <i class="fas fa-plus"></i>
                    </slot>
                </span>
                {{ createLabel }}
            </button>

            <slot name="actions" />
        </div>
    </form>
</template>
