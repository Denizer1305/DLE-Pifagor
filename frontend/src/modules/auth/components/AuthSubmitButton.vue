<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";

interface Props {
    label: string;
    loadingLabel?: string;
    icon?: string;
    isLoading?: boolean;
    disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
    loadingLabel: "Пожалуйста, подождите...",
    icon: "fa-solid fa-arrow-right",
    isLoading: false,
    disabled: false,
});

const { tr } = useI18n();

const currentLabel = computed(() => tr(props.label));
const currentLoadingLabel = computed(() => tr(props.loadingLabel));
</script>

<template>
    <button
        class="auth-submit-btn"
        type="submit"
        :disabled="disabled || isLoading"
    >
        <span v-if="isLoading">
            <i class="fa-solid fa-spinner fa-spin"></i>
            {{ currentLoadingLabel }}
        </span>

        <span v-else>
            {{ currentLabel }}
            <i :class="icon"></i>
        </span>
    </button>
</template>
