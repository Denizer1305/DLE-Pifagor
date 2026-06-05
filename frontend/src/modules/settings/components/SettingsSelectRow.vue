<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";

import type { SettingsSelectOptionModel } from "@/modules/settings/types/settings.types";

interface Props {
    label: string;
    text?: string;
    modelValue: string;
    options: SettingsSelectOptionModel[];
    disabled?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: string): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <div class="settings-select-row">
        <span class="settings-select-copy">
            <strong>{{ label }}</strong>
            <span v-if="text">{{ text }}</span>
        </span>

        <BaseSelect
            :model-value="modelValue"
            :options="options"
            :aria-label="label"
            :disabled="disabled"
            @update:model-value="emit('update:modelValue', $event)"
        />
    </div>
</template>
