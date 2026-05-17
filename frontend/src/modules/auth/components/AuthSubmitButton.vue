<script setup lang="ts">
interface Props {
    label: string;
    loadingLabel?: string;
    icon?: string;
    isLoading?: boolean;
    disabled?: boolean;
}

withDefaults(defineProps<Props>(), {
    loadingLabel: "Пожалуйста, подождите...",
    icon: "fa-solid fa-arrow-right",
    isLoading: false,
    disabled: false,
});
</script>

<template>
    <button
        class="auth-submit-btn"
        type="submit"
        :disabled="disabled || isLoading"
    >
        <span v-if="isLoading">
            <i class="fa-solid fa-spinner fa-spin"></i>
            {{ loadingLabel }}
        </span>

        <span v-else>
            {{ label }}
            <i :class="icon"></i>
        </span>
    </button>
</template>